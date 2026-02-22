"""Anthropic messages language model runtime wrapper."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Awaitable, Callable

from packages.provider.src.language_model.v3.language_model_v3_usage import (
  LanguageModelV3Usage,
)

from .convert_anthropic_messages_usage import convertAnthropicMessagesUsage
from .map_anthropic_stop_reason import mapAnthropicStopReason


FetchFunction = Callable[[str, dict[str, Any]], Awaitable[Any]]


@dataclass
class AnthropicMessagesConfig:
  provider: str
  baseURL: str
  headers: Callable[[], dict[str, str]]
  fetch: FetchFunction | None = None
  generateId: Callable[[], str] | None = None
  supportedUrls: Callable[[], dict[str, list[object]]] | None = None


class AnthropicMessagesLanguageModel:
  """Model adapter for Anthropic messages API."""

  specificationVersion = 'v3'

  def __init__(self, modelId: str, config: AnthropicMessagesConfig | dict[str, Any]):
    self.modelId = modelId
    self.config = config

  @property
  def provider(self) -> str:
    if isinstance(self.config, dict):
      return str(self.config['provider'])
    return self.config.provider

  @property
  def supportedUrls(self) -> dict[str, list[object]]:
    if isinstance(self.config, dict):
      builder = self.config.get('supportedUrls')
      return builder() if callable(builder) else {}
    return self.config.supportedUrls() if self.config.supportedUrls else {}

  async def doGenerate(self, options: dict[str, Any]) -> dict[str, Any]:
    """Execute a non-streaming Anthropic message request."""

    base_url = self.config['baseURL'] if isinstance(self.config, dict) else self.config.baseURL
    headers_fn = self.config['headers'] if isinstance(self.config, dict) else self.config.headers
    fetch_fn = self.config.get('fetch') if isinstance(self.config, dict) else self.config.fetch

    request_body = {
      'model': self.modelId,
      'messages': options.get('prompt', []),
    }
    response_payload: dict[str, Any] = {
      'id': None,
      'model': self.modelId,
      'content': [],
      'stop_reason': None,
      'usage': {'input_tokens': 0, 'output_tokens': 0},
    }

    response_headers: dict[str, str] = {}

    if callable(fetch_fn):
      response = await fetch_fn(
        f'{base_url}/messages',
        {
          'method': 'POST',
          'headers': headers_fn(),
          'body': json.dumps(request_body),
        },
      )
      response_headers = dict(getattr(response, 'headers', {}) or {})
      if hasattr(response, 'json'):
        json_result = response.json()
        response_payload = await json_result if hasattr(json_result, '__await__') else json_result

    content: list[dict[str, Any]] = []
    for part in response_payload.get('content', []):
      if part.get('type') == 'text':
        content.append({'type': 'text', 'text': part.get('text', '')})

    usage: LanguageModelV3Usage = convertAnthropicMessagesUsage(
      usage=response_payload.get('usage', {'input_tokens': 0, 'output_tokens': 0}),
    )

    finish_reason = response_payload.get('stop_reason')

    return {
      'content': content,
      'finishReason': {
        'unified': mapAnthropicStopReason(finishReason=finish_reason),
        'raw': finish_reason,
      },
      'usage': usage,
      'request': {'body': request_body},
      'response': {
        'id': response_payload.get('id'),
        'timestamp': datetime.now(UTC),
        'modelId': response_payload.get('model') or self.modelId,
        'headers': response_headers,
        'body': response_payload,
      },
      'warnings': [],
      'providerMetadata': {},
    }


__all__ = ['AnthropicMessagesConfig', 'AnthropicMessagesLanguageModel']

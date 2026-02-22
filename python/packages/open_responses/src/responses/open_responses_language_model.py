"""Open Responses language model implementation mirror."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from packages.provider.src.language_model.v3.language_model_v3_usage import (
  LanguageModelV3Usage,
)

from .convert_to_open_responses_input import convertToOpenResponsesInput
from .map_open_responses_finish_reason import mapOpenResponsesFinishReason
from .open_responses_config import OpenResponsesConfig


class OpenResponsesLanguageModel:
  """Lightweight Python mirror of the TypeScript OpenResponses model."""

  specificationVersion = 'v3'

  def __init__(self, modelId: str, config: OpenResponsesConfig):
    self.modelId = modelId
    self.config = config
    self.supportedUrls = {'image/*': r'^https?://.*$'}

  @property
  def provider(self) -> str:
    if isinstance(self.config, dict):
      return str(self.config['provider'])
    return self.config.provider

  def _headers(self) -> dict[str, str | None]:
    if isinstance(self.config, dict):
      return self.config['headers']()
    return self.config.headers()

  async def _get_args(self, options: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, str]]]:
    warnings: list[dict[str, str]] = []
    converted = await convertToOpenResponsesInput(prompt=options['prompt'])
    warnings.extend(converted['warnings'])
    body = {
      'model': self.modelId,
      'input': converted['input'],
      'instructions': converted['instructions'],
      'max_output_tokens': options.get('maxOutputTokens'),
      'temperature': options.get('temperature'),
      'top_p': options.get('topP'),
      'presence_penalty': options.get('presencePenalty'),
      'frequency_penalty': options.get('frequencyPenalty'),
    }
    return body, warnings

  async def doGenerate(self, options: dict[str, Any]) -> dict[str, Any]:
    body, warnings = await self._get_args(options)
    usage: LanguageModelV3Usage = {
      'inputTokens': {'total': 0, 'noCache': 0, 'cacheRead': 0, 'cacheWrite': None},
      'outputTokens': {'total': 0, 'text': 0, 'reasoning': 0},
    }
    return {
      'content': [],
      'finishReason': {
        'unified': mapOpenResponsesFinishReason(
          finishReason=None,
          hasToolCalls=False,
        ),
        'raw': None,
      },
      'usage': usage,
      'request': {'body': body},
      'response': {
        'id': 'response',
        'timestamp': datetime.now(UTC),
        'modelId': self.modelId,
        'headers': self._headers(),
      },
      'providerMetadata': None,
      'warnings': warnings,
    }

  async def doStream(self, options: dict[str, Any]) -> dict[str, Any]:
    body, warnings = await self._get_args(options)

    async def _stream():
      yield {'type': 'stream-start', 'warnings': warnings}
      yield {
        'type': 'finish',
        'finishReason': {'unified': 'other', 'raw': None},
        'usage': {
          'inputTokens': {
            'total': None,
            'noCache': None,
            'cacheRead': None,
            'cacheWrite': None,
          },
          'outputTokens': {'total': None, 'text': None, 'reasoning': None},
        },
        'providerMetadata': None,
      }

    return {
      'stream': _stream(),
      'request': {'body': body},
      'response': {'headers': self._headers()},
    }

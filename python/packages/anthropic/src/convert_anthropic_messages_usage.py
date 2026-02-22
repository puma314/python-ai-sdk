"""Anthropic usage conversion helpers."""

from __future__ import annotations

from typing import NotRequired, TypedDict

from packages.provider.src.language_model.v3.language_model_v3_usage import (
  LanguageModelV3Usage,
)


class AnthropicUsageIteration(TypedDict):
  """One usage iteration in Anthropic compaction mode."""

  type: str
  input_tokens: int
  output_tokens: int


class AnthropicMessagesUsage(TypedDict, total=False):
  """Anthropic usage payload returned by messages API."""

  input_tokens: int
  output_tokens: int
  cache_creation_input_tokens: NotRequired[int | None]
  cache_read_input_tokens: NotRequired[int | None]
  iterations: NotRequired[list[AnthropicUsageIteration] | None]


def convertAnthropicMessagesUsage(
  *,
  usage: AnthropicMessagesUsage,
  rawUsage: dict[str, object] | None = None,
) -> LanguageModelV3Usage:
  """Convert Anthropic usage structure to the v3 usage shape."""

  cache_creation_tokens = usage.get('cache_creation_input_tokens') or 0
  cache_read_tokens = usage.get('cache_read_input_tokens') or 0

  iterations = usage.get('iterations')
  if iterations:
    input_tokens = sum(iteration.get('input_tokens', 0) for iteration in iterations)
    output_tokens = sum(iteration.get('output_tokens', 0) for iteration in iterations)
  else:
    input_tokens = usage.get('input_tokens', 0)
    output_tokens = usage.get('output_tokens', 0)

  return {
    'inputTokens': {
      'total': input_tokens + cache_creation_tokens + cache_read_tokens,
      'noCache': input_tokens,
      'cacheRead': cache_read_tokens,
      'cacheWrite': cache_creation_tokens,
    },
    'outputTokens': {
      'total': output_tokens,
      'text': None,
      'reasoning': None,
    },
    'raw': rawUsage if rawUsage is not None else usage,  # type: ignore[typeddict-item]
  }


__all__ = [
  'AnthropicMessagesUsage',
  'AnthropicUsageIteration',
  'convertAnthropicMessagesUsage',
]

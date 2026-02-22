"""Convert Moonshot usage payloads into LanguageModelV3 usage shape."""

from typing import TypedDict

from packages.provider.src.language_model.v3.language_model_v3_usage import (
  LanguageModelV3Usage,
)


class _UsagePromptDetails(TypedDict, total=False):
  cached_tokens: int | None


class _UsageCompletionDetails(TypedDict, total=False):
  reasoning_tokens: int | None


class MoonshotUsage(TypedDict, total=False):
  prompt_tokens: int | None
  completion_tokens: int | None
  cached_tokens: int | None
  prompt_tokens_details: _UsagePromptDetails | None
  completion_tokens_details: _UsageCompletionDetails | None


def convertMoonshotAIChatUsage(usage: MoonshotUsage | None) -> LanguageModelV3Usage:
  """Map Moonshot usage fields onto the standardized v3 usage structure."""

  if usage is None:
    return {
      'inputTokens': {
        'total': None,
        'noCache': None,
        'cacheRead': None,
        'cacheWrite': None,
      },
      'outputTokens': {
        'total': None,
        'text': None,
        'reasoning': None,
      },
    }

  prompt_tokens = usage.get('prompt_tokens') or 0
  completion_tokens = usage.get('completion_tokens') or 0
  cache_read = usage.get('cached_tokens')
  if cache_read is None:
    cache_read = (usage.get('prompt_tokens_details') or {}).get('cached_tokens') or 0
  reasoning_tokens = (
    (usage.get('completion_tokens_details') or {}).get('reasoning_tokens') or 0
  )

  return {
    'inputTokens': {
      'total': prompt_tokens,
      'noCache': prompt_tokens - cache_read,
      'cacheRead': cache_read,
      'cacheWrite': None,
    },
    'outputTokens': {
      'total': completion_tokens,
      'text': completion_tokens - reasoning_tokens,
      'reasoning': reasoning_tokens,
    },
    'raw': usage,  # type: ignore[typeddict-item]
  }

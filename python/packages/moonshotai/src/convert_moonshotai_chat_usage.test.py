"""Tests for Moonshot usage conversion helper."""

from .convert_moonshotai_chat_usage import convertMoonshotAIChatUsage


def test_convert_usage_none():
  result = convertMoonshotAIChatUsage(None)
  assert result['inputTokens']['total'] is None
  assert result['outputTokens']['total'] is None


def test_convert_usage_with_cache_and_reasoning():
  result = convertMoonshotAIChatUsage(
    {
      'prompt_tokens': 100,
      'completion_tokens': 80,
      'cached_tokens': 35,
      'completion_tokens_details': {'reasoning_tokens': 30},
    }
  )
  assert result['inputTokens']['noCache'] == 65
  assert result['outputTokens']['text'] == 50
  assert result['outputTokens']['reasoning'] == 30

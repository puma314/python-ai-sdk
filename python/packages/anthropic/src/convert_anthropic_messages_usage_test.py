"""Tests for Anthropic usage conversion."""

from .convert_anthropic_messages_usage import convertAnthropicMessagesUsage


def test_uses_usage_as_raw_when_raw_usage_missing():
  usage = {'input_tokens': 10, 'output_tokens': 20}
  result = convertAnthropicMessagesUsage(usage=usage)
  assert result['raw'] == usage


def test_computes_token_totals_with_cache_tokens():
  result = convertAnthropicMessagesUsage(
    usage={
      'input_tokens': 10,
      'output_tokens': 20,
      'cache_creation_input_tokens': 5,
      'cache_read_input_tokens': 3,
    }
  )
  assert result['inputTokens'] == {
    'total': 18,
    'noCache': 10,
    'cacheRead': 3,
    'cacheWrite': 5,
  }
  assert result['outputTokens']['total'] == 20


def test_uses_iterations_when_present():
  result = convertAnthropicMessagesUsage(
    usage={
      'input_tokens': 45000,
      'output_tokens': 1234,
      'iterations': [
        {'type': 'compaction', 'input_tokens': 180000, 'output_tokens': 3500},
        {'type': 'message', 'input_tokens': 23000, 'output_tokens': 1000},
      ],
    }
  )
  assert result['inputTokens']['total'] == 203000
  assert result['outputTokens']['total'] == 4500

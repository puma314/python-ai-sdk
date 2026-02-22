"""Tests for Anthropic provider factory."""

import pytest

from .anthropic_provider import AnthropicProviderSettings, createAnthropic


class _Response:
  def __init__(self, payload: dict):
    self._payload = payload
    self.headers = {'content-type': 'application/json'}

  async def json(self):
    return self._payload


@pytest.mark.asyncio
async def test_uses_default_anthropic_base_url_when_not_provided(monkeypatch):
  monkeypatch.delenv('ANTHROPIC_BASE_URL', raising=False)
  fetch_calls: list[tuple[str, dict]] = []

  async def fetch(url: str, options: dict):
    fetch_calls.append((url, options))
    return _Response(
      {
        'type': 'message',
        'id': 'msg_123',
        'model': 'claude-3-haiku-20240307',
        'content': [{'type': 'text', 'text': 'Hi'}],
        'stop_reason': None,
        'usage': {'input_tokens': 1, 'output_tokens': 1},
      }
    )

  provider = createAnthropic(
    AnthropicProviderSettings(apiKey='test-api-key', fetch=fetch)
  )
  await provider('claude-3-haiku-20240307').doGenerate(
    {'prompt': [{'role': 'user', 'content': [{'type': 'text', 'text': 'Hello'}]}]}
  )
  assert fetch_calls[0][0] == 'https://api.anthropic.com/v1/messages'


def test_raises_when_api_key_and_auth_token_both_provided():
  with pytest.raises(Exception):
    createAnthropic(
      AnthropicProviderSettings(apiKey='api-key', authToken='auth-token')
    )


def test_custom_provider_name_is_used():
  provider = createAnthropic(
    AnthropicProviderSettings(apiKey='test-api-key', name='my-claude-proxy')
  )
  model = provider('claude-3-haiku-20240307')
  assert model.provider == 'my-claude-proxy'

"""Tests for AnthropicMessagesLanguageModel."""

import pytest

from .anthropic_messages_language_model import AnthropicMessagesLanguageModel


class _Response:
  def __init__(self, payload: dict):
    self.payload = payload
    self.headers = {'content-type': 'application/json'}

  async def json(self):
    return self.payload


@pytest.mark.asyncio
async def test_do_generate_calls_fetch_and_maps_response():
  async def fetch(url: str, options: dict):
    assert url.endswith('/messages')
    return _Response(
      {
        'id': 'msg_1',
        'model': 'claude-3-haiku-20240307',
        'content': [{'type': 'text', 'text': 'Hi'}],
        'stop_reason': 'end_turn',
        'usage': {'input_tokens': 1, 'output_tokens': 1},
      }
    )

  model = AnthropicMessagesLanguageModel(
    'claude-3-haiku-20240307',
    {
      'provider': 'anthropic.messages',
      'baseURL': 'https://api.anthropic.com/v1',
      'headers': lambda: {'x-api-key': 'key'},
      'fetch': fetch,
      'supportedUrls': lambda: {},
    },
  )

  result = await model.doGenerate(
    {'prompt': [{'role': 'user', 'content': [{'type': 'text', 'text': 'Hello'}]}]}
  )
  assert result['content'][0]['text'] == 'Hi'
  assert result['finishReason']['unified'] == 'stop'


def test_provider_property_returns_configured_provider():
  model = AnthropicMessagesLanguageModel(
    'claude-3-haiku-20240307',
    {
      'provider': 'my-provider',
      'baseURL': 'https://api.anthropic.com/v1',
      'headers': lambda: {},
      'supportedUrls': lambda: {},
    },
  )
  assert model.provider == 'my-provider'

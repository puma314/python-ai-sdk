"""Tests for OpenResponsesLanguageModel."""

import pytest

from .open_responses_language_model import OpenResponsesLanguageModel


def _create_model():
  return OpenResponsesLanguageModel(
    'gemma-7b-it',
    config={
      'provider': 'lmstudio',
      'url': 'https://localhost:1234/v1/responses',
      'headers': lambda: {},
      'fetch': None,
      'generateId': lambda: 'id',
    },
  )


@pytest.mark.asyncio
async def test_do_generate_returns_standard_shape():
  model = _create_model()
  result = await model.doGenerate(
    options={'prompt': [{'role': 'user', 'content': [{'type': 'text', 'text': 'Hi'}]}]}
  )
  assert 'content' in result
  assert 'usage' in result
  assert result['response']['modelId'] == 'gemma-7b-it'


@pytest.mark.asyncio
async def test_do_stream_emits_start_and_finish():
  model = _create_model()
  result = await model.doStream(
    options={'prompt': [{'role': 'user', 'content': [{'type': 'text', 'text': 'Hi'}]}]}
  )
  items = [item async for item in result['stream']]
  assert items[0]['type'] == 'stream-start'
  assert items[-1]['type'] == 'finish'

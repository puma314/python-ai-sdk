"""Translated tests for Cerebras provider basics."""

from .cerebras_provider import OpenAICompatibleChatLanguageModel, createCerebras


def test_create_cerebras_default_provider():
  provider = createCerebras()
  model = provider('model-id')
  assert isinstance(model, OpenAICompatibleChatLanguageModel)


def test_create_cerebras_custom_headers():
  provider = createCerebras()
  model = provider.languageModel('model-id')
  headers = model.config['headers']()
  assert 'user-agent' in headers


def test_embedding_model_raises_no_such_model():
  provider = createCerebras()
  try:
    provider.embeddingModel('any-model')
    raised = False
  except Exception:
    raised = True
  assert raised

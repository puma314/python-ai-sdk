"""Basic tests for MoonshotAI provider factory."""

from .moonshotai_chat_language_model import MoonshotAIChatLanguageModel
from .moonshotai_provider import createMoonshotAI


def test_provider_returns_chat_model():
  provider = createMoonshotAI()
  model = provider('kimi-k2.5')
  assert isinstance(model, MoonshotAIChatLanguageModel)


def test_provider_raises_for_embedding_model():
  provider = createMoonshotAI()
  try:
    provider.embeddingModel('foo')
    raised = False
  except Exception:
    raised = True
  assert raised

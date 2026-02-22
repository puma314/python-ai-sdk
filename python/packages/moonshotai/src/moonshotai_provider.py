"""MoonshotAI provider factory mirror."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from pydantic import BaseModel

from packages.provider.src.errors.no_such_model_error import NoSuchModelError

from .moonshotai_chat_language_model import MoonshotAIChatLanguageModel
from .moonshotai_chat_options import MoonshotAIChatModelId
from .version import VERSION


class MoonshotAIErrorData(BaseModel):
  """Error schema returned by Moonshot endpoints."""

  error: dict[str, str | None]


@dataclass
class MoonshotAIProviderSettings:
  """Configuration options for Moonshot provider creation."""

  apiKey: str | None = None
  baseURL: str | None = None
  headers: dict[str, str] | None = None
  fetch: Callable[..., object] | None = None


def _without_trailing_slash(url: str) -> str:
  return url[:-1] if url.endswith('/') else url


def createMoonshotAI(options: MoonshotAIProviderSettings | None = None):
  """Create a MoonshotAI provider instance."""

  settings = options or MoonshotAIProviderSettings()
  baseURL = _without_trailing_slash(settings.baseURL or 'https://api.moonshot.ai/v1')

  def getHeaders() -> dict[str, str]:
    headers = {
      'Authorization': f'Bearer {settings.apiKey or "MOONSHOT_API_KEY"}',
      'user-agent': f'ai-sdk/moonshotai/{VERSION}',
    }
    if settings.headers:
      headers.update(settings.headers)
    return headers

  def createChatModel(modelId: MoonshotAIChatModelId):
    return MoonshotAIChatLanguageModel(
      str(modelId),
      {
        'provider': 'moonshotai.chat',
        'url': lambda path: f'{baseURL}{path}',
        'headers': getHeaders,
        'fetch': settings.fetch,
      },
    )

  class _Provider:
    specificationVersion = 'v3'

    def __call__(self, modelId: MoonshotAIChatModelId):
      return createChatModel(modelId)

    def chatModel(self, modelId: MoonshotAIChatModelId):
      return createChatModel(modelId)

    def languageModel(self, modelId: MoonshotAIChatModelId):
      return createChatModel(modelId)

    def embeddingModel(self, modelId: str):
      raise NoSuchModelError(modelId=modelId, modelType='embeddingModel')

    def imageModel(self, modelId: str):
      raise NoSuchModelError(modelId=modelId, modelType='imageModel')

  return _Provider()


moonshotai = createMoonshotAI()

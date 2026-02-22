"""Cerebras provider factory and provider protocol mirror."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Protocol

from pydantic import BaseModel

from packages.provider.src.errors import NoSuchModelError

from .cerebras_chat_options import CerebrasChatModelId
from .version import VERSION


class CerebrasErrorData(BaseModel):
  """Schema for Cerebras error payloads."""

  message: str
  type: str
  param: str
  code: str


@dataclass
class CerebrasProviderSettings:
  """Configuration for constructing a Cerebras provider."""

  apiKey: str | None = None
  baseURL: str | None = None
  headers: dict[str, str] | None = None
  fetch: Callable[..., object] | None = None


@dataclass
class OpenAICompatibleChatLanguageModel:
  """Minimal runtime placeholder for the TS OpenAI-compatible model."""

  modelId: str
  config: dict[str, object]


class CerebrasProvider(Protocol):
  """Provider interface for creating Cerebras language models."""

  specificationVersion: str

  def __call__(self, modelId: CerebrasChatModelId) -> OpenAICompatibleChatLanguageModel: ...

  def languageModel(
    self, modelId: CerebrasChatModelId
  ) -> OpenAICompatibleChatLanguageModel: ...

  def chat(
    self, modelId: CerebrasChatModelId
  ) -> OpenAICompatibleChatLanguageModel: ...

  def embeddingModel(self, modelId: str) -> object: ...

  def textEmbeddingModel(self, modelId: str) -> object: ...

  def imageModel(self, modelId: str) -> object: ...


def _without_trailing_slash(url: str) -> str:
  return url[:-1] if url.endswith('/') else url


def createCerebras(options: CerebrasProviderSettings | None = None):
  """Create a Cerebras provider instance."""

  settings = options or CerebrasProviderSettings()
  baseURL = _without_trailing_slash(settings.baseURL or 'https://api.cerebras.ai/v1')

  def getHeaders() -> dict[str, str]:
    base_headers = {
      'Authorization': f'Bearer {settings.apiKey or "CEREBRAS_API_KEY"}',
      'user-agent': f'ai-sdk/cerebras/{VERSION}',
    }
    if settings.headers:
      base_headers.update(settings.headers)
    return base_headers

  def createLanguageModel(modelId: CerebrasChatModelId):
    return OpenAICompatibleChatLanguageModel(
      str(modelId),
      {
        'provider': 'cerebras.chat',
        'url': lambda path: f'{baseURL}{path}',
        'headers': getHeaders,
        'fetch': settings.fetch,
        'supportsStructuredOutputs': True,
      },
    )

  class _Provider:
    specificationVersion = 'v3'

    def __call__(self, modelId: CerebrasChatModelId):
      return createLanguageModel(modelId)

    def languageModel(self, modelId: CerebrasChatModelId):
      return createLanguageModel(modelId)

    def chat(self, modelId: CerebrasChatModelId):
      return createLanguageModel(modelId)

    def embeddingModel(self, modelId: str):
      raise NoSuchModelError(modelId=modelId, modelType='embeddingModel')

    def textEmbeddingModel(self, modelId: str):
      return self.embeddingModel(modelId)

    def imageModel(self, modelId: str):
      raise NoSuchModelError(modelId=modelId, modelType='imageModel')

  return _Provider()


cerebras = createCerebras()

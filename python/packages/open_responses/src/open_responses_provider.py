"""Factory for Open Responses provider instances."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
from uuid import uuid4

from packages.provider.src.errors.no_such_model_error import NoSuchModelError

from .responses.open_responses_config import OpenResponsesConfig
from .responses.open_responses_language_model import OpenResponsesLanguageModel
from .version import VERSION


@dataclass
class OpenResponsesProviderSettings:
  """Settings for Open Responses provider factory."""

  url: str
  name: str
  apiKey: str | None = None
  headers: dict[str, str] | None = None
  fetch: Callable[..., object] | None = None


def createOpenResponses(options: OpenResponsesProviderSettings):
  """Create an Open Responses provider."""

  providerName = options.name

  def getHeaders() -> dict[str, str]:
    headers = {
      'user-agent': f'ai-sdk/open-responses/{VERSION}',
      **(options.headers or {}),
    }
    if options.apiKey:
      headers['Authorization'] = f'Bearer {options.apiKey}'
    return headers

  def createResponsesModel(modelId: str) -> OpenResponsesLanguageModel:
    config: OpenResponsesConfig = {
      'provider': f'{providerName}.responses',
      'headers': getHeaders,
      'url': options.url,
      'fetch': options.fetch,
      'generateId': lambda: str(uuid4()),
    }
    return OpenResponsesLanguageModel(modelId, config)

  def createLanguageModel(modelId: str):
    return createResponsesModel(modelId)

  class _Provider:
    specificationVersion = 'v3'

    def __call__(self, modelId: str):
      return createLanguageModel(modelId)

    languageModel = staticmethod(createLanguageModel)

    @staticmethod
    def embeddingModel(modelId: str):
      raise NoSuchModelError(modelId=modelId, modelType='embeddingModel')

    @staticmethod
    def imageModel(modelId: str):
      raise NoSuchModelError(modelId=modelId, modelType='imageModel')

  return _Provider()

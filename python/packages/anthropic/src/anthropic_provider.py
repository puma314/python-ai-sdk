"""Anthropic provider factory."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Protocol

from packages.provider.src.errors.invalid_argument_error import InvalidArgumentError
from packages.provider.src.errors.no_such_model_error import NoSuchModelError
from packages.provider_utils.src.generate_id import generateId
from packages.provider_utils.src.load_api_key import loadApiKey
from packages.provider_utils.src.load_optional_setting import loadOptionalSetting
from packages.provider_utils.src.with_user_agent_suffix import withUserAgentSuffix
from packages.provider_utils.src.without_trailing_slash import withoutTrailingSlash

from .anthropic_messages_language_model import AnthropicMessagesLanguageModel
from .anthropic_tools import anthropicTools
from .version import VERSION


@dataclass
class AnthropicProviderSettings:
  baseURL: str | None = None
  apiKey: str | None = None
  authToken: str | None = None
  headers: dict[str, str] | None = None
  fetch: Callable[..., object] | None = None
  generateId: Callable[[], str] | None = None
  name: str | None = None


class AnthropicProvider(Protocol):
  specificationVersion: str

  def __call__(self, modelId: str) -> AnthropicMessagesLanguageModel: ...

  def languageModel(self, modelId: str) -> AnthropicMessagesLanguageModel: ...

  def chat(self, modelId: str) -> AnthropicMessagesLanguageModel: ...

  def messages(self, modelId: str) -> AnthropicMessagesLanguageModel: ...


def createAnthropic(
  options: AnthropicProviderSettings | None = None,
) -> AnthropicProvider:
  """Create an Anthropic provider instance."""

  settings = options or AnthropicProviderSettings()
  if settings.apiKey and settings.authToken:
    raise InvalidArgumentError(
      argument='apiKey/authToken',
      message=(
        'Both apiKey and authToken were provided. '
        'Please use only one authentication method.'
      ),
    )

  base_url = (
    withoutTrailingSlash(
      loadOptionalSetting(
        settingValue=settings.baseURL,
        environmentVariableName='ANTHROPIC_BASE_URL',
      )
    )
    or 'https://api.anthropic.com/v1'
  )
  provider_name = settings.name or 'anthropic.messages'

  def getHeaders() -> dict[str, str]:
    if settings.authToken:
      auth_headers = {'authorization': f'Bearer {settings.authToken}'}
    else:
      auth_headers = {
        'x-api-key': loadApiKey(
          apiKey=settings.apiKey,
          environmentVariableName='ANTHROPIC_API_KEY',
          description='Anthropic',
        )
      }
    merged = {
      'anthropic-version': '2023-06-01',
      **auth_headers,
      **(settings.headers or {}),
    }
    return withUserAgentSuffix(merged, f'ai-sdk/anthropic/{VERSION}')

  def createChatModel(modelId: str) -> AnthropicMessagesLanguageModel:
    return AnthropicMessagesLanguageModel(
      modelId,
      {
        'provider': provider_name,
        'baseURL': base_url,
        'headers': getHeaders,
        'fetch': settings.fetch,
        'generateId': settings.generateId or generateId,
        'supportedUrls': lambda: {
          'image/*': [r'^https?://.*$'],
          'application/pdf': [r'^https?://.*$'],
        },
      },
    )

  class _Provider:
    specificationVersion = 'v3'
    tools = anthropicTools

    def __call__(self, modelId: str) -> AnthropicMessagesLanguageModel:
      return createChatModel(modelId)

    def languageModel(self, modelId: str) -> AnthropicMessagesLanguageModel:
      return createChatModel(modelId)

    def chat(self, modelId: str) -> AnthropicMessagesLanguageModel:
      return createChatModel(modelId)

    def messages(self, modelId: str) -> AnthropicMessagesLanguageModel:
      return createChatModel(modelId)

    def embeddingModel(self, modelId: str):
      raise NoSuchModelError(modelId=modelId, modelType='embeddingModel')

    def textEmbeddingModel(self, modelId: str):
      return self.embeddingModel(modelId)

    def imageModel(self, modelId: str):
      raise NoSuchModelError(modelId=modelId, modelType='imageModel')

  return _Provider()


anthropic = createAnthropic()


__all__ = [
  'AnthropicProvider',
  'AnthropicProviderSettings',
  'createAnthropic',
  'anthropic',
]

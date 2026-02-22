from typing import Literal, NotRequired, TypeAlias, TypedDict

from ...shared.v3.shared_v3_provider_metadata import SharedV3ProviderMetadata


class LanguageModelV3UrlSource(TypedDict):
  type: Literal['source']
  sourceType: Literal['url']
  id: str
  url: str
  title: NotRequired[str]
  providerMetadata: NotRequired[SharedV3ProviderMetadata]


class LanguageModelV3DocumentSource(TypedDict):
  type: Literal['source']
  sourceType: Literal['document']
  id: str
  mediaType: str
  title: str
  filename: NotRequired[str]
  providerMetadata: NotRequired[SharedV3ProviderMetadata]


LanguageModelV3Source: TypeAlias = (
  LanguageModelV3UrlSource | LanguageModelV3DocumentSource
)

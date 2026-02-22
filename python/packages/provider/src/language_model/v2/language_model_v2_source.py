from typing import Literal, NotRequired, TypeAlias, TypedDict

from ...shared.v2.shared_v2_provider_metadata import SharedV2ProviderMetadata


class LanguageModelV2URLSource(TypedDict):
  type: Literal['source']
  sourceType: Literal['url']
  id: str
  url: str
  title: NotRequired[str]
  providerMetadata: NotRequired[SharedV2ProviderMetadata]


class LanguageModelV2DocumentSource(TypedDict):
  type: Literal['source']
  sourceType: Literal['document']
  id: str
  mediaType: str
  title: str
  filename: NotRequired[str]
  providerMetadata: NotRequired[SharedV2ProviderMetadata]


LanguageModelV2Source: TypeAlias = (
  LanguageModelV2URLSource | LanguageModelV2DocumentSource
)

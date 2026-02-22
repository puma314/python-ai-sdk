from typing import Literal, NotRequired, TypedDict

from ...shared.v3.shared_v3_provider_metadata import SharedV3ProviderMetadata


class LanguageModelV3Text(TypedDict):
  type: Literal['text']
  text: str
  providerMetadata: NotRequired[SharedV3ProviderMetadata]

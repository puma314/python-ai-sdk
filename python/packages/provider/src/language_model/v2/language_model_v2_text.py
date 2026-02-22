from typing import Literal, NotRequired, TypedDict

from ...shared.v2.shared_v2_provider_metadata import SharedV2ProviderMetadata


class LanguageModelV2Text(TypedDict):
  type: Literal['text']
  text: str
  providerMetadata: NotRequired[SharedV2ProviderMetadata]

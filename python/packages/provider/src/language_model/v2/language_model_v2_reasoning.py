from typing import Literal, NotRequired, TypedDict

from ...shared.v2.shared_v2_provider_metadata import SharedV2ProviderMetadata


class LanguageModelV2Reasoning(TypedDict):
  type: Literal['reasoning']
  text: str
  providerMetadata: NotRequired[SharedV2ProviderMetadata]

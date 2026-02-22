from typing import Literal, NotRequired, TypedDict

from ...shared.v3.shared_v3_provider_metadata import SharedV3ProviderMetadata


class LanguageModelV3File(TypedDict):
  type: Literal['file']
  mediaType: str
  data: str | bytes
  providerMetadata: NotRequired[SharedV3ProviderMetadata]

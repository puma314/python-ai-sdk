from typing import NotRequired, TypedDict

from ...shared.v3.shared_v3_headers import SharedV3Headers
from ...shared.v3.shared_v3_provider_options import SharedV3ProviderOptions


class EmbeddingModelV3CallOptions(TypedDict):
  values: list[str]
  abortSignal: NotRequired[object]
  providerOptions: NotRequired[SharedV3ProviderOptions]
  headers: NotRequired[SharedV3Headers]

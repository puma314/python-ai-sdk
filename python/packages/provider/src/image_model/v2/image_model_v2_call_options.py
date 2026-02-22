from typing import NotRequired, TypedDict

from ...shared.v2.shared_v2_provider_options import SharedV2ProviderOptions


class ImageModelV2CallOptions(TypedDict):
  prompt: str
  n: int
  size: str | None
  aspectRatio: str | None
  seed: int | None
  providerOptions: SharedV2ProviderOptions
  abortSignal: NotRequired[object]
  headers: NotRequired[dict[str, str | None]]

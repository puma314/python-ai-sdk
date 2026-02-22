"""Call options for image-model v3 generation."""

from typing import NotRequired, TypedDict

from ...shared.v3.shared_v3_provider_options import SharedV3ProviderOptions
from .image_model_v3_file import ImageModelV3File


class ImageModelV3CallOptions(TypedDict):
  """Standardized options passed to image providers."""

  prompt: str | None
  n: int
  size: str | None
  aspectRatio: str | None
  seed: int | None
  files: ImageModelV3File | list[ImageModelV3File] | None
  mask: ImageModelV3File | None
  providerOptions: SharedV3ProviderOptions
  abortSignal: NotRequired[object]
  headers: NotRequired[dict[str, str | None]]

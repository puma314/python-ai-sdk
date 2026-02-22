"""Call options for video-model v3 generation."""

from typing import NotRequired, TypedDict

from ...shared.v3.shared_v3_provider_options import SharedV3ProviderOptions
from .video_model_v3_file import VideoModelV3File


class VideoModelV3CallOptions(TypedDict):
  prompt: str | None
  n: int
  aspectRatio: str | None
  resolution: str | None
  duration: float | None
  fps: float | None
  seed: int | None
  image: VideoModelV3File | None
  providerOptions: SharedV3ProviderOptions
  abortSignal: NotRequired[object]
  headers: NotRequired[dict[str, str | None]]

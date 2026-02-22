"""Video generation model specification version 3."""

from __future__ import annotations

from typing import Awaitable, Callable, Literal, NotRequired, Protocol, TypeAlias, TypedDict

from ...shared.v3.shared_v3_provider_metadata import SharedV3ProviderMetadata
from ...shared.v3.shared_v3_warning import SharedV3Warning
from .video_model_v3_call_options import VideoModelV3CallOptions


class VideoModelV3URLData(TypedDict):
  type: Literal['url']
  url: str
  mediaType: str


class VideoModelV3Base64Data(TypedDict):
  type: Literal['base64']
  data: str
  mediaType: str


class VideoModelV3BinaryData(TypedDict):
  type: Literal['binary']
  data: bytes
  mediaType: str


VideoModelV3VideoData: TypeAlias = (
  VideoModelV3URLData | VideoModelV3Base64Data | VideoModelV3BinaryData
)

GetMaxVideosPerCallFunction: TypeAlias = Callable[[dict[str, str]], int | None]


class VideoModelV3Response(TypedDict):
  timestamp: object
  modelId: str
  headers: dict[str, str] | None


class VideoModelV3Result(TypedDict):
  videos: list[VideoModelV3VideoData]
  warnings: list[SharedV3Warning]
  providerMetadata: NotRequired[SharedV3ProviderMetadata]
  response: VideoModelV3Response


class VideoModelV3(Protocol):
  specificationVersion: str
  provider: str
  modelId: str
  maxVideosPerCall: int | None | GetMaxVideosPerCallFunction

  def doGenerate(
    self, options: VideoModelV3CallOptions
  ) -> Awaitable[VideoModelV3Result]: ...

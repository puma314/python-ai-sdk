"""Input file definitions for video-model v3 generation."""

from typing import Literal, NotRequired, TypeAlias, TypedDict

from ...shared.v3.shared_v3_provider_metadata import SharedV3ProviderMetadata


class VideoModelV3BinaryFile(TypedDict):
  type: Literal['file']
  mediaType: str
  data: str | bytes
  providerOptions: NotRequired[SharedV3ProviderMetadata]


class VideoModelV3URLFile(TypedDict):
  type: Literal['url']
  url: str
  providerOptions: NotRequired[SharedV3ProviderMetadata]


VideoModelV3File: TypeAlias = VideoModelV3BinaryFile | VideoModelV3URLFile

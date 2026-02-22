"""Image generation model specification version 3."""

from __future__ import annotations

from typing import Awaitable, Callable, NotRequired, Protocol, TypeAlias, TypedDict

from ...json_value.json_value import JSONArray, JSONValue
from ...shared.v3.shared_v3_warning import SharedV3Warning
from .image_model_v3_call_options import ImageModelV3CallOptions
from .image_model_v3_usage import ImageModelV3Usage

ImageModelV3ProviderMetadata: TypeAlias = dict[
  str, dict[str, JSONArray] | JSONValue
]

GetMaxImagesPerCallFunction: TypeAlias = Callable[[dict[str, str]], int | None]


class ImageModelV3Response(TypedDict):
  """Response metadata for telemetry and debugging."""

  timestamp: object
  modelId: str
  headers: dict[str, str] | None


class ImageModelV3Result(TypedDict):
  """Result payload returned by image generation providers."""

  images: list[str] | list[bytes]
  warnings: list[SharedV3Warning]
  providerMetadata: NotRequired[ImageModelV3ProviderMetadata]
  response: ImageModelV3Response
  usage: NotRequired[ImageModelV3Usage]


class ImageModelV3(Protocol):
  """Protocol for v3 image generation providers."""

  specificationVersion: str
  provider: str
  modelId: str
  maxImagesPerCall: int | None | GetMaxImagesPerCallFunction

  def doGenerate(
    self, options: ImageModelV3CallOptions
  ) -> Awaitable[ImageModelV3Result]: ...

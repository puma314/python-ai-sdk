from typing import Awaitable, NotRequired, Protocol, TypeAlias, TypedDict

from ...json_value.json_value import JSONArray, JSONValue
from .image_model_v2_call_options import ImageModelV2CallOptions
from .image_model_v2_call_warning import ImageModelV2CallWarning

ImageModelV2ProviderMetadata: TypeAlias = dict[
  str, dict[str, JSONArray] | JSONValue
]


class ImageModelV2Response(TypedDict):
  timestamp: object
  modelId: str
  headers: dict[str, str] | None


class ImageModelV2Result(TypedDict):
  images: list[str] | list[bytes]
  warnings: list[ImageModelV2CallWarning]
  providerMetadata: NotRequired[ImageModelV2ProviderMetadata]
  response: ImageModelV2Response


class ImageModelV2(Protocol):
  specificationVersion: str
  provider: str
  modelId: str
  maxImagesPerCall: int | None

  def doGenerate(
    self, options: ImageModelV2CallOptions
  ) -> Awaitable[ImageModelV2Result]: ...

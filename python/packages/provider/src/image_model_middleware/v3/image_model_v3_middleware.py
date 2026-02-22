"""Middleware contract for image-model v3 wrappers."""

from typing import Callable, NotRequired, TypedDict

from ...image_model.v3.image_model_v3 import ImageModelV3, ImageModelV3Result
from ...image_model.v3.image_model_v3_call_options import ImageModelV3CallOptions


class ImageModelV3Middleware(TypedDict):
  """Shape of middleware hooks for image generation models."""

  specificationVersion: str
  overrideProvider: NotRequired[Callable[[dict[str, ImageModelV3]], str]]
  overrideModelId: NotRequired[Callable[[dict[str, ImageModelV3]], str]]
  overrideMaxImagesPerCall: NotRequired[
    Callable[[dict[str, ImageModelV3]], object]
  ]
  transformParams: NotRequired[
    Callable[[dict[str, object]], ImageModelV3CallOptions]
  ]
  wrapGenerate: NotRequired[Callable[[dict[str, object]], ImageModelV3Result]]

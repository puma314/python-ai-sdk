"""Middleware contract for language-model v3 wrappers."""

from typing import Callable, NotRequired, TypedDict

from ...language_model.v3.language_model_v3 import LanguageModelV3
from ...language_model.v3.language_model_v3_call_options import (
  LanguageModelV3CallOptions,
)
from ...language_model.v3.language_model_v3_generate_result import (
  LanguageModelV3GenerateResult,
)
from ...language_model.v3.language_model_v3_stream_result import (
  LanguageModelV3StreamResult,
)


class LanguageModelV3Middleware(TypedDict):
  specificationVersion: str
  overrideProvider: NotRequired[Callable[[dict[str, LanguageModelV3]], str]]
  overrideModelId: NotRequired[Callable[[dict[str, LanguageModelV3]], str]]
  overrideSupportedUrls: NotRequired[Callable[[dict[str, LanguageModelV3]], dict]]
  transformParams: NotRequired[
    Callable[[dict[str, object]], LanguageModelV3CallOptions]
  ]
  wrapGenerate: NotRequired[Callable[[dict[str, object]], LanguageModelV3GenerateResult]]
  wrapStream: NotRequired[Callable[[dict[str, object]], LanguageModelV3StreamResult]]

"""Middleware contract for language-model v2 wrappers."""

from typing import Callable, NotRequired, TypedDict

from ...language_model.v2.language_model_v2 import LanguageModelV2
from ...language_model.v2.language_model_v2_call_options import (
  LanguageModelV2CallOptions,
)
from ...language_model.v2.language_model_v2 import (
  LanguageModelV2GenerateResult,
  LanguageModelV2StreamResult,
)


class LanguageModelV2Middleware(TypedDict):
  middlewareVersion: NotRequired[str]
  overrideProvider: NotRequired[Callable[[dict[str, LanguageModelV2]], str]]
  overrideModelId: NotRequired[Callable[[dict[str, LanguageModelV2]], str]]
  overrideSupportedUrls: NotRequired[Callable[[dict[str, LanguageModelV2]], dict]]
  transformParams: NotRequired[
    Callable[[dict[str, object]], LanguageModelV2CallOptions]
  ]
  wrapGenerate: NotRequired[Callable[[dict[str, object]], LanguageModelV2GenerateResult]]
  wrapStream: NotRequired[Callable[[dict[str, object]], LanguageModelV2StreamResult]]

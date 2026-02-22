from __future__ import annotations

import re
from typing import Awaitable, Literal, Protocol

from .language_model_v3_call_options import LanguageModelV3CallOptions
from .language_model_v3_generate_result import LanguageModelV3GenerateResult
from .language_model_v3_stream_result import LanguageModelV3StreamResult


class LanguageModelV3(Protocol):
  specificationVersion: Literal['v3']
  provider: str
  modelId: str
  supportedUrls: (
    Awaitable[dict[str, list[re.Pattern[str]]]]
    | dict[str, list[re.Pattern[str]]]
  )

  def doGenerate(
    self, options: LanguageModelV3CallOptions
  ) -> Awaitable[LanguageModelV3GenerateResult]: ...

  def doStream(
    self, options: LanguageModelV3CallOptions
  ) -> Awaitable[LanguageModelV3StreamResult]: ...

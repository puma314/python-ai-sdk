from __future__ import annotations

import re
from typing import AsyncIterable, Awaitable, Literal, NotRequired, Protocol, TypedDict

from ...shared.v2.shared_v2_headers import SharedV2Headers
from ...shared.v2.shared_v2_provider_metadata import SharedV2ProviderMetadata
from .language_model_v2_call_options import LanguageModelV2CallOptions
from .language_model_v2_call_warning import LanguageModelV2CallWarning
from .language_model_v2_content import LanguageModelV2Content
from .language_model_v2_finish_reason import LanguageModelV2FinishReason
from .language_model_v2_response_metadata import LanguageModelV2ResponseMetadata
from .language_model_v2_stream_part import LanguageModelV2StreamPart
from .language_model_v2_usage import LanguageModelV2Usage


class LanguageModelV2GenerateRequestMetadata(TypedDict):
  body: NotRequired[object]


class LanguageModelV2GenerateResponseMetadata(LanguageModelV2ResponseMetadata):
  headers: NotRequired[SharedV2Headers]
  body: NotRequired[object]


class LanguageModelV2GenerateResult(TypedDict):
  content: list[LanguageModelV2Content]
  finishReason: LanguageModelV2FinishReason
  usage: LanguageModelV2Usage
  providerMetadata: NotRequired[SharedV2ProviderMetadata]
  request: NotRequired[LanguageModelV2GenerateRequestMetadata]
  response: NotRequired[LanguageModelV2GenerateResponseMetadata]
  warnings: list[LanguageModelV2CallWarning]


class LanguageModelV2StreamRequestMetadata(TypedDict):
  body: NotRequired[object]


class LanguageModelV2StreamResponseMetadata(TypedDict):
  headers: NotRequired[SharedV2Headers]


class LanguageModelV2StreamResult(TypedDict):
  stream: AsyncIterable[LanguageModelV2StreamPart]
  request: NotRequired[LanguageModelV2StreamRequestMetadata]
  response: NotRequired[LanguageModelV2StreamResponseMetadata]


class LanguageModelV2(Protocol):
  specificationVersion: Literal['v2']
  provider: str
  modelId: str
  supportedUrls: (
    Awaitable[dict[str, list[re.Pattern[str]]]]
    | dict[str, list[re.Pattern[str]]]
  )

  def doGenerate(
    self, options: LanguageModelV2CallOptions
  ) -> Awaitable[LanguageModelV2GenerateResult]: ...

  def doStream(
    self, options: LanguageModelV2CallOptions
  ) -> Awaitable[LanguageModelV2StreamResult]: ...

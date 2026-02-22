from typing import Any, AsyncIterable, NotRequired, TypedDict

from ...shared.v3.shared_v3_headers import SharedV3Headers
from .language_model_v3_stream_part import LanguageModelV3StreamPart


class LanguageModelV3StreamRequestInfo(TypedDict):
  body: NotRequired[Any]


class LanguageModelV3StreamResponseInfo(TypedDict):
  headers: NotRequired[SharedV3Headers]


class LanguageModelV3StreamResult(TypedDict):
  stream: AsyncIterable[LanguageModelV3StreamPart]
  request: NotRequired[LanguageModelV3StreamRequestInfo]
  response: NotRequired[LanguageModelV3StreamResponseInfo]

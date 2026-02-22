"""Speech model specification version 2."""

from __future__ import annotations

from typing import Awaitable, NotRequired, Protocol, TypedDict

from ...json_value.json_value import JSONValue
from ...shared.v2.shared_v2_headers import SharedV2Headers
from .speech_model_v2_call_options import SpeechModelV2CallOptions
from .speech_model_v2_call_warning import SpeechModelV2CallWarning


class SpeechModelV2Response(TypedDict):
  timestamp: object
  modelId: str
  headers: NotRequired[SharedV2Headers]
  body: NotRequired[object]


class SpeechModelV2Request(TypedDict):
  body: NotRequired[object]


class SpeechModelV2Result(TypedDict):
  audio: str | bytes
  warnings: list[SpeechModelV2CallWarning]
  request: NotRequired[SpeechModelV2Request]
  response: SpeechModelV2Response
  providerMetadata: NotRequired[dict[str, dict[str, JSONValue]]]


class SpeechModelV2(Protocol):
  specificationVersion: str
  provider: str
  modelId: str

  def doGenerate(
    self, options: SpeechModelV2CallOptions
  ) -> Awaitable[SpeechModelV2Result]: ...

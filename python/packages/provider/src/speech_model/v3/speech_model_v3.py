"""Speech model specification version 3."""

from __future__ import annotations

from typing import Awaitable, NotRequired, Protocol, TypedDict

from ...json_value.json_value import JSONObject
from ...shared.v2.shared_v2_headers import SharedV2Headers
from ...shared.v3.shared_v3_warning import SharedV3Warning
from .speech_model_v3_call_options import SpeechModelV3CallOptions


class SpeechModelV3Response(TypedDict):
  timestamp: object
  modelId: str
  headers: NotRequired[SharedV2Headers]
  body: NotRequired[object]


class SpeechModelV3Request(TypedDict):
  body: NotRequired[object]


class SpeechModelV3Result(TypedDict):
  audio: str | bytes
  warnings: list[SharedV3Warning]
  request: NotRequired[SpeechModelV3Request]
  response: SpeechModelV3Response
  providerMetadata: NotRequired[dict[str, JSONObject]]


class SpeechModelV3(Protocol):
  specificationVersion: str
  provider: str
  modelId: str

  def doGenerate(
    self, options: SpeechModelV3CallOptions
  ) -> Awaitable[SpeechModelV3Result]: ...

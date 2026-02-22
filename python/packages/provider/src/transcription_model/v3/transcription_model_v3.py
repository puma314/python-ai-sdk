"""Transcription model specification version 3."""

from __future__ import annotations

from typing import Awaitable, NotRequired, Protocol, TypedDict

from ...json_value.json_value import JSONObject
from ...shared.v3.shared_v3_headers import SharedV3Headers
from ...shared.v3.shared_v3_warning import SharedV3Warning
from .transcription_model_v3_call_options import TranscriptionModelV3CallOptions


class TranscriptionModelV3Segment(TypedDict):
  text: str
  startSecond: float
  endSecond: float


class TranscriptionModelV3Request(TypedDict):
  body: NotRequired[str]


class TranscriptionModelV3Response(TypedDict):
  timestamp: object
  modelId: str
  headers: NotRequired[SharedV3Headers]
  body: NotRequired[object]


class TranscriptionModelV3Result(TypedDict):
  text: str
  segments: list[TranscriptionModelV3Segment]
  language: str | None
  durationInSeconds: float | None
  warnings: list[SharedV3Warning]
  request: NotRequired[TranscriptionModelV3Request]
  response: TranscriptionModelV3Response
  providerMetadata: NotRequired[dict[str, JSONObject]]


class TranscriptionModelV3(Protocol):
  specificationVersion: str
  provider: str
  modelId: str

  def doGenerate(
    self, options: TranscriptionModelV3CallOptions
  ) -> Awaitable[TranscriptionModelV3Result]: ...

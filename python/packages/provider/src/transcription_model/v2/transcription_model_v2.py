"""Transcription model specification version 2."""

from __future__ import annotations

from typing import Awaitable, NotRequired, Protocol, TypedDict

from ...json_value.json_value import JSONValue
from ...shared.v2.shared_v2_headers import SharedV2Headers
from .transcription_model_v2_call_options import TranscriptionModelV2CallOptions
from .transcription_model_v2_call_warning import TranscriptionModelV2CallWarning


class TranscriptionModelV2Segment(TypedDict):
  text: str
  startSecond: float
  endSecond: float


class TranscriptionModelV2Request(TypedDict):
  body: NotRequired[str]


class TranscriptionModelV2Response(TypedDict):
  timestamp: object
  modelId: str
  headers: NotRequired[SharedV2Headers]
  body: NotRequired[object]


class TranscriptionModelV2Result(TypedDict):
  text: str
  segments: list[TranscriptionModelV2Segment]
  language: str | None
  durationInSeconds: float | None
  warnings: list[TranscriptionModelV2CallWarning]
  request: NotRequired[TranscriptionModelV2Request]
  response: TranscriptionModelV2Response
  providerMetadata: NotRequired[dict[str, dict[str, JSONValue]]]


class TranscriptionModelV2(Protocol):
  specificationVersion: str
  provider: str
  modelId: str

  def doGenerate(
    self, options: TranscriptionModelV2CallOptions
  ) -> Awaitable[TranscriptionModelV2Result]: ...

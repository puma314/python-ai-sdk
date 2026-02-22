"""Warning types for transcription-model v2."""

from typing import Literal, NotRequired, TypeAlias, TypedDict


class TranscriptionModelV2UnsupportedSettingWarning(TypedDict):
  type: Literal['unsupported-setting']
  setting: str
  details: NotRequired[str]


class TranscriptionModelV2OtherWarning(TypedDict):
  type: Literal['other']
  message: str


TranscriptionModelV2CallWarning: TypeAlias = (
  TranscriptionModelV2UnsupportedSettingWarning
  | TranscriptionModelV2OtherWarning
)

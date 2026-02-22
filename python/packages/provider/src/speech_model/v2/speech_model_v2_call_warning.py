"""Warning types for speech-model v2 calls."""

from typing import Literal, NotRequired, TypeAlias, TypedDict


class SpeechModelV2UnsupportedSettingWarning(TypedDict):
  type: Literal['unsupported-setting']
  setting: str
  details: NotRequired[str]


class SpeechModelV2OtherWarning(TypedDict):
  type: Literal['other']
  message: str


SpeechModelV2CallWarning: TypeAlias = (
  SpeechModelV2UnsupportedSettingWarning | SpeechModelV2OtherWarning
)

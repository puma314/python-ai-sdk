from typing import Literal, NotRequired, TypeAlias, TypedDict


class ImageModelV2UnsupportedSettingWarning(TypedDict):
  type: Literal['unsupported-setting']
  setting: str
  details: NotRequired[str]


class ImageModelV2OtherWarning(TypedDict):
  type: Literal['other']
  message: str


ImageModelV2CallWarning: TypeAlias = (
  ImageModelV2UnsupportedSettingWarning | ImageModelV2OtherWarning
)

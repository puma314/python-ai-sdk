from typing import Literal, NotRequired, TypeAlias, TypedDict

from .language_model_v2_function_tool import LanguageModelV2FunctionTool
from .language_model_v2_provider_defined_tool import (
  LanguageModelV2ProviderDefinedTool,
)


class LanguageModelV2UnsupportedSettingWarning(TypedDict):
  type: Literal['unsupported-setting']
  setting: str
  details: NotRequired[str]


class LanguageModelV2UnsupportedToolWarning(TypedDict):
  type: Literal['unsupported-tool']
  tool: LanguageModelV2FunctionTool | LanguageModelV2ProviderDefinedTool
  details: NotRequired[str]


class LanguageModelV2OtherWarning(TypedDict):
  type: Literal['other']
  message: str


LanguageModelV2CallWarning: TypeAlias = (
  LanguageModelV2UnsupportedSettingWarning
  | LanguageModelV2UnsupportedToolWarning
  | LanguageModelV2OtherWarning
)

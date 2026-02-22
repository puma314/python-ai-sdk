from typing import Literal, TypeAlias, TypedDict


class LanguageModelV2AutoToolChoice(TypedDict):
  type: Literal['auto']


class LanguageModelV2NoToolChoice(TypedDict):
  type: Literal['none']


class LanguageModelV2RequiredToolChoice(TypedDict):
  type: Literal['required']


class LanguageModelV2SpecificToolChoice(TypedDict):
  type: Literal['tool']
  toolName: str


LanguageModelV2ToolChoice: TypeAlias = (
  LanguageModelV2AutoToolChoice
  | LanguageModelV2NoToolChoice
  | LanguageModelV2RequiredToolChoice
  | LanguageModelV2SpecificToolChoice
)

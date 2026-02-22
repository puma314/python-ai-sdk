from typing import Literal, TypeAlias, TypedDict


class LanguageModelV3AutoToolChoice(TypedDict):
  type: Literal['auto']


class LanguageModelV3NoToolChoice(TypedDict):
  type: Literal['none']


class LanguageModelV3RequiredToolChoice(TypedDict):
  type: Literal['required']


class LanguageModelV3SpecificToolChoice(TypedDict):
  type: Literal['tool']
  toolName: str


LanguageModelV3ToolChoice: TypeAlias = (
  LanguageModelV3AutoToolChoice
  | LanguageModelV3NoToolChoice
  | LanguageModelV3RequiredToolChoice
  | LanguageModelV3SpecificToolChoice
)

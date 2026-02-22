from typing import Any, Literal, NotRequired, TypeAlias, TypedDict

from ...json_value.json_value import JSONValue
from ...shared.v2.shared_v2_provider_options import SharedV2ProviderOptions
from .language_model_v2_data_content import LanguageModelV2DataContent


class LanguageModelV2TextPart(TypedDict):
  type: Literal['text']
  text: str
  providerOptions: NotRequired[SharedV2ProviderOptions]


class LanguageModelV2ReasoningPart(TypedDict):
  type: Literal['reasoning']
  text: str
  providerOptions: NotRequired[SharedV2ProviderOptions]


class LanguageModelV2FilePart(TypedDict):
  type: Literal['file']
  filename: NotRequired[str]
  data: LanguageModelV2DataContent
  mediaType: str
  providerOptions: NotRequired[SharedV2ProviderOptions]


class LanguageModelV2ToolResultOutputText(TypedDict):
  type: Literal['text']
  value: str


class LanguageModelV2ToolResultOutputJSON(TypedDict):
  type: Literal['json']
  value: JSONValue


class LanguageModelV2ToolResultOutputErrorText(TypedDict):
  type: Literal['error-text']
  value: str


class LanguageModelV2ToolResultOutputErrorJSON(TypedDict):
  type: Literal['error-json']
  value: JSONValue


class LanguageModelV2ToolResultContentTextPart(TypedDict):
  type: Literal['text']
  text: str


class LanguageModelV2ToolResultContentMediaPart(TypedDict):
  type: Literal['media']
  data: str
  mediaType: str


LanguageModelV2ToolResultContentPart: TypeAlias = (
  LanguageModelV2ToolResultContentTextPart
  | LanguageModelV2ToolResultContentMediaPart
)


class LanguageModelV2ToolResultOutputContent(TypedDict):
  type: Literal['content']
  value: list[LanguageModelV2ToolResultContentPart]


LanguageModelV2ToolResultOutput: TypeAlias = (
  LanguageModelV2ToolResultOutputText
  | LanguageModelV2ToolResultOutputJSON
  | LanguageModelV2ToolResultOutputErrorText
  | LanguageModelV2ToolResultOutputErrorJSON
  | LanguageModelV2ToolResultOutputContent
)


class LanguageModelV2ToolCallPart(TypedDict):
  type: Literal['tool-call']
  toolCallId: str
  toolName: str
  input: Any
  providerExecuted: NotRequired[bool]
  providerOptions: NotRequired[SharedV2ProviderOptions]


class LanguageModelV2ToolResultPart(TypedDict):
  type: Literal['tool-result']
  toolCallId: str
  toolName: str
  output: LanguageModelV2ToolResultOutput
  providerOptions: NotRequired[SharedV2ProviderOptions]


class LanguageModelV2SystemMessage(TypedDict):
  role: Literal['system']
  content: str
  providerOptions: NotRequired[SharedV2ProviderOptions]


class LanguageModelV2UserMessage(TypedDict):
  role: Literal['user']
  content: list[LanguageModelV2TextPart | LanguageModelV2FilePart]
  providerOptions: NotRequired[SharedV2ProviderOptions]


class LanguageModelV2AssistantMessage(TypedDict):
  role: Literal['assistant']
  content: list[
    LanguageModelV2TextPart
    | LanguageModelV2FilePart
    | LanguageModelV2ReasoningPart
    | LanguageModelV2ToolCallPart
    | LanguageModelV2ToolResultPart
  ]
  providerOptions: NotRequired[SharedV2ProviderOptions]


class LanguageModelV2ToolMessage(TypedDict):
  role: Literal['tool']
  content: list[LanguageModelV2ToolResultPart]
  providerOptions: NotRequired[SharedV2ProviderOptions]


LanguageModelV2Message: TypeAlias = (
  LanguageModelV2SystemMessage
  | LanguageModelV2UserMessage
  | LanguageModelV2AssistantMessage
  | LanguageModelV2ToolMessage
)

LanguageModelV2Prompt: TypeAlias = list[LanguageModelV2Message]

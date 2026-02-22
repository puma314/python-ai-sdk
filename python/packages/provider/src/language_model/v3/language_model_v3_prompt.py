from typing import Any, Literal, NotRequired, TypeAlias, TypedDict

from ...json_value.json_value import JSONValue
from ...shared.v3.shared_v3_provider_options import SharedV3ProviderOptions
from .language_model_v3_data_content import LanguageModelV3DataContent


class LanguageModelV3TextPart(TypedDict):
  type: Literal['text']
  text: str
  providerOptions: NotRequired[SharedV3ProviderOptions]


class LanguageModelV3ReasoningPart(TypedDict):
  type: Literal['reasoning']
  text: str
  providerOptions: NotRequired[SharedV3ProviderOptions]


class LanguageModelV3FilePart(TypedDict):
  type: Literal['file']
  filename: NotRequired[str]
  data: LanguageModelV3DataContent
  mediaType: str
  providerOptions: NotRequired[SharedV3ProviderOptions]


class LanguageModelV3ToolResultOutputText(TypedDict):
  type: Literal['text']
  value: str
  providerOptions: NotRequired[SharedV3ProviderOptions]


class LanguageModelV3ToolResultOutputJSON(TypedDict):
  type: Literal['json']
  value: JSONValue
  providerOptions: NotRequired[SharedV3ProviderOptions]


class LanguageModelV3ToolResultOutputExecutionDenied(TypedDict):
  type: Literal['execution-denied']
  reason: NotRequired[str]
  providerOptions: NotRequired[SharedV3ProviderOptions]


class LanguageModelV3ToolResultOutputErrorText(TypedDict):
  type: Literal['error-text']
  value: str
  providerOptions: NotRequired[SharedV3ProviderOptions]


class LanguageModelV3ToolResultOutputErrorJSON(TypedDict):
  type: Literal['error-json']
  value: JSONValue
  providerOptions: NotRequired[SharedV3ProviderOptions]


class LanguageModelV3ToolResultContentTextPart(TypedDict):
  type: Literal['text']
  text: str
  providerOptions: NotRequired[SharedV3ProviderOptions]


class LanguageModelV3ToolResultContentFileDataPart(TypedDict):
  type: Literal['file-data']
  data: str
  mediaType: str
  filename: NotRequired[str]
  providerOptions: NotRequired[SharedV3ProviderOptions]


class LanguageModelV3ToolResultContentFileURLPart(TypedDict):
  type: Literal['file-url']
  url: str
  providerOptions: NotRequired[SharedV3ProviderOptions]


class LanguageModelV3ToolResultContentFileIDPart(TypedDict):
  type: Literal['file-id']
  fileId: str | dict[str, str]
  providerOptions: NotRequired[SharedV3ProviderOptions]


class LanguageModelV3ToolResultContentImageDataPart(TypedDict):
  type: Literal['image-data']
  data: str
  mediaType: str
  providerOptions: NotRequired[SharedV3ProviderOptions]


class LanguageModelV3ToolResultContentImageURLPart(TypedDict):
  type: Literal['image-url']
  url: str
  providerOptions: NotRequired[SharedV3ProviderOptions]


class LanguageModelV3ToolResultContentImageFileIDPart(TypedDict):
  type: Literal['image-file-id']
  fileId: str | dict[str, str]
  providerOptions: NotRequired[SharedV3ProviderOptions]


class LanguageModelV3ToolResultContentCustomPart(TypedDict):
  type: Literal['custom']
  providerOptions: NotRequired[SharedV3ProviderOptions]


LanguageModelV3ToolResultContentPart: TypeAlias = (
  LanguageModelV3ToolResultContentTextPart
  | LanguageModelV3ToolResultContentFileDataPart
  | LanguageModelV3ToolResultContentFileURLPart
  | LanguageModelV3ToolResultContentFileIDPart
  | LanguageModelV3ToolResultContentImageDataPart
  | LanguageModelV3ToolResultContentImageURLPart
  | LanguageModelV3ToolResultContentImageFileIDPart
  | LanguageModelV3ToolResultContentCustomPart
)


class LanguageModelV3ToolResultOutputContent(TypedDict):
  type: Literal['content']
  value: list[LanguageModelV3ToolResultContentPart]


LanguageModelV3ToolResultOutput: TypeAlias = (
  LanguageModelV3ToolResultOutputText
  | LanguageModelV3ToolResultOutputJSON
  | LanguageModelV3ToolResultOutputExecutionDenied
  | LanguageModelV3ToolResultOutputErrorText
  | LanguageModelV3ToolResultOutputErrorJSON
  | LanguageModelV3ToolResultOutputContent
)


class LanguageModelV3ToolCallPart(TypedDict):
  type: Literal['tool-call']
  toolCallId: str
  toolName: str
  input: Any
  providerExecuted: NotRequired[bool]
  providerOptions: NotRequired[SharedV3ProviderOptions]


class LanguageModelV3ToolResultPart(TypedDict):
  type: Literal['tool-result']
  toolCallId: str
  toolName: str
  output: LanguageModelV3ToolResultOutput
  providerOptions: NotRequired[SharedV3ProviderOptions]


class LanguageModelV3ToolApprovalResponsePart(TypedDict):
  type: Literal['tool-approval-response']
  approvalId: str
  approved: bool
  reason: NotRequired[str]
  providerOptions: NotRequired[SharedV3ProviderOptions]


class LanguageModelV3SystemMessage(TypedDict):
  role: Literal['system']
  content: str
  providerOptions: NotRequired[SharedV3ProviderOptions]


class LanguageModelV3UserMessage(TypedDict):
  role: Literal['user']
  content: list[LanguageModelV3TextPart | LanguageModelV3FilePart]
  providerOptions: NotRequired[SharedV3ProviderOptions]


class LanguageModelV3AssistantMessage(TypedDict):
  role: Literal['assistant']
  content: list[
    LanguageModelV3TextPart
    | LanguageModelV3FilePart
    | LanguageModelV3ReasoningPart
    | LanguageModelV3ToolCallPart
    | LanguageModelV3ToolResultPart
  ]
  providerOptions: NotRequired[SharedV3ProviderOptions]


class LanguageModelV3ToolMessage(TypedDict):
  role: Literal['tool']
  content: list[
    LanguageModelV3ToolResultPart | LanguageModelV3ToolApprovalResponsePart
  ]
  providerOptions: NotRequired[SharedV3ProviderOptions]


LanguageModelV3Message: TypeAlias = (
  LanguageModelV3SystemMessage
  | LanguageModelV3UserMessage
  | LanguageModelV3AssistantMessage
  | LanguageModelV3ToolMessage
)

LanguageModelV3Prompt: TypeAlias = list[LanguageModelV3Message]

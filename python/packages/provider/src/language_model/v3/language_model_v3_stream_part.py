from typing import Any, Literal, NotRequired, TypeAlias, TypedDict

from ...shared.v3.shared_v3_provider_metadata import SharedV3ProviderMetadata
from ...shared.v3.shared_v3_warning import SharedV3Warning
from .language_model_v3_file import LanguageModelV3File
from .language_model_v3_finish_reason import LanguageModelV3FinishReason
from .language_model_v3_response_metadata import LanguageModelV3ResponseMetadata
from .language_model_v3_source import LanguageModelV3Source
from .language_model_v3_tool_approval_request import (
  LanguageModelV3ToolApprovalRequest,
)
from .language_model_v3_tool_call import LanguageModelV3ToolCall
from .language_model_v3_tool_result import LanguageModelV3ToolResult
from .language_model_v3_usage import LanguageModelV3Usage


class LanguageModelV3TextStartPart(TypedDict):
  type: Literal['text-start']
  id: str
  providerMetadata: NotRequired[SharedV3ProviderMetadata]


class LanguageModelV3TextDeltaPart(TypedDict):
  type: Literal['text-delta']
  id: str
  delta: str
  providerMetadata: NotRequired[SharedV3ProviderMetadata]


class LanguageModelV3TextEndPart(TypedDict):
  type: Literal['text-end']
  id: str
  providerMetadata: NotRequired[SharedV3ProviderMetadata]


class LanguageModelV3ReasoningStartPart(TypedDict):
  type: Literal['reasoning-start']
  id: str
  providerMetadata: NotRequired[SharedV3ProviderMetadata]


class LanguageModelV3ReasoningDeltaPart(TypedDict):
  type: Literal['reasoning-delta']
  id: str
  delta: str
  providerMetadata: NotRequired[SharedV3ProviderMetadata]


class LanguageModelV3ReasoningEndPart(TypedDict):
  type: Literal['reasoning-end']
  id: str
  providerMetadata: NotRequired[SharedV3ProviderMetadata]


class LanguageModelV3ToolInputStartPart(TypedDict):
  type: Literal['tool-input-start']
  id: str
  toolName: str
  providerMetadata: NotRequired[SharedV3ProviderMetadata]
  providerExecuted: NotRequired[bool]
  dynamic: NotRequired[bool]
  title: NotRequired[str]


class LanguageModelV3ToolInputDeltaPart(TypedDict):
  type: Literal['tool-input-delta']
  id: str
  delta: str
  providerMetadata: NotRequired[SharedV3ProviderMetadata]


class LanguageModelV3ToolInputEndPart(TypedDict):
  type: Literal['tool-input-end']
  id: str
  providerMetadata: NotRequired[SharedV3ProviderMetadata]


class LanguageModelV3StreamStartPart(TypedDict):
  type: Literal['stream-start']
  warnings: list[SharedV3Warning]


class LanguageModelV3ResponseMetadataPart(LanguageModelV3ResponseMetadata):
  type: Literal['response-metadata']


class LanguageModelV3FinishPart(TypedDict):
  type: Literal['finish']
  usage: LanguageModelV3Usage
  finishReason: LanguageModelV3FinishReason
  providerMetadata: NotRequired[SharedV3ProviderMetadata]


class LanguageModelV3RawPart(TypedDict):
  type: Literal['raw']
  rawValue: Any


class LanguageModelV3ErrorPart(TypedDict):
  type: Literal['error']
  error: Any


LanguageModelV3StreamPart: TypeAlias = (
  LanguageModelV3TextStartPart
  | LanguageModelV3TextDeltaPart
  | LanguageModelV3TextEndPart
  | LanguageModelV3ReasoningStartPart
  | LanguageModelV3ReasoningDeltaPart
  | LanguageModelV3ReasoningEndPart
  | LanguageModelV3ToolInputStartPart
  | LanguageModelV3ToolInputDeltaPart
  | LanguageModelV3ToolInputEndPart
  | LanguageModelV3ToolApprovalRequest
  | LanguageModelV3ToolCall
  | LanguageModelV3ToolResult
  | LanguageModelV3File
  | LanguageModelV3Source
  | LanguageModelV3StreamStartPart
  | LanguageModelV3ResponseMetadataPart
  | LanguageModelV3FinishPart
  | LanguageModelV3RawPart
  | LanguageModelV3ErrorPart
)

from typing import Any, Literal, NotRequired, TypeAlias, TypedDict

from ...shared.v2.shared_v2_provider_metadata import SharedV2ProviderMetadata
from .language_model_v2_call_warning import LanguageModelV2CallWarning
from .language_model_v2_file import LanguageModelV2File
from .language_model_v2_finish_reason import LanguageModelV2FinishReason
from .language_model_v2_response_metadata import LanguageModelV2ResponseMetadata
from .language_model_v2_source import LanguageModelV2Source
from .language_model_v2_tool_call import LanguageModelV2ToolCall
from .language_model_v2_tool_result import LanguageModelV2ToolResult
from .language_model_v2_usage import LanguageModelV2Usage


class LanguageModelV2TextStartPart(TypedDict):
  type: Literal['text-start']
  id: str
  providerMetadata: NotRequired[SharedV2ProviderMetadata]


class LanguageModelV2TextDeltaPart(TypedDict):
  type: Literal['text-delta']
  id: str
  delta: str
  providerMetadata: NotRequired[SharedV2ProviderMetadata]


class LanguageModelV2TextEndPart(TypedDict):
  type: Literal['text-end']
  id: str
  providerMetadata: NotRequired[SharedV2ProviderMetadata]


class LanguageModelV2ReasoningStartPart(TypedDict):
  type: Literal['reasoning-start']
  id: str
  providerMetadata: NotRequired[SharedV2ProviderMetadata]


class LanguageModelV2ReasoningDeltaPart(TypedDict):
  type: Literal['reasoning-delta']
  id: str
  delta: str
  providerMetadata: NotRequired[SharedV2ProviderMetadata]


class LanguageModelV2ReasoningEndPart(TypedDict):
  type: Literal['reasoning-end']
  id: str
  providerMetadata: NotRequired[SharedV2ProviderMetadata]


class LanguageModelV2ToolInputStartPart(TypedDict):
  type: Literal['tool-input-start']
  id: str
  toolName: str
  providerExecuted: NotRequired[bool]
  providerMetadata: NotRequired[SharedV2ProviderMetadata]


class LanguageModelV2ToolInputDeltaPart(TypedDict):
  type: Literal['tool-input-delta']
  id: str
  delta: str
  providerMetadata: NotRequired[SharedV2ProviderMetadata]


class LanguageModelV2ToolInputEndPart(TypedDict):
  type: Literal['tool-input-end']
  id: str
  providerMetadata: NotRequired[SharedV2ProviderMetadata]


class LanguageModelV2StreamStartPart(TypedDict):
  type: Literal['stream-start']
  warnings: list[LanguageModelV2CallWarning]


class LanguageModelV2ResponseMetadataPart(LanguageModelV2ResponseMetadata):
  type: Literal['response-metadata']


class LanguageModelV2FinishPart(TypedDict):
  type: Literal['finish']
  usage: LanguageModelV2Usage
  finishReason: LanguageModelV2FinishReason
  providerMetadata: NotRequired[SharedV2ProviderMetadata]


class LanguageModelV2RawPart(TypedDict):
  type: Literal['raw']
  rawValue: Any


class LanguageModelV2ErrorPart(TypedDict):
  type: Literal['error']
  error: Any


LanguageModelV2StreamPart: TypeAlias = (
  LanguageModelV2TextStartPart
  | LanguageModelV2TextDeltaPart
  | LanguageModelV2TextEndPart
  | LanguageModelV2ReasoningStartPart
  | LanguageModelV2ReasoningDeltaPart
  | LanguageModelV2ReasoningEndPart
  | LanguageModelV2ToolInputStartPart
  | LanguageModelV2ToolInputDeltaPart
  | LanguageModelV2ToolInputEndPart
  | LanguageModelV2ToolCall
  | LanguageModelV2ToolResult
  | LanguageModelV2File
  | LanguageModelV2Source
  | LanguageModelV2StreamStartPart
  | LanguageModelV2ResponseMetadataPart
  | LanguageModelV2FinishPart
  | LanguageModelV2RawPart
  | LanguageModelV2ErrorPart
)

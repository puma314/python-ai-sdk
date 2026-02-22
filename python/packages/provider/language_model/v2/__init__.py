from __future__ import annotations
"""Language model v2 public API.

Translated from: packages/provider/src/language-model/v2/index.ts
"""

from .language_model_v2 import (
    LanguageModelV2,
    LanguageModelV2GenerateRequest,
    LanguageModelV2GenerateResponse,
    LanguageModelV2GenerateResult,
    LanguageModelV2StreamRequest,
    LanguageModelV2StreamResponse,
    LanguageModelV2StreamResult,
)
from .language_model_v2_call_options import (
    JSONResponseFormat,
    LanguageModelV2CallOptions,
    LanguageModelV2ResponseFormat,
    TextResponseFormat,
)
from .language_model_v2_call_warning import (
    LanguageModelV2CallOptionKey,
    LanguageModelV2CallWarning,
    OtherWarning,
    UnsupportedSettingWarning,
    UnsupportedToolWarning,
)
from .language_model_v2_content import LanguageModelV2Content
from .language_model_v2_data_content import LanguageModelV2DataContent
from .language_model_v2_file import LanguageModelV2File
from .language_model_v2_finish_reason import LanguageModelV2FinishReason
from .language_model_v2_function_tool import LanguageModelV2FunctionTool
from .language_model_v2_prompt import (
    LanguageModelV2AssistantMessage,
    LanguageModelV2FilePart,
    LanguageModelV2Message,
    LanguageModelV2Prompt,
    LanguageModelV2ReasoningPart,
    LanguageModelV2SystemMessage,
    LanguageModelV2TextPart,
    LanguageModelV2ToolCallPart,
    LanguageModelV2ToolMessage,
    LanguageModelV2ToolResultContentMedia,
    LanguageModelV2ToolResultContentOutput,
    LanguageModelV2ToolResultContentText,
    LanguageModelV2ToolResultErrorJsonOutput,
    LanguageModelV2ToolResultErrorTextOutput,
    LanguageModelV2ToolResultJsonOutput,
    LanguageModelV2ToolResultOutput,
    LanguageModelV2ToolResultPart,
    LanguageModelV2ToolResultTextOutput,
    LanguageModelV2UserMessage,
)
from .language_model_v2_provider_defined_tool import LanguageModelV2ProviderDefinedTool
from .language_model_v2_reasoning import LanguageModelV2Reasoning
from .language_model_v2_response_metadata import LanguageModelV2ResponseMetadata
from .language_model_v2_source import (
    LanguageModelV2DocumentSource,
    LanguageModelV2Source,
    LanguageModelV2UrlSource,
)
from .language_model_v2_stream_part import (
    LanguageModelV2Error,
    LanguageModelV2Finish,
    LanguageModelV2Raw,
    LanguageModelV2ReasoningDelta,
    LanguageModelV2ReasoningEnd,
    LanguageModelV2ReasoningStart,
    LanguageModelV2ResponseMetadataPart,
    LanguageModelV2StreamPart,
    LanguageModelV2StreamStart,
    LanguageModelV2TextDelta,
    LanguageModelV2TextEnd,
    LanguageModelV2TextStart,
    LanguageModelV2ToolInputDelta,
    LanguageModelV2ToolInputEnd,
    LanguageModelV2ToolInputStart,
)
from .language_model_v2_text import LanguageModelV2Text
from .language_model_v2_tool_call import LanguageModelV2ToolCall
from .language_model_v2_tool_choice import (
    AutoToolChoice,
    LanguageModelV2ToolChoice,
    NoneToolChoice,
    RequiredToolChoice,
    SpecificToolChoice,
)
from .language_model_v2_usage import LanguageModelV2Usage

__all__ = [
    # language_model_v2
    "LanguageModelV2",
    "LanguageModelV2GenerateRequest",
    "LanguageModelV2GenerateResponse",
    "LanguageModelV2GenerateResult",
    "LanguageModelV2StreamRequest",
    "LanguageModelV2StreamResponse",
    "LanguageModelV2StreamResult",
    # language_model_v2_call_options
    "JSONResponseFormat",
    "LanguageModelV2CallOptions",
    "LanguageModelV2ResponseFormat",
    "TextResponseFormat",
    # language_model_v2_call_warning
    "LanguageModelV2CallOptionKey",
    "LanguageModelV2CallWarning",
    "OtherWarning",
    "UnsupportedSettingWarning",
    "UnsupportedToolWarning",
    # language_model_v2_content
    "LanguageModelV2Content",
    # language_model_v2_data_content
    "LanguageModelV2DataContent",
    # language_model_v2_file
    "LanguageModelV2File",
    # language_model_v2_finish_reason
    "LanguageModelV2FinishReason",
    # language_model_v2_function_tool
    "LanguageModelV2FunctionTool",
    # language_model_v2_prompt
    "LanguageModelV2AssistantMessage",
    "LanguageModelV2FilePart",
    "LanguageModelV2Message",
    "LanguageModelV2Prompt",
    "LanguageModelV2ReasoningPart",
    "LanguageModelV2SystemMessage",
    "LanguageModelV2TextPart",
    "LanguageModelV2ToolCallPart",
    "LanguageModelV2ToolMessage",
    "LanguageModelV2ToolResultContentMedia",
    "LanguageModelV2ToolResultContentOutput",
    "LanguageModelV2ToolResultContentText",
    "LanguageModelV2ToolResultErrorJsonOutput",
    "LanguageModelV2ToolResultErrorTextOutput",
    "LanguageModelV2ToolResultJsonOutput",
    "LanguageModelV2ToolResultOutput",
    "LanguageModelV2ToolResultPart",
    "LanguageModelV2ToolResultTextOutput",
    "LanguageModelV2UserMessage",
    # language_model_v2_provider_defined_tool
    "LanguageModelV2ProviderDefinedTool",
    # language_model_v2_reasoning
    "LanguageModelV2Reasoning",
    # language_model_v2_response_metadata
    "LanguageModelV2ResponseMetadata",
    # language_model_v2_source
    "LanguageModelV2DocumentSource",
    "LanguageModelV2Source",
    "LanguageModelV2UrlSource",
    # language_model_v2_stream_part
    "LanguageModelV2Error",
    "LanguageModelV2Finish",
    "LanguageModelV2Raw",
    "LanguageModelV2ReasoningDelta",
    "LanguageModelV2ReasoningEnd",
    "LanguageModelV2ReasoningStart",
    "LanguageModelV2ResponseMetadataPart",
    "LanguageModelV2StreamPart",
    "LanguageModelV2StreamStart",
    "LanguageModelV2TextDelta",
    "LanguageModelV2TextEnd",
    "LanguageModelV2TextStart",
    "LanguageModelV2ToolInputDelta",
    "LanguageModelV2ToolInputEnd",
    "LanguageModelV2ToolInputStart",
    # language_model_v2_text
    "LanguageModelV2Text",
    # language_model_v2_tool_call
    "LanguageModelV2ToolCall",
    # language_model_v2_tool_choice
    "AutoToolChoice",
    "LanguageModelV2ToolChoice",
    "NoneToolChoice",
    "RequiredToolChoice",
    "SpecificToolChoice",
    # language_model_v2_usage
    "LanguageModelV2Usage",
]

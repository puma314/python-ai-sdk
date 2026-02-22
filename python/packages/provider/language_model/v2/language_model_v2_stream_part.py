from __future__ import annotations

"""Language model v2 stream part types.

Translated from: packages/provider/src/language-model/v2/language-model-v2-stream-part.ts
"""

from dataclasses import dataclass, field
from typing import Any, Literal, Union

from ...shared.v2.shared_v2_provider_metadata import SharedV2ProviderMetadata
from .language_model_v2_call_warning import LanguageModelV2CallWarning
from .language_model_v2_file import LanguageModelV2File
from .language_model_v2_finish_reason import LanguageModelV2FinishReason
from .language_model_v2_source import LanguageModelV2Source
from .language_model_v2_tool_call import LanguageModelV2ToolCall
from .language_model_v2_tool_result import LanguageModelV2ToolResult
from .language_model_v2_usage import LanguageModelV2Usage


# Text blocks:


@dataclass(frozen=True)
class LanguageModelV2TextStart:
    """Text start stream part."""

    type: Literal['text-start'] = 'text-start'
    id: str = ''
    provider_metadata: SharedV2ProviderMetadata | None = None


@dataclass(frozen=True)
class LanguageModelV2TextDelta:
    """Text delta stream part."""

    type: Literal['text-delta'] = 'text-delta'
    id: str = ''
    delta: str = ''
    provider_metadata: SharedV2ProviderMetadata | None = None


@dataclass(frozen=True)
class LanguageModelV2TextEnd:
    """Text end stream part."""

    type: Literal['text-end'] = 'text-end'
    id: str = ''
    provider_metadata: SharedV2ProviderMetadata | None = None


# Reasoning blocks:


@dataclass(frozen=True)
class LanguageModelV2ReasoningStart:
    """Reasoning start stream part."""

    type: Literal['reasoning-start'] = 'reasoning-start'
    id: str = ''
    provider_metadata: SharedV2ProviderMetadata | None = None


@dataclass(frozen=True)
class LanguageModelV2ReasoningDelta:
    """Reasoning delta stream part."""

    type: Literal['reasoning-delta'] = 'reasoning-delta'
    id: str = ''
    delta: str = ''
    provider_metadata: SharedV2ProviderMetadata | None = None


@dataclass(frozen=True)
class LanguageModelV2ReasoningEnd:
    """Reasoning end stream part."""

    type: Literal['reasoning-end'] = 'reasoning-end'
    id: str = ''
    provider_metadata: SharedV2ProviderMetadata | None = None


# Tool calls and results:


@dataclass(frozen=True)
class LanguageModelV2ToolInputStart:
    """Tool input start stream part."""

    type: Literal['tool-input-start'] = 'tool-input-start'
    id: str = ''
    tool_name: str = ''
    provider_metadata: SharedV2ProviderMetadata | None = None
    provider_executed: bool | None = None


@dataclass(frozen=True)
class LanguageModelV2ToolInputDelta:
    """Tool input delta stream part."""

    type: Literal['tool-input-delta'] = 'tool-input-delta'
    id: str = ''
    delta: str = ''
    provider_metadata: SharedV2ProviderMetadata | None = None


@dataclass(frozen=True)
class LanguageModelV2ToolInputEnd:
    """Tool input end stream part."""

    type: Literal['tool-input-end'] = 'tool-input-end'
    id: str = ''
    provider_metadata: SharedV2ProviderMetadata | None = None


# Files and sources:
# (LanguageModelV2File and LanguageModelV2Source are imported directly)


# stream start event with warnings for the call, e.g. unsupported settings:


@dataclass(frozen=True)
class LanguageModelV2StreamStart:
    """Stream start event with warnings for the call, e.g. unsupported settings."""

    type: Literal['stream-start'] = 'stream-start'
    warnings: list[LanguageModelV2CallWarning] = field(default_factory=list)


# metadata for the response.
# separate stream part so it can be sent once it is available.


@dataclass(frozen=True)
class LanguageModelV2ResponseMetadataPart:
    """Metadata for the response.

    Separate stream part so it can be sent once it is available.
    """

    type: Literal['response-metadata'] = 'response-metadata'
    id: str | None = None
    """ID for the generated response, if the provider sends one."""

    timestamp: Any | None = None
    """Timestamp for the start of the generated response, if the provider sends one."""

    model_id: str | None = None
    """The ID of the response model that was used to generate the response, if the provider sends one."""


# metadata that is available after the stream is finished:


@dataclass(frozen=True)
class LanguageModelV2Finish:
    """Metadata that is available after the stream is finished."""

    type: Literal['finish'] = 'finish'
    usage: LanguageModelV2Usage = field(default_factory=LanguageModelV2Usage)
    finish_reason: LanguageModelV2FinishReason | None = None
    provider_metadata: SharedV2ProviderMetadata | None = None


# raw chunks if enabled


@dataclass(frozen=True)
class LanguageModelV2Raw:
    """Raw chunks if enabled."""

    type: Literal['raw'] = 'raw'
    raw_value: Any = None


# error parts are streamed, allowing for multiple errors


@dataclass(frozen=True)
class LanguageModelV2Error:
    """Error parts are streamed, allowing for multiple errors."""

    type: Literal['error'] = 'error'
    error: Any = None


LanguageModelV2StreamPart = Union[
    LanguageModelV2TextStart,
    LanguageModelV2TextDelta,
    LanguageModelV2TextEnd,
    LanguageModelV2ReasoningStart,
    LanguageModelV2ReasoningDelta,
    LanguageModelV2ReasoningEnd,
    LanguageModelV2ToolInputStart,
    LanguageModelV2ToolInputDelta,
    LanguageModelV2ToolInputEnd,
    LanguageModelV2ToolCall,
    LanguageModelV2ToolResult,
    LanguageModelV2File,
    LanguageModelV2Source,
    LanguageModelV2StreamStart,
    LanguageModelV2ResponseMetadataPart,
    LanguageModelV2Finish,
    LanguageModelV2Raw,
    LanguageModelV2Error,
]

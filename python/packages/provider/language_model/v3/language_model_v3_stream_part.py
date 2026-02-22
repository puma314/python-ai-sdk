from __future__ import annotations

"""Language model v3 stream part types.

Translated from: packages/provider/src/language-model/v3/language-model-v3-stream-part.ts
"""

from dataclasses import dataclass, field
from typing import Any, Literal, Union

from ...shared.v3.shared_v3_provider_metadata import SharedV3ProviderMetadata
from ...shared.v3.shared_v3_warning import SharedV3Warning
from .language_model_v3_file import LanguageModelV3File
from .language_model_v3_finish_reason import LanguageModelV3FinishReason
from .language_model_v3_response_metadata import LanguageModelV3ResponseMetadata
from .language_model_v3_source import LanguageModelV3Source
from .language_model_v3_tool_approval_request import LanguageModelV3ToolApprovalRequest
from .language_model_v3_tool_call import LanguageModelV3ToolCall
from .language_model_v3_tool_result import LanguageModelV3ToolResult
from .language_model_v3_usage import LanguageModelV3Usage


# Text blocks:


@dataclass(frozen=True)
class LanguageModelV3TextStart:
    """Text start stream part."""

    type: Literal['text-start'] = 'text-start'
    id: str = ''
    provider_metadata: SharedV3ProviderMetadata | None = None


@dataclass(frozen=True)
class LanguageModelV3TextDelta:
    """Text delta stream part."""

    type: Literal['text-delta'] = 'text-delta'
    id: str = ''
    delta: str = ''
    provider_metadata: SharedV3ProviderMetadata | None = None


@dataclass(frozen=True)
class LanguageModelV3TextEnd:
    """Text end stream part."""

    type: Literal['text-end'] = 'text-end'
    id: str = ''
    provider_metadata: SharedV3ProviderMetadata | None = None


# Reasoning blocks:


@dataclass(frozen=True)
class LanguageModelV3ReasoningStart:
    """Reasoning start stream part."""

    type: Literal['reasoning-start'] = 'reasoning-start'
    id: str = ''
    provider_metadata: SharedV3ProviderMetadata | None = None


@dataclass(frozen=True)
class LanguageModelV3ReasoningDelta:
    """Reasoning delta stream part."""

    type: Literal['reasoning-delta'] = 'reasoning-delta'
    id: str = ''
    delta: str = ''
    provider_metadata: SharedV3ProviderMetadata | None = None


@dataclass(frozen=True)
class LanguageModelV3ReasoningEnd:
    """Reasoning end stream part."""

    type: Literal['reasoning-end'] = 'reasoning-end'
    id: str = ''
    provider_metadata: SharedV3ProviderMetadata | None = None


# Tool calls and results:


@dataclass(frozen=True)
class LanguageModelV3ToolInputStart:
    """Tool input start stream part."""

    type: Literal['tool-input-start'] = 'tool-input-start'
    id: str = ''
    tool_name: str = ''
    provider_metadata: SharedV3ProviderMetadata | None = None
    provider_executed: bool | None = None
    dynamic: bool | None = None
    title: str | None = None


@dataclass(frozen=True)
class LanguageModelV3ToolInputDelta:
    """Tool input delta stream part."""

    type: Literal['tool-input-delta'] = 'tool-input-delta'
    id: str = ''
    delta: str = ''
    provider_metadata: SharedV3ProviderMetadata | None = None


@dataclass(frozen=True)
class LanguageModelV3ToolInputEnd:
    """Tool input end stream part."""

    type: Literal['tool-input-end'] = 'tool-input-end'
    id: str = ''
    provider_metadata: SharedV3ProviderMetadata | None = None


# stream start event with warnings for the call, e.g. unsupported settings:


@dataclass(frozen=True)
class LanguageModelV3StreamStart:
    """Stream start event with warnings for the call, e.g. unsupported settings."""

    type: Literal['stream-start'] = 'stream-start'
    warnings: list[SharedV3Warning] = field(default_factory=list)


# metadata for the response.
# separate stream part so it can be sent once it is available.


@dataclass(frozen=True)
class LanguageModelV3ResponseMetadataPart:
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
class LanguageModelV3Finish:
    """Metadata that is available after the stream is finished."""

    type: Literal['finish'] = 'finish'
    usage: LanguageModelV3Usage = field(default_factory=LanguageModelV3Usage)
    finish_reason: LanguageModelV3FinishReason | None = None
    provider_metadata: SharedV3ProviderMetadata | None = None


# raw chunks if enabled


@dataclass(frozen=True)
class LanguageModelV3Raw:
    """Raw chunks if enabled."""

    type: Literal['raw'] = 'raw'
    raw_value: Any = None


# error parts are streamed, allowing for multiple errors


@dataclass(frozen=True)
class LanguageModelV3Error:
    """Error parts are streamed, allowing for multiple errors."""

    type: Literal['error'] = 'error'
    error: Any = None


LanguageModelV3StreamPart = Union[
    LanguageModelV3TextStart,
    LanguageModelV3TextDelta,
    LanguageModelV3TextEnd,
    LanguageModelV3ReasoningStart,
    LanguageModelV3ReasoningDelta,
    LanguageModelV3ReasoningEnd,
    LanguageModelV3ToolInputStart,
    LanguageModelV3ToolInputDelta,
    LanguageModelV3ToolInputEnd,
    LanguageModelV3ToolApprovalRequest,
    LanguageModelV3ToolCall,
    LanguageModelV3ToolResult,
    LanguageModelV3File,
    LanguageModelV3Source,
    LanguageModelV3StreamStart,
    LanguageModelV3ResponseMetadataPart,
    LanguageModelV3Finish,
    LanguageModelV3Raw,
    LanguageModelV3Error,
]

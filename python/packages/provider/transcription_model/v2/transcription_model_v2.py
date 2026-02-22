from __future__ import annotations

"""Transcription model specification version 2.

Translated from: packages/provider/src/transcription-model/v2/transcription-model-v2.ts
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Awaitable, Literal, Protocol, runtime_checkable

from ...json_value.json_value import JSONValue
from ...shared.v2.shared_v2_headers import SharedV2Headers
from .transcription_model_v2_call_options import TranscriptionModelV2CallOptions
from .transcription_model_v2_call_warning import TranscriptionModelV2CallWarning


@dataclass(frozen=True)
class TranscriptionModelV2Segment:
    """A segment of transcribed text with timing information."""

    text: str
    """The text content of this segment."""

    start_second: float
    """The start time of this segment in seconds."""

    end_second: float
    """The end time of this segment in seconds."""


@dataclass(frozen=True)
class TranscriptionModelV2RequestInfo:
    """Optional request information for telemetry and debugging purposes."""

    body: str | None = None
    """Raw request HTTP body that was sent to the provider API as a string
    (JSON should be stringified). Non-HTTP(s) providers should not set this."""


@dataclass(frozen=True)
class TranscriptionModelV2ResponseInfo:
    """Response information for telemetry and debugging purposes."""

    timestamp: datetime
    """Timestamp for the start of the generated response."""

    model_id: str
    """The ID of the response model that was used to generate the response."""

    headers: SharedV2Headers | None = None
    """Response headers."""

    body: Any = None
    """Response body."""


@dataclass(frozen=True)
class TranscriptionModelV2Result:
    """Result of a transcription model v2 call."""

    text: str
    """The complete transcribed text from the audio."""

    segments: list[TranscriptionModelV2Segment]
    """Array of transcript segments with timing information.
    Each segment represents a portion of the transcribed text with start and end times."""

    language: str | None
    """The detected language of the audio content, as an ISO-639-1 code (e.g., 'en' for English).
    May be None if the language couldn't be detected."""

    duration_in_seconds: float | None
    """The total duration of the audio file in seconds.
    May be None if the duration couldn't be determined."""

    warnings: list[TranscriptionModelV2CallWarning]
    """Warnings for the call, e.g. unsupported settings."""

    response: TranscriptionModelV2ResponseInfo
    """Response information for telemetry and debugging purposes."""

    request: TranscriptionModelV2RequestInfo | None = None
    """Optional request information for telemetry and debugging purposes."""

    provider_metadata: dict[str, dict[str, JSONValue]] | None = None
    """Additional provider-specific metadata. They are passed through
    from the provider to the AI SDK and enable provider-specific
    results that can be fully encapsulated in the provider."""


@runtime_checkable
class TranscriptionModelV2(Protocol):
    """Transcription model specification version 2."""

    @property
    def specification_version(self) -> Literal['v2']:
        """The transcription model must specify which transcription model interface
        version it implements. This will allow us to evolve the transcription
        model interface and retain backwards compatibility. The different
        implementation versions can be handled as a discriminated union
        on our side."""
        ...

    @property
    def provider(self) -> str:
        """Name of the provider for logging purposes."""
        ...

    @property
    def model_id(self) -> str:
        """Provider-specific model ID for logging purposes."""
        ...

    def do_generate(
        self, options: TranscriptionModelV2CallOptions
    ) -> Awaitable[TranscriptionModelV2Result]:
        """Generates a transcript."""
        ...

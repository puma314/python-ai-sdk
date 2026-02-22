from __future__ import annotations
"""Speech model specification version 2.

Translated from: packages/provider/src/speech-model/v2/speech-model-v2.ts
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Awaitable, Protocol, runtime_checkable

from ...json_value.json_value import JSONValue
from ...shared.v2.shared_v2_headers import SharedV2Headers
from .speech_model_v2_call_options import SpeechModelV2CallOptions
from .speech_model_v2_call_warning import SpeechModelV2CallWarning


@dataclass(frozen=True)
class SpeechModelV2RequestInfo:
    """Optional request information for telemetry and debugging purposes."""

    body: Any = None
    """Response body (available only for providers that use HTTP requests)."""


@dataclass(frozen=True)
class SpeechModelV2ResponseInfo:
    """Response information for telemetry and debugging purposes."""

    timestamp: datetime = field(default_factory=datetime.now)
    """Timestamp for the start of the generated response."""

    model_id: str = ''
    """The ID of the response model that was used to generate the response."""

    headers: SharedV2Headers | None = None
    """Response headers."""

    body: Any = None
    """Response body."""


@dataclass(frozen=True)
class SpeechModelV2GenerateResult:
    """Result of a speech model V2 generate call."""

    audio: str | bytes = b''
    """Generated audio.

    The audio should be returned without any unnecessary conversion.
    If the API returns base64 encoded strings, the audio should be returned
    as base64 encoded strings. If the API returns binary data, the audio
    should be returned as binary data.
    """

    warnings: list[SpeechModelV2CallWarning] = field(default_factory=list)
    """Warnings for the call, e.g. unsupported settings."""

    request: SpeechModelV2RequestInfo | None = None
    """Optional request information for telemetry and debugging purposes."""

    response: SpeechModelV2ResponseInfo = field(default_factory=SpeechModelV2ResponseInfo)
    """Response information for telemetry and debugging purposes."""

    provider_metadata: dict[str, dict[str, JSONValue]] | None = None
    """Additional provider-specific metadata. They are passed through
    from the provider to the AI SDK and enable provider-specific
    results that can be fully encapsulated in the provider.
    """


@runtime_checkable
class SpeechModelV2(Protocol):
    """Speech model specification version 2.

    The speech model must specify which speech model interface
    version it implements. This will allow us to evolve the speech
    model interface and retain backwards compatibility. The different
    implementation versions can be handled as a discriminated union
    on our side.
    """

    @property
    def specification_version(self) -> str:
        """The speech model must specify which speech model interface
        version it implements. This will allow us to evolve the speech
        model interface and retain backwards compatibility. The different
        implementation versions can be handled as a discriminated union
        on our side.
        """
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
        self, options: SpeechModelV2CallOptions
    ) -> Awaitable[SpeechModelV2GenerateResult]:
        """Generates speech audio from text."""
        ...

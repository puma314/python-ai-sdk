from __future__ import annotations

"""Specification for a language model that implements the language model interface version 2.

Translated from: packages/provider/src/language-model/v2/language-model-v2.ts
"""

import re
from collections.abc import AsyncIterator, Awaitable
from dataclasses import dataclass, field
from typing import Any, Literal, Protocol, runtime_checkable

from ...shared.v2.shared_v2_headers import SharedV2Headers
from ...shared.v2.shared_v2_provider_metadata import SharedV2ProviderMetadata
from .language_model_v2_call_options import LanguageModelV2CallOptions
from .language_model_v2_call_warning import LanguageModelV2CallWarning
from .language_model_v2_content import LanguageModelV2Content
from .language_model_v2_finish_reason import LanguageModelV2FinishReason
from .language_model_v2_response_metadata import LanguageModelV2ResponseMetadata
from .language_model_v2_stream_part import LanguageModelV2StreamPart
from .language_model_v2_usage import LanguageModelV2Usage


@dataclass(frozen=True)
class LanguageModelV2GenerateRequest:
    """Optional request information for telemetry and debugging purposes."""

    body: Any = None
    """Request HTTP body that was sent to the provider API."""


@dataclass(frozen=True)
class LanguageModelV2GenerateResponse:
    """Optional response information for telemetry and debugging purposes."""

    id: str | None = None
    """ID for the generated response, if the provider sends one."""

    timestamp: Any = None
    """Timestamp for the start of the generated response, if the provider sends one."""

    model_id: str | None = None
    """The ID of the response model that was used to generate the response, if the provider sends one."""

    headers: SharedV2Headers | None = None
    """Response headers."""

    body: Any = None
    """Response HTTP body."""


@dataclass(frozen=True)
class LanguageModelV2GenerateResult:
    """Result of a non-streaming language model generation call."""

    content: list[LanguageModelV2Content] = field(default_factory=list)
    """Ordered content that the model has generated."""

    finish_reason: LanguageModelV2FinishReason = 'unknown'
    """Finish reason."""

    usage: LanguageModelV2Usage = field(default_factory=LanguageModelV2Usage)
    """Usage information."""

    provider_metadata: SharedV2ProviderMetadata | None = None
    """Additional provider-specific metadata.

    They are passed through from the provider to the AI SDK and enable
    provider-specific results that can be fully encapsulated in the provider.
    """

    request: LanguageModelV2GenerateRequest | None = None
    """Optional request information for telemetry and debugging purposes."""

    response: LanguageModelV2GenerateResponse | None = None
    """Optional response information for telemetry and debugging purposes."""

    warnings: list[LanguageModelV2CallWarning] = field(default_factory=list)
    """Warnings for the call, e.g. unsupported settings."""


@dataclass(frozen=True)
class LanguageModelV2StreamRequest:
    """Optional request information for telemetry and debugging purposes."""

    body: Any = None
    """Request HTTP body that was sent to the provider API."""


@dataclass(frozen=True)
class LanguageModelV2StreamResponse:
    """Optional response data."""

    headers: SharedV2Headers | None = None
    """Response headers."""


@dataclass(frozen=True)
class LanguageModelV2StreamResult:
    """Result of a streaming language model generation call."""

    stream: AsyncIterator[LanguageModelV2StreamPart] = field(
        default_factory=lambda: _empty_async_iterator()
    )

    request: LanguageModelV2StreamRequest | None = None
    """Optional request information for telemetry and debugging purposes."""

    response: LanguageModelV2StreamResponse | None = None
    """Optional response data."""


async def _empty_async_iterator() -> AsyncIterator[LanguageModelV2StreamPart]:
    """Helper to provide an empty async iterator as a default factory."""
    return
    yield  # pragma: no cover - makes this an async generator


@runtime_checkable
class LanguageModelV2(Protocol):
    """Specification for a language model that implements the language model interface version 2."""

    @property
    def specification_version(self) -> Literal['v2']:
        """The language model must specify which language model interface version it implements."""
        ...

    @property
    def provider(self) -> str:
        """Name of the provider for logging purposes."""
        ...

    @property
    def model_id(self) -> str:
        """Provider-specific model ID for logging purposes."""
        ...

    @property
    def supported_urls(
        self,
    ) -> Awaitable[dict[str, list[re.Pattern[str]]]] | dict[str, list[re.Pattern[str]]]:
        """Supported URL patterns by media type for the provider.

        The keys are media type patterns or full media types (e.g. ``*/*`` for
        everything, ``audio/*``, ``video/*``, or ``application/pdf``) and the
        values are arrays of regular expressions that match the URL paths.

        The matching should be against lower-case URLs.

        Matched URLs are supported natively by the model and are not downloaded.

        Returns:
            A map of supported URL patterns by media type (as a promise or a
            plain object).
        """
        ...

    def do_generate(
        self,
        options: LanguageModelV2CallOptions,
    ) -> Awaitable[LanguageModelV2GenerateResult]:
        """Generate a language model output (non-streaming).

        Naming: "do" prefix to prevent accidental direct usage of the method
        by the user.
        """
        ...

    def do_stream(
        self,
        options: LanguageModelV2CallOptions,
    ) -> Awaitable[LanguageModelV2StreamResult]:
        """Generate a language model output (streaming).

        Naming: "do" prefix to prevent accidental direct usage of the method
        by the user.

        Returns:
            A stream of higher-level language model output parts.
        """
        ...

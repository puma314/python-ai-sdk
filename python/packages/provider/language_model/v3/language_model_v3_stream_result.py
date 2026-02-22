from __future__ import annotations
"""Language model v3 stream result type.

Translated from: packages/provider/src/language-model/v3/language-model-v3-stream-result.ts
"""

from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from typing import Any

from ...shared.v3.shared_v3_headers import SharedV3Headers
from .language_model_v3_stream_part import LanguageModelV3StreamPart


@dataclass(frozen=True)
class LanguageModelV3StreamResultRequest:
    """Optional request information for telemetry and debugging purposes."""

    body: Any = None
    """Request HTTP body that was sent to the provider API."""


@dataclass(frozen=True)
class LanguageModelV3StreamResultResponse:
    """Optional response data."""

    headers: SharedV3Headers | None = None
    """Response headers."""


@dataclass(frozen=True)
class LanguageModelV3StreamResult:
    """The result of a language model doStream call."""

    stream: AsyncIterator[LanguageModelV3StreamPart] = field(
        default_factory=lambda: _empty_async_iterator()
    )
    """The stream."""

    request: LanguageModelV3StreamResultRequest | None = None
    """Optional request information for telemetry and debugging purposes."""

    response: LanguageModelV3StreamResultResponse | None = None
    """Optional response data."""


async def _empty_async_iterator() -> AsyncIterator[LanguageModelV3StreamPart]:
    """Return an empty async iterator as a default for the stream field."""
    return
    yield  # noqa: RET504 - makes this an async generator

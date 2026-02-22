from __future__ import annotations

"""The result of a language model doGenerate call.

Translated from: packages/provider/src/language-model/v3/language-model-v3-generate-result.ts
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ...shared.v3.shared_v3_headers import SharedV3Headers
from ...shared.v3.shared_v3_provider_metadata import SharedV3ProviderMetadata
from ...shared.v3.shared_v3_warning import SharedV3Warning
from .language_model_v3_content import LanguageModelV3Content
from .language_model_v3_finish_reason import LanguageModelV3FinishReason
from .language_model_v3_usage import LanguageModelV3Usage


@dataclass(frozen=True)
class LanguageModelV3GenerateResultRequest:
    """Optional request information for telemetry and debugging purposes."""

    body: Any = None
    """Request HTTP body that was sent to the provider API."""


@dataclass(frozen=True)
class LanguageModelV3GenerateResultResponse:
    """Optional response information for telemetry and debugging purposes.

    Combines LanguageModelV3ResponseMetadata fields with additional
    response headers and body.
    """

    # Fields from LanguageModelV3ResponseMetadata
    id: str | None = None
    """ID for the generated response, if the provider sends one."""

    timestamp: datetime | None = None
    """Timestamp for the start of the generated response, if the provider sends one."""

    model_id: str | None = None
    """The ID of the response model that was used to generate the response, if the provider sends one."""

    # Additional fields
    headers: SharedV3Headers | None = None
    """Response headers."""

    body: Any = None
    """Response HTTP body."""


@dataclass(frozen=True)
class LanguageModelV3GenerateResult:
    """The result of a language model doGenerate call."""

    content: list[LanguageModelV3Content]
    """Ordered content that the model has generated."""

    finish_reason: LanguageModelV3FinishReason
    """The finish reason."""

    usage: LanguageModelV3Usage
    """The usage information."""

    warnings: list[SharedV3Warning]
    """Warnings for the call, e.g. unsupported settings."""

    provider_metadata: SharedV3ProviderMetadata | None = None
    """Additional provider-specific metadata. They are passed through
    from the provider to the AI SDK and enable provider-specific
    results that can be fully encapsulated in the provider.
    """

    request: LanguageModelV3GenerateResultRequest | None = None
    """Optional request information for telemetry and debugging purposes."""

    response: LanguageModelV3GenerateResultResponse | None = None
    """Optional response information for telemetry and debugging purposes."""

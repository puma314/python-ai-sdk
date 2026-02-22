from __future__ import annotations

"""The result of an embedding model doEmbed call.

Translated from: packages/provider/src/embedding-model/v3/embedding-model-v3-result.ts
"""

from dataclasses import dataclass, field
from typing import Any

from ...shared.v3.shared_v3_headers import SharedV3Headers
from ...shared.v3.shared_v3_provider_metadata import SharedV3ProviderMetadata
from ...shared.v3.shared_v3_warning import SharedV3Warning
from .embedding_model_v3_embedding import EmbeddingModelV3Embedding


@dataclass(frozen=True)
class EmbeddingModelV3ResultResponse:
    """Optional response information for debugging purposes."""

    headers: SharedV3Headers | None = None
    """Response headers."""

    body: Any = None
    """The response body."""


@dataclass(frozen=True)
class EmbeddingModelV3ResultUsage:
    """Token usage. We only have input tokens for embeddings."""

    tokens: int = 0


@dataclass(frozen=True)
class EmbeddingModelV3Result:
    """The result of an embedding model doEmbed call."""

    embeddings: list[EmbeddingModelV3Embedding] = field(default_factory=list)
    """Generated embeddings. They are in the same order as the input values."""

    usage: EmbeddingModelV3ResultUsage | None = None
    """Token usage. We only have input tokens for embeddings."""

    provider_metadata: SharedV3ProviderMetadata | None = None
    """Additional provider-specific metadata. They are passed through
    from the provider to the AI SDK and enable provider-specific
    results that can be fully encapsulated in the provider."""

    response: EmbeddingModelV3ResultResponse | None = None
    """Optional response information for debugging purposes."""

    warnings: list[SharedV3Warning] = field(default_factory=list)
    """Warnings for the call, e.g. unsupported settings."""

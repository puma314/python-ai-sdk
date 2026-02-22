from __future__ import annotations
"""Specification for an embedding model (v2 interface).

Translated from: packages/provider/src/embedding-model/v2/embedding-model-v2.ts
"""

import asyncio
from dataclasses import dataclass, field
from typing import Any, Awaitable, Generic, Literal, Protocol, TypeVar

from ...shared.v2.shared_v2_headers import SharedV2Headers
from ...shared.v2.shared_v2_provider_metadata import SharedV2ProviderMetadata
from ...shared.v2.shared_v2_provider_options import SharedV2ProviderOptions
from .embedding_model_v2_embedding import EmbeddingModelV2Embedding

VALUE = TypeVar("VALUE")


@dataclass(frozen=True)
class EmbeddingModelV2DoEmbedResponse:
    """Response from the do_embed method."""

    embeddings: list[EmbeddingModelV2Embedding] = field(default_factory=list)
    """Generated embeddings. They are in the same order as the input values."""

    usage: EmbeddingModelV2TokenUsage | None = None
    """Token usage. We only have input tokens for embeddings."""

    provider_metadata: SharedV2ProviderMetadata | None = None
    """Additional provider-specific metadata. They are passed through
    from the provider to the AI SDK and enable provider-specific
    results that can be fully encapsulated in the provider."""

    response: EmbeddingModelV2ResponseMetadata | None = None
    """Optional response information for debugging purposes."""


@dataclass(frozen=True)
class EmbeddingModelV2TokenUsage:
    """Token usage for embedding calls."""

    tokens: int = 0


@dataclass(frozen=True)
class EmbeddingModelV2ResponseMetadata:
    """Optional response information for debugging purposes."""

    headers: SharedV2Headers | None = None
    """Response headers."""

    body: Any = None
    """The response body."""


class EmbeddingModelV2(Protocol[VALUE]):
    """Specification for an embedding model that implements the embedding model
    interface version 2.

    VALUE is the type of the values that the model can embed.
    This will allow us to go beyond text embeddings in the future,
    e.g. to support image embeddings.
    """

    @property
    def specification_version(self) -> Literal["v2"]:
        """The embedding model must specify which embedding model interface
        version it implements. This will allow us to evolve the embedding
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

    @property
    def max_embeddings_per_call(self) -> int | None | Awaitable[int | None]:
        """Limit of how many embeddings can be generated in a single API call.

        Use float('inf') for models that do not have a limit.
        """
        ...

    @property
    def supports_parallel_calls(self) -> bool | Awaitable[bool]:
        """True if the model can handle multiple embedding calls in parallel."""
        ...

    def do_embed(
        self,
        *,
        values: list[VALUE],
        abort_signal: asyncio.Event | None = None,
        provider_options: SharedV2ProviderOptions | None = None,
        headers: dict[str, str | None] | None = None,
    ) -> Awaitable[EmbeddingModelV2DoEmbedResponse]:
        """Generates a list of embeddings for the given input text.

        Naming: "do" prefix to prevent accidental direct usage of the method
        by the user.

        Args:
            values: List of values to embed.
            abort_signal: Abort signal for cancelling the operation.
            provider_options: Additional provider-specific options. They are passed
                through to the provider from the AI SDK and enable provider-specific
                functionality that can be fully encapsulated in the provider.
            headers: Additional HTTP headers to be sent with the request.
                Only applicable for HTTP-based providers.

        Returns:
            The embedding response containing embeddings, usage, metadata,
            and optional response information.
        """
        ...

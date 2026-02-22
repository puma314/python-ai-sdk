from __future__ import annotations

"""Specification for a reranking model that implements the reranking model interface version 3.

Translated from: packages/provider/src/reranking-model/v3/reranking-model-v3.ts
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Awaitable, Literal, Protocol

from ...shared.v3 import SharedV3Headers, SharedV3ProviderMetadata, SharedV3Warning
from .reranking_model_v3_call_options import RerankingModelV3CallOptions


@dataclass(frozen=True)
class RerankingModelV3RankingEntry:
    """A single entry in the reranking result."""

    index: int = 0
    """The index of the document in the original list of documents before reranking."""

    relevance_score: float = 0.0
    """The relevance score of the document after reranking."""


@dataclass(frozen=True)
class RerankingModelV3ResponseMetadata:
    """Optional response information for debugging purposes."""

    id: str | None = None
    """ID for the generated response, if the provider sends one."""

    timestamp: datetime | None = None
    """Timestamp for the start of the generated response, if the provider sends one."""

    model_id: str | None = None
    """The ID of the response model that was used to generate the response, if the provider sends one."""

    headers: SharedV3Headers | None = None
    """Response headers."""

    body: Any = None
    """Response body."""


@dataclass(frozen=True)
class RerankingModelV3Result:
    """Result of a reranking model V3 call."""

    ranking: list[RerankingModelV3RankingEntry] = field(default_factory=list)
    """Ordered list of reranked documents (via index before reranking).
    The documents are sorted by the descending order of relevance scores.
    """

    provider_metadata: SharedV3ProviderMetadata | None = None
    """Additional provider-specific metadata. They are passed through
    to the provider from the AI SDK and enable provider-specific
    functionality that can be fully encapsulated in the provider.
    """

    warnings: list[SharedV3Warning] | None = None
    """Warnings for the call, e.g. unsupported settings."""

    response: RerankingModelV3ResponseMetadata | None = None
    """Optional response information for debugging purposes."""


class RerankingModelV3(Protocol):
    """Specification for a reranking model that implements the reranking model interface version 3."""

    @property
    def specification_version(self) -> Literal['v3']:
        """The reranking model must specify which reranking model interface version it implements."""
        ...

    @property
    def provider(self) -> str:
        """Provider ID."""
        ...

    @property
    def model_id(self) -> str:
        """Provider-specific model ID."""
        ...

    def do_rerank(
        self, options: RerankingModelV3CallOptions
    ) -> Awaitable[RerankingModelV3Result]:
        """Reranking a list of documents using the query.

        Note: "do" prefix to prevent accidental direct usage of the method by the user.
        """
        ...

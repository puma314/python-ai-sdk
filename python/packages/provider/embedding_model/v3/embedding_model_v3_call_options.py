from __future__ import annotations
"""Embedding model v3 call options.

Translated from: packages/provider/src/embedding-model/v3/embedding-model-v3-call-options.ts
"""

import asyncio
from dataclasses import dataclass, field

from ...shared import SharedV3Headers, SharedV3ProviderOptions


@dataclass(frozen=True)
class EmbeddingModelV3CallOptions:
    """Options for an embedding model v3 call."""

    values: list[str] = field(default_factory=list)
    """List of text values to generate embeddings for."""

    abort_signal: asyncio.Event | None = None
    """Abort signal for cancelling the operation."""

    provider_options: SharedV3ProviderOptions | None = None
    """Additional provider-specific options. They are passed through
    to the provider from the AI SDK and enable provider-specific
    functionality that can be fully encapsulated in the provider."""

    headers: SharedV3Headers | None = None
    """Additional HTTP headers to be sent with the request.
    Only applicable for HTTP-based providers."""

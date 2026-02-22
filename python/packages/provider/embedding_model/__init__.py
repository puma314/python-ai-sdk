from __future__ import annotations

"""Public API for embedding model.

Translated from: packages/provider/src/embedding-model/index.ts
"""

from .v3 import (
    EmbeddingModelV3,
    EmbeddingModelV3CallOptions,
    EmbeddingModelV3Embedding,
    EmbeddingModelV3Result,
    EmbeddingModelV3ResultResponse,
    EmbeddingModelV3ResultUsage,
)
from .v2 import (
    EmbeddingModelV2,
    EmbeddingModelV2DoEmbedResponse,
    EmbeddingModelV2Embedding,
    EmbeddingModelV2ResponseMetadata,
    EmbeddingModelV2TokenUsage,
)

__all__ = [
    "EmbeddingModelV3",
    "EmbeddingModelV3CallOptions",
    "EmbeddingModelV3Embedding",
    "EmbeddingModelV3Result",
    "EmbeddingModelV3ResultResponse",
    "EmbeddingModelV3ResultUsage",
    "EmbeddingModelV2",
    "EmbeddingModelV2DoEmbedResponse",
    "EmbeddingModelV2Embedding",
    "EmbeddingModelV2ResponseMetadata",
    "EmbeddingModelV2TokenUsage",
]

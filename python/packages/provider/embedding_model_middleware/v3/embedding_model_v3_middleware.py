from __future__ import annotations
"""Middleware for EmbeddingModelV3.

This type defines the structure for middleware that can be used to modify
the behavior of EmbeddingModelV3 operations.

Translated from: packages/provider/src/embedding-model-middleware/v3/embedding-model-v3-middleware.ts
"""

from dataclasses import dataclass, field
from typing import Awaitable, Callable, Literal

from ...embedding_model.v3.embedding_model_v3 import EmbeddingModelV3
from ...embedding_model.v3.embedding_model_v3_call_options import (
    EmbeddingModelV3CallOptions,
)
from ...embedding_model.v3.embedding_model_v3_result import EmbeddingModelV3Result


@dataclass(frozen=True)
class EmbeddingModelV3Middleware:
    """Middleware for EmbeddingModelV3.

    This type defines the structure for middleware that can be used to modify
    the behavior of EmbeddingModelV3 operations.

    All hook fields are optional. A middleware with only ``specification_version``
    set to ``'v3'`` is fully valid.
    """

    specification_version: Literal['v3'] = 'v3'
    """Middleware specification version. Use ``v3`` for the current version."""

    override_provider: Callable[[EmbeddingModelV3], str] | None = None
    """Override the provider name if desired.

    Called with the embedding model instance and should return the new provider name.
    """

    override_model_id: Callable[[EmbeddingModelV3], str] | None = None
    """Override the model ID if desired.

    Called with the embedding model instance and should return the new model ID.
    """

    override_max_embeddings_per_call: (
        Callable[[EmbeddingModelV3], Awaitable[int | None] | int | None] | None
    ) = None
    """Override the limit of how many embeddings can be generated in a single API call if desired.

    Called with the embedding model instance.
    """

    override_supports_parallel_calls: (
        Callable[[EmbeddingModelV3], Awaitable[bool] | bool] | None
    ) = None
    """Override support for handling multiple embedding calls in parallel, if desired.

    Called with the embedding model instance.
    """

    transform_params: (
        Callable[
            [EmbeddingModelV3CallOptions, EmbeddingModelV3],
            Awaitable[EmbeddingModelV3CallOptions],
        ]
        | None
    ) = None
    """Transform the parameters before they are passed to the embed model.

    Called with the original parameters and the embedding model instance.
    Returns a promise that resolves to the transformed parameters.
    """

    wrap_embed: (
        Callable[
            [
                Callable[[], Awaitable[EmbeddingModelV3Result]],
                EmbeddingModelV3CallOptions,
                EmbeddingModelV3,
            ],
            Awaitable[EmbeddingModelV3Result],
        ]
        | None
    ) = None
    """Wrap the embed operation of the embedding model.

    Called with:
        do_embed: The original embed function.
        params: The parameters for the embed call. If the
            ``transform_params`` middleware is used, this will be
            the transformed parameters.
        model: The embedding model instance.

    Returns a promise that resolves to the result of the generate operation.
    """

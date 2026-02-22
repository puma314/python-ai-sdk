from __future__ import annotations

"""Specification for an embedding model that implements the embedding model
interface version 3.

Translated from: packages/provider/src/embedding-model/v3/embedding-model-v3.ts
"""

from typing import Awaitable, Literal, Protocol, runtime_checkable

from .embedding_model_v3_call_options import EmbeddingModelV3CallOptions
from .embedding_model_v3_result import EmbeddingModelV3Result


@runtime_checkable
class EmbeddingModelV3(Protocol):
    """Specification for an embedding model that implements the embedding model
    interface version 3.

    It is specific to text embeddings.
    """

    @property
    def specification_version(self) -> Literal['v3']:
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
    def max_embeddings_per_call(
        self,
    ) -> Awaitable[int | None] | int | None:
        """Limit of how many embeddings can be generated in a single API call.

        Use float('inf') for models that do not have a limit.
        """
        ...

    @property
    def supports_parallel_calls(self) -> Awaitable[bool] | bool:
        """True if the model can handle multiple embedding calls in parallel."""
        ...

    def do_embed(
        self,
        options: EmbeddingModelV3CallOptions,
    ) -> Awaitable[EmbeddingModelV3Result]:
        """Generates a list of embeddings for the given input text.

        Naming: "do" prefix to prevent accidental direct usage of the method
        by the user.
        """
        ...

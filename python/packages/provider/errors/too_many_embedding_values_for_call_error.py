from __future__ import annotations

"""Too many embedding values for call error.

Translated from: packages/provider/src/errors/too-many-embedding-values-for-call-error.ts
"""

from typing import Any, ClassVar

from .ai_sdk_error import AISDKError

_NAME = "AI_TooManyEmbeddingValuesForCallError"
_MARKER = f"vercel.ai.error.{_NAME}"


class TooManyEmbeddingValuesForCallError(AISDKError):

    _marker: ClassVar[str] = _MARKER  # used in is_instance

    provider: str
    model_id: str
    max_embeddings_per_call: int
    values: list[Any]

    def __init__(
        self,
        *,
        provider: str,
        model_id: str,
        max_embeddings_per_call: int,
        values: list[Any],
    ) -> None:
        super().__init__(
            name=_NAME,
            message=(
                f"Too many values for a single embedding call. "
                f'The {provider} model "{model_id}" can only embed up to '
                f"{max_embeddings_per_call} values per call, but {len(values)} values were provided."
            ),
        )

        self.provider = provider
        self.model_id = model_id
        self.max_embeddings_per_call = max_embeddings_per_call
        self.values = values

    @classmethod
    def is_instance(cls, error: object) -> bool:
        return AISDKError.has_marker(error, _MARKER)

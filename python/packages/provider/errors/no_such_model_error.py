from __future__ import annotations

"""No such model error.

Translated from: packages/provider/src/errors/no-such-model-error.ts
"""

from typing import ClassVar, Literal

from .ai_sdk_error import AISDKError

_NAME = "AI_NoSuchModelError"
_MARKER = f"vercel.ai.error.{_NAME}"

ModelType = Literal[
    "languageModel",
    "embeddingModel",
    "imageModel",
    "transcriptionModel",
    "speechModel",
    "rerankingModel",
    "videoModel",
]


class NoSuchModelError(AISDKError):
    _marker: ClassVar[str] = _MARKER  # used in is_instance

    model_id: str
    model_type: ModelType

    def __init__(
        self,
        *,
        error_name: str = _NAME,
        model_id: str,
        model_type: ModelType,
        message: str | None = None,
    ) -> None:
        if message is None:
            message = f"No such {model_type}: {model_id}"

        super().__init__(name=error_name, message=message)

        self.model_id = model_id
        self.model_type = model_type

    @classmethod
    def is_instance(cls, error: object) -> bool:
        return AISDKError.has_marker(error, _MARKER)

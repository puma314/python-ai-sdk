from __future__ import annotations

"""No content generated error.

Translated from: packages/provider/src/errors/no-content-generated-error.ts
"""

from typing import ClassVar

from .ai_sdk_error import AISDKError

_NAME = "AI_NoContentGeneratedError"
_MARKER = f"vercel.ai.error.{_NAME}"


class NoContentGeneratedError(AISDKError):
    """Thrown when the AI provider fails to generate any content."""

    _marker: ClassVar[str] = _MARKER  # used in is_instance

    def __init__(
        self,
        *,
        message: str = "No content generated.",
    ) -> None:
        super().__init__(name=_NAME, message=message)

    @classmethod
    def is_instance(cls, error: object) -> bool:
        return AISDKError.has_marker(error, _MARKER)

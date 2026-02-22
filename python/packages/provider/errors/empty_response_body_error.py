from __future__ import annotations

"""Empty response body error.

Translated from: packages/provider/src/errors/empty-response-body-error.ts
"""

from typing import ClassVar

from .ai_sdk_error import AISDKError

_NAME = "AI_EmptyResponseBodyError"
_MARKER = f"vercel.ai.error.{_NAME}"


class EmptyResponseBodyError(AISDKError):
    """Error raised when a response body is empty."""

    _marker: ClassVar[str] = _MARKER  # used in is_instance

    def __init__(self, *, message: str = "Empty response body") -> None:
        super().__init__(name=_NAME, message=message)

    @classmethod
    def is_instance(cls, error: object) -> bool:
        return AISDKError.has_marker(error, _MARKER)

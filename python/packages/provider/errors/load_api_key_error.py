from __future__ import annotations

"""Load API key error.

Translated from: packages/provider/src/errors/load-api-key-error.ts
"""

from typing import ClassVar

from .ai_sdk_error import AISDKError

_NAME = "AI_LoadAPIKeyError"
_MARKER = f"vercel.ai.error.{_NAME}"


class LoadAPIKeyError(AISDKError):
    """Error raised when an API key cannot be loaded."""

    _marker: ClassVar[str] = _MARKER  # used in is_instance

    def __init__(self, *, message: str) -> None:
        super().__init__(name=_NAME, message=message)

    @classmethod
    def is_instance(cls, error: object) -> bool:
        return AISDKError.has_marker(error, _MARKER)

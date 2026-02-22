from __future__ import annotations

"""Unsupported functionality error.

Translated from: packages/provider/src/errors/unsupported-functionality-error.ts
"""

from typing import ClassVar

from .ai_sdk_error import AISDKError

_NAME = "AI_UnsupportedFunctionalityError"
_MARKER = f"vercel.ai.error.{_NAME}"


class UnsupportedFunctionalityError(AISDKError):
    _marker: ClassVar[str] = _MARKER  # used in is_instance

    functionality: str

    def __init__(
        self,
        *,
        functionality: str,
        message: str | None = None,
    ) -> None:
        if message is None:
            message = f"'{functionality}' functionality not supported."

        super().__init__(name=_NAME, message=message)

        self.functionality = functionality

    @classmethod
    def is_instance(cls, error: object) -> bool:
        return AISDKError.has_marker(error, _MARKER)

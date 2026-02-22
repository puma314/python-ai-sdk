from __future__ import annotations

"""Invalid argument error class.

Translated from: packages/provider/src/errors/invalid-argument-error.ts
"""

from typing import ClassVar

from .ai_sdk_error import AISDKError

_NAME = "AI_InvalidArgumentError"
_MARKER = f"vercel.ai.error.{_NAME}"


class InvalidArgumentError(AISDKError):
    """A function argument is invalid."""

    _marker: ClassVar[str] = _MARKER  # used in is_instance

    argument: str

    def __init__(
        self,
        *,
        argument: str,
        message: str,
        cause: BaseException | None = None,
    ) -> None:
        super().__init__(name=_NAME, message=message, cause=cause)

        self.argument = argument

    @classmethod
    def is_instance(cls, error: object) -> bool:
        return AISDKError.has_marker(error, _MARKER)

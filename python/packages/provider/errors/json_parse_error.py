from __future__ import annotations

"""JSON parse error class.

Translated from: packages/provider/src/errors/json-parse-error.ts
"""

from typing import ClassVar

from .ai_sdk_error import AISDKError
from .get_error_message import get_error_message

_NAME = "AI_JSONParseError"
_MARKER = f"vercel.ai.error.{_NAME}"


class JSONParseError(AISDKError):

    _marker: ClassVar[str] = _MARKER  # used in is_instance

    text: str

    def __init__(self, *, text: str, cause: BaseException | None = None) -> None:
        super().__init__(
            name=_NAME,
            message=(
                f"JSON parsing failed: "
                f"Text: {text}.\n"
                f"Error message: {get_error_message(cause)}"
            ),
            cause=cause,
        )

        self.text = text

    @classmethod
    def is_instance(cls, error: object) -> bool:
        return AISDKError.has_marker(error, _MARKER)

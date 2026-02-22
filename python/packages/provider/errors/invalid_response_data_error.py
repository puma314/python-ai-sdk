from __future__ import annotations

"""Invalid response data error.

Translated from: packages/provider/src/errors/invalid-response-data-error.ts
"""

import json
from typing import Any, ClassVar

from .ai_sdk_error import AISDKError

_NAME = "AI_InvalidResponseDataError"
_MARKER = f"vercel.ai.error.{_NAME}"


class InvalidResponseDataError(AISDKError):
    """Server returned a response with invalid data content.

    This should be thrown by providers when they cannot parse the response
    from the API.
    """

    _marker: ClassVar[str] = _MARKER  # used in is_instance

    data: Any
    """The invalid response data."""

    def __init__(
        self,
        *,
        data: Any,
        message: str | None = None,
    ) -> None:
        if message is None:
            message = f"Invalid response data: {json.dumps(data)}."

        super().__init__(name=_NAME, message=message)

        self.data = data

    @classmethod
    def is_instance(cls, error: object) -> bool:
        return AISDKError.has_marker(error, _MARKER)

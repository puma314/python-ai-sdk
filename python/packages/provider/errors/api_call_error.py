from __future__ import annotations

"""API call error class for handling HTTP API errors.

Translated from: packages/provider/src/errors/api-call-error.ts
"""

from typing import Any, ClassVar

from .ai_sdk_error import AISDKError

_NAME = "AI_APICallError"
_MARKER = f"vercel.ai.error.{_NAME}"


class APICallError(AISDKError):
    """Error class for API call failures."""

    _marker: ClassVar[str] = _MARKER  # used in is_instance

    url: str
    request_body_values: Any
    status_code: int | None
    response_headers: dict[str, str] | None
    response_body: str | None
    is_retryable: bool
    data: Any | None

    def __init__(
        self,
        *,
        message: str,
        url: str,
        request_body_values: Any,
        status_code: int | None = None,
        response_headers: dict[str, str] | None = None,
        response_body: str | None = None,
        cause: BaseException | None = None,
        is_retryable: bool | None = None,
        data: Any | None = None,
    ) -> None:
        super().__init__(name=_NAME, message=message, cause=cause)

        self.url = url
        self.request_body_values = request_body_values
        self.status_code = status_code
        self.response_headers = response_headers
        self.response_body = response_body
        self.data = data

        # Default is_retryable based on status code if not explicitly provided
        if is_retryable is not None:
            self.is_retryable = is_retryable
        else:
            self.is_retryable = (
                status_code is not None
                and (
                    status_code == 408  # request timeout
                    or status_code == 409  # conflict
                    or status_code == 429  # too many requests
                    or status_code >= 500  # server error
                )
            )

    @classmethod
    def is_instance(cls, error: object) -> bool:
        return AISDKError.has_marker(error, _MARKER)

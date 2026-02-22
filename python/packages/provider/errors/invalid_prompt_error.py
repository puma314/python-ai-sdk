from __future__ import annotations

"""Invalid prompt error.

A prompt is invalid. This error should be thrown by providers when they cannot
process a prompt.

Translated from: packages/provider/src/errors/invalid-prompt-error.ts
"""

from typing import Any, ClassVar

from .ai_sdk_error import AISDKError

_NAME = "AI_InvalidPromptError"
_MARKER = f"vercel.ai.error.{_NAME}"


class InvalidPromptError(AISDKError):
    """A prompt is invalid. This error should be thrown by providers when they cannot
    process a prompt.
    """

    _marker: ClassVar[str] = _MARKER  # used in is_instance

    prompt: Any

    def __init__(
        self,
        *,
        prompt: Any,
        message: str,
        cause: BaseException | None = None,
    ) -> None:
        """Creates an InvalidPromptError.

        Args:
            prompt: The invalid prompt.
            message: The error message describing why the prompt is invalid.
            cause: The underlying cause of the error.
        """
        super().__init__(name=_NAME, message=f"Invalid prompt: {message}", cause=cause)

        self.prompt = prompt

    @classmethod
    def is_instance(cls, error: object) -> bool:
        """Checks if the given error is an InvalidPromptError.

        Args:
            error: The error to check.

        Returns:
            True if the error is an InvalidPromptError, false otherwise.
        """
        return AISDKError.has_marker(error, _MARKER)

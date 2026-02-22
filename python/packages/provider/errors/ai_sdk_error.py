from __future__ import annotations

"""AI SDK base error class.

Translated from: packages/provider/src/errors/ai-sdk-error.ts
"""

from typing import ClassVar


# Marker string used for identifying AI SDK Error instances.
# Enables checking if an error is an instance of AISDKError across package versions.
_MARKER = "vercel.ai.error"


class AISDKError(Exception):
    """Custom error class for AI SDK related errors."""

    _marker: ClassVar[str] = _MARKER  # used in is_instance

    cause: BaseException | None
    """The underlying cause of the error, if any."""

    def __init__(
        self,
        *,
        name: str,
        message: str,
        cause: BaseException | None = None,
    ) -> None:
        """Creates an AI SDK Error.

        Args:
            name: The name of the error.
            message: The error message.
            cause: The underlying cause of the error.
        """
        super().__init__(message)

        self.name = name
        self.cause = cause
        if cause is not None:
            self.__cause__ = cause

    @classmethod
    def is_instance(cls, error: object) -> bool:
        """Checks if the given error is an AI SDK Error.

        Args:
            error: The error to check.

        Returns:
            True if the error is an AI SDK Error, false otherwise.
        """
        return cls.has_marker(error, _MARKER)

    @staticmethod
    def has_marker(error: object, marker: str) -> bool:
        return (
            error is not None
            and isinstance(error, Exception)
            and hasattr(error, "_marker")
            and isinstance(getattr(error, "_marker", None), str)
            and getattr(error, "_marker", "").startswith(marker)
        )

from __future__ import annotations

"""Type validation error for the AI SDK.

Translated from: packages/provider/src/errors/type-validation-error.ts
"""

import json
from dataclasses import dataclass
from typing import Any, ClassVar

from .ai_sdk_error import AISDKError
from .get_error_message import get_error_message

_NAME = "AI_TypeValidationError"
_MARKER = f"vercel.ai.error.{_NAME}"


@dataclass(frozen=True)
class TypeValidationContext:
    """Context information about a type validation failure."""

    field: str | None = None
    """Field path in dot notation (e.g., "message.metadata", "message.parts[3].data")"""

    entity_name: str | None = None
    """Entity name (e.g., tool name, data type name)"""

    entity_id: str | None = None
    """Entity identifier (e.g., message ID, tool call ID)"""


class TypeValidationError(AISDKError):
    """Error raised when a value fails type validation."""

    _marker: ClassVar[str] = _MARKER  # used in is_instance

    value: Any
    context: TypeValidationContext | None

    def __init__(
        self,
        *,
        value: Any,
        cause: Any,
        context: TypeValidationContext | None = None,
    ) -> None:
        context_prefix = "Type validation failed"

        if context is not None and context.field is not None:
            context_prefix += f" for {context.field}"

        if context is not None and (
            context.entity_name is not None or context.entity_id is not None
        ):
            context_prefix += " ("
            parts: list[str] = []
            if context.entity_name is not None:
                parts.append(context.entity_name)
            if context.entity_id is not None:
                parts.append(f'id: "{context.entity_id}"')
            context_prefix += ", ".join(parts)
            context_prefix += ")"

        # Convert cause to BaseException if it isn't already
        error_cause: BaseException | None = None
        if isinstance(cause, BaseException):
            error_cause = cause

        super().__init__(
            name=_NAME,
            message=(
                f"{context_prefix}: "
                f"Value: {json.dumps(value)}.\n"
                f"Error message: {get_error_message(cause)}"
            ),
            cause=error_cause,
        )

        self.value = value
        self.context = context

    @classmethod
    def is_instance(cls, error: object) -> bool:
        """Checks if the given error is a TypeValidationError.

        Args:
            error: The error to check.

        Returns:
            True if the error is a TypeValidationError, false otherwise.
        """
        return AISDKError.has_marker(error, _MARKER)

    @classmethod
    def wrap(
        cls,
        *,
        value: Any,
        cause: Any,
        context: TypeValidationContext | None = None,
    ) -> TypeValidationError:
        """Wraps an error into a TypeValidationError.

        If the cause is already a TypeValidationError with the same value and
        context, it returns the cause. Otherwise, it creates a new
        TypeValidationError.

        Args:
            value: The value that failed validation.
            cause: The original error or cause of the validation failure.
            context: Optional context about what is being validated.

        Returns:
            A TypeValidationError instance.
        """
        if (
            TypeValidationError.is_instance(cause)
            and isinstance(cause, TypeValidationError)
            and cause.value is value
            and (cause.context.field if cause.context is not None else None)
            == (context.field if context is not None else None)
            and (cause.context.entity_name if cause.context is not None else None)
            == (context.entity_name if context is not None else None)
            and (cause.context.entity_id if cause.context is not None else None)
            == (context.entity_id if context is not None else None)
        ):
            return cause

        return TypeValidationError(value=value, cause=cause, context=context)

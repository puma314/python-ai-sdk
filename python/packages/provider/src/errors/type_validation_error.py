"""Error raised when runtime type validation fails."""

from __future__ import annotations

from dataclasses import dataclass

from .ai_sdk_error import AISDKError
from .get_error_message import getErrorMessage


@dataclass
class TypeValidationContext:
  """Context for type-validation failures."""

  field: str | None = None
  entityName: str | None = None
  entityId: str | None = None


class TypeValidationError(AISDKError):
  """Raised when validating a value against an expected type fails."""

  def __init__(
    self,
    *,
    value: object,
    cause: object,
    context: TypeValidationContext | None = None,
  ):
    contextPrefix = 'Type validation failed'
    if context and context.field:
      contextPrefix += f' for {context.field}'
    if context and (context.entityName or context.entityId):
      parts: list[str] = []
      if context.entityName:
        parts.append(context.entityName)
      if context.entityId:
        parts.append(f'id: "{context.entityId}"')
      contextPrefix += f" ({', '.join(parts)})"

    super().__init__(
      name='AI_TypeValidationError',
      message=(
        f'{contextPrefix}: Value: {value!r}.\n'
        f'Error message: {getErrorMessage(cause)}'
      ),
      cause=cause,
    )
    self.value = value
    self.context = context

  @staticmethod
  def wrap(
    *,
    value: object,
    cause: object,
    context: TypeValidationContext | None = None,
  ) -> 'TypeValidationError':
    if isinstance(cause, TypeValidationError):
      if (
        cause.value is value
        and (cause.context.field if cause.context else None)
        == (context.field if context else None)
        and (cause.context.entityName if cause.context else None)
        == (context.entityName if context else None)
        and (cause.context.entityId if cause.context else None)
        == (context.entityId if context else None)
      ):
        return cause
    return TypeValidationError(value=value, cause=cause, context=context)

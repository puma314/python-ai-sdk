"""Error raised for invalid function arguments."""

from .ai_sdk_error import AISDKError


class InvalidArgumentError(AISDKError):
  """Raised when a required argument has an invalid value."""

  def __init__(
    self, *, argument: str, message: str, cause: object | None = None
  ):
    super().__init__(
      name='AI_InvalidArgumentError',
      message=message,
      cause=cause,
    )
    self.argument = argument

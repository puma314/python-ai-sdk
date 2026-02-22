"""Error raised when a prompt payload is invalid."""

from .ai_sdk_error import AISDKError


class InvalidPromptError(AISDKError):
  """Raised by providers when they cannot process a prompt."""

  def __init__(self, *, prompt: object, message: str, cause: object | None = None):
    super().__init__(
      name='AI_InvalidPromptError',
      message=f'Invalid prompt: {message}',
      cause=cause,
    )
    self.prompt = prompt

"""Error raised when provider generated no content."""

from .ai_sdk_error import AISDKError


class NoContentGeneratedError(AISDKError):
  """Raised when a model call returns no generated content."""

  def __init__(self, *, message: str = 'No content generated.'):
    super().__init__(name='AI_NoContentGeneratedError', message=message)

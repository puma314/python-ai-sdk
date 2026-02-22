"""Error raised when an API key cannot be loaded."""

from .ai_sdk_error import AISDKError


class LoadAPIKeyError(AISDKError):
  """Raised when provider API key resolution fails."""

  def __init__(self, *, message: str):
    super().__init__(name='AI_LoadAPIKeyError', message=message)

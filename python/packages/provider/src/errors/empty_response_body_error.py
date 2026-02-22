"""Error raised when a response body is unexpectedly empty."""

from .ai_sdk_error import AISDKError


class EmptyResponseBodyError(AISDKError):
  """Raised when a provider response does not contain expected content."""

  def __init__(self, *, message: str = 'Empty response body'):
    super().__init__(name='AI_EmptyResponseBodyError', message=message)

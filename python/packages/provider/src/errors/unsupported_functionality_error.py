"""Error raised when requested provider functionality is unsupported."""

from .ai_sdk_error import AISDKError


class UnsupportedFunctionalityError(AISDKError):
  """Raised for unsupported optional provider features."""

  def __init__(self, *, functionality: str, message: str | None = None):
    super().__init__(
      name='AI_UnsupportedFunctionalityError',
      message=message or f"'{functionality}' functionality not supported.",
    )
    self.functionality = functionality

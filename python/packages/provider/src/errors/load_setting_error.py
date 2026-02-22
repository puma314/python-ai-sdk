"""Error raised when required setting resolution fails."""

from .ai_sdk_error import AISDKError


class LoadSettingError(AISDKError):
  """Raised for missing/invalid environment or runtime settings."""

  def __init__(self, *, message: str):
    super().__init__(name='AI_LoadSettingError', message=message)

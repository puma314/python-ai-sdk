"""Error raised when provider response payload has invalid content."""

from __future__ import annotations

import json

from .ai_sdk_error import AISDKError


class InvalidResponseDataError(AISDKError):
  """Raised when provider response data cannot be interpreted."""

  def __init__(self, *, data: object, message: str | None = None):
    default = f'Invalid response data: {json.dumps(data, default=str)}.'
    super().__init__(
      name='AI_InvalidResponseDataError',
      message=message or default,
    )
    self.data = data

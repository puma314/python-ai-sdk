"""Error raised when JSON decoding fails."""

from .ai_sdk_error import AISDKError
from .get_error_message import getErrorMessage


class JSONParseError(AISDKError):
  """Raised when parsing JSON text fails."""

  def __init__(self, *, text: str, cause: object):
    super().__init__(
      name='AI_JSONParseError',
      message=(
        f'JSON parsing failed: Text: {text}.\n'
        f'Error message: {getErrorMessage(cause)}'
      ),
      cause=cause,
    )
    self.text = text

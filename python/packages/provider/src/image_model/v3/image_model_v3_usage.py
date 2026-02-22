"""Usage information for an image model call."""

from typing import TypedDict


class ImageModelV3Usage(TypedDict):
  """Token usage reported for an image generation call."""

  inputTokens: int | None
  outputTokens: int | None
  totalTokens: int | None

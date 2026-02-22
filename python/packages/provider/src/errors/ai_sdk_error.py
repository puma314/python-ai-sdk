"""Base error type for provider package exceptions."""

from __future__ import annotations


class AISDKError(Exception):
  """Base class for AI SDK errors with optional cause chaining."""

  def __init__(self, *, name: str, message: str, cause: object | None = None):
    super().__init__(message)
    self.name = name
    self.cause = cause

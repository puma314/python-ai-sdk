"""Error raised when an API call fails."""

from __future__ import annotations

from .ai_sdk_error import AISDKError


class APICallError(AISDKError):
  """Raised for transport and HTTP failures from model providers."""

  def __init__(
    self,
    *,
    message: str,
    url: str,
    requestBodyValues: object,
    statusCode: int | None = None,
    responseHeaders: dict[str, str] | None = None,
    responseBody: str | None = None,
    cause: object | None = None,
    isRetryable: bool | None = None,
    data: object | None = None,
  ):
    retryable = (
      isRetryable
      if isRetryable is not None
      else (
        statusCode is not None
        and (statusCode in {408, 409, 429} or statusCode >= 500)
      )
    )
    super().__init__(name='AI_APICallError', message=message, cause=cause)
    self.url = url
    self.requestBodyValues = requestBodyValues
    self.statusCode = statusCode
    self.responseHeaders = responseHeaders
    self.responseBody = responseBody
    self.isRetryable = retryable
    self.data = data

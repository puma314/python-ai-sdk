"""Anthropic API error schemas and response handlers."""

from __future__ import annotations

from pydantic import BaseModel


class _AnthropicErrorObject(BaseModel):
  type: str
  message: str


class AnthropicErrorData(BaseModel):
  """Top-level Anthropic error response structure."""

  type: str
  error: _AnthropicErrorObject


def anthropicErrorDataSchema() -> type[AnthropicErrorData]:
  """Return Anthropic error schema model class."""

  return AnthropicErrorData


def anthropicFailedResponseHandler(payload: dict[str, object]) -> str:
  """Extract an error message from Anthropic JSON error payload."""

  parsed = AnthropicErrorData.model_validate(payload)
  return parsed.error.message


__all__ = [
  'AnthropicErrorData',
  'anthropicErrorDataSchema',
  'anthropicFailedResponseHandler',
]

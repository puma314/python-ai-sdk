"""Anthropic code execution tool (2025-08-25)."""

from __future__ import annotations

from pydantic import BaseModel, Field

from ..anthropic_tools import codeExecution_20250825


class CodeExecution_20250825Input(BaseModel):
  type: str
  command: str | None = None
  code: str | None = None
  path: str | None = None
  file_text: str | None = None
  old_str: str | None = None
  new_str: str | None = None


class CodeExecution_20250825Output(BaseModel):
  type: str
  stdout: str | None = None
  stderr: str | None = None
  return_code: int | None = None
  content: list[dict[str, str]] = Field(default_factory=list)
  error_code: str | None = None


def codeExecution_20250825InputSchema() -> type[CodeExecution_20250825Input]:
  """Return pydantic model for code execution input validation."""

  return CodeExecution_20250825Input


def codeExecution_20250825OutputSchema() -> type[CodeExecution_20250825Output]:
  """Return pydantic model for code execution output validation."""

  return CodeExecution_20250825Output


__all__ = [
  'codeExecution_20250825',
  'codeExecution_20250825InputSchema',
  'codeExecution_20250825OutputSchema',
]

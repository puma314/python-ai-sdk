"""Anthropic code execution tool (2025-05-22)."""

from __future__ import annotations

from pydantic import BaseModel, Field

from ..anthropic_tools import codeExecution_20250522


class CodeExecutionOutputFile(BaseModel):
  type: str
  file_id: str


class CodeExecution_20250522Output(BaseModel):
  type: str
  stdout: str
  stderr: str
  return_code: int
  content: list[CodeExecutionOutputFile] = Field(default_factory=list)


def codeExecution_20250522OutputSchema() -> type[CodeExecution_20250522Output]:
  """Return pydantic model for code execution tool output validation."""

  return CodeExecution_20250522Output


__all__ = ['codeExecution_20250522', 'codeExecution_20250522OutputSchema']

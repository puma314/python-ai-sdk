"""Anthropic text editor tool (2025-07-28)."""

from __future__ import annotations

from pydantic import BaseModel

from ..anthropic_tools import textEditor_20250728


class TextEditor_20250728Args(BaseModel):
  maxCharacters: int | None = None


def textEditor_20250728ArgsSchema() -> type[TextEditor_20250728Args]:
  """Return args schema for text editor tool options."""

  return TextEditor_20250728Args


__all__ = ['textEditor_20250728', 'textEditor_20250728ArgsSchema']

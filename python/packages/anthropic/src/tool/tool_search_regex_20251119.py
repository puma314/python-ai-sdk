"""Anthropic regex-based tool-search tool (2025-11-19)."""

from __future__ import annotations

from pydantic import BaseModel

from ..anthropic_tools import toolSearchRegex_20251119


class ToolReference(BaseModel):
  type: str
  toolName: str


def toolSearchRegex_20251119OutputSchema() -> type[ToolReference]:
  return ToolReference


__all__ = ['toolSearchRegex_20251119', 'toolSearchRegex_20251119OutputSchema']

"""Anthropic BM25 tool-search tool (2025-11-19)."""

from __future__ import annotations

from pydantic import BaseModel

from ..anthropic_tools import toolSearchBm25_20251119


class ToolReference(BaseModel):
  type: str
  toolName: str


def toolSearchBm25_20251119OutputSchema() -> type[ToolReference]:
  return ToolReference


__all__ = ['toolSearchBm25_20251119', 'toolSearchBm25_20251119OutputSchema']

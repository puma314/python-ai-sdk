"""Anthropic web search tool (2025-03-05)."""

from __future__ import annotations

from pydantic import BaseModel

from ..anthropic_tools import webSearch_20250305


class WebSearch_20250305Args(BaseModel):
  maxUses: int | None = None
  allowedDomains: list[str] | None = None
  blockedDomains: list[str] | None = None
  userLocation: dict[str, str] | None = None


class WebSearchResult(BaseModel):
  url: str
  title: str | None
  pageAge: str | None
  encryptedContent: str
  type: str


def webSearch_20250305ArgsSchema() -> type[WebSearch_20250305Args]:
  return WebSearch_20250305Args


def webSearch_20250305OutputSchema() -> type[WebSearchResult]:
  return WebSearchResult


__all__ = [
  'webSearch_20250305',
  'webSearch_20250305ArgsSchema',
  'webSearch_20250305OutputSchema',
]

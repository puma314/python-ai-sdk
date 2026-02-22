"""Anthropic web fetch tool (2025-09-10)."""

from __future__ import annotations

from pydantic import BaseModel

from ..anthropic_tools import webFetch_20250910


class WebFetch_20250910Args(BaseModel):
  maxUses: int | None = None
  allowedDomains: list[str] | None = None
  blockedDomains: list[str] | None = None
  citations: dict[str, bool] | None = None
  maxContentTokens: int | None = None


class WebFetchResultSource(BaseModel):
  type: str
  mediaType: str
  data: str


class WebFetchResultContent(BaseModel):
  type: str
  title: str | None
  citations: dict[str, bool] | None = None
  source: WebFetchResultSource


class WebFetch_20250910Output(BaseModel):
  type: str
  url: str
  content: WebFetchResultContent
  retrievedAt: str | None


def webFetch_20250910ArgsSchema() -> type[WebFetch_20250910Args]:
  return WebFetch_20250910Args


def webFetch_20250910OutputSchema() -> type[WebFetch_20250910Output]:
  return WebFetch_20250910Output


__all__ = [
  'webFetch_20250910',
  'webFetch_20250910ArgsSchema',
  'webFetch_20250910OutputSchema',
]

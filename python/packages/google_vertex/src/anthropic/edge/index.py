"""
Auto-translated Python mirror for `src/anthropic/edge/index.ts`.
"""

from __future__ import annotations

from typing import Any, TypeAlias

try:
  from .google_vertex_anthropic_provider_edge import createVertexAnthropic, vertexAnthropic
except Exception:
  createVertexAnthropic: Any = None
  vertexAnthropic: Any = None

try:
  from .google_vertex_anthropic_provider_edge import GoogleVertexAnthropicProviderSettings, GoogleVertexAnthropicProvider
except Exception:
  GoogleVertexAnthropicProviderSettings: Any = None
  GoogleVertexAnthropicProvider: Any = None


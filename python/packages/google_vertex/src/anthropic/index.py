"""
Auto-translated Python mirror for `src/anthropic/index.ts`.
"""

from __future__ import annotations

from typing import Any, TypeAlias

try:
  from .google_vertex_anthropic_provider_node import vertexAnthropic, createVertexAnthropic
except Exception:
  vertexAnthropic: Any = None
  createVertexAnthropic: Any = None

try:
  from .google_vertex_anthropic_provider_node import GoogleVertexAnthropicProvider, GoogleVertexAnthropicProviderSettings
except Exception:
  GoogleVertexAnthropicProvider: Any = None
  GoogleVertexAnthropicProviderSettings: Any = None


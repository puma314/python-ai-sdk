"""
Auto-translated Python mirror for `src/edge/index.ts`.
"""

from __future__ import annotations

from typing import Any, TypeAlias

try:
  from .google_vertex_provider_edge import createVertex, vertex
except Exception:
  createVertex: Any = None
  vertex: Any = None

try:
  from .google_vertex_provider_edge import GoogleVertexProviderSettings, GoogleVertexProvider
except Exception:
  GoogleVertexProviderSettings: Any = None
  GoogleVertexProvider: Any = None


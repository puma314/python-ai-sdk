"""
Auto-translated Python mirror for `src/index.ts`.
"""

from __future__ import annotations

from typing import Any, TypeAlias

try:
  from .google_vertex_embedding_options import GoogleVertexEmbeddingModelOptions
except Exception:
  GoogleVertexEmbeddingModelOptions: Any = None

try:
  from .google_vertex_image_model import GoogleVertexImageModelOptions, GoogleVertexImageProviderOptions
except Exception:
  GoogleVertexImageModelOptions: Any = None
  GoogleVertexImageProviderOptions: Any = None

try:
  from .google_vertex_video_model import GoogleVertexVideoModelOptions, GoogleVertexVideoProviderOptions
except Exception:
  GoogleVertexVideoModelOptions: Any = None
  GoogleVertexVideoProviderOptions: Any = None

try:
  from .google_vertex_video_settings import GoogleVertexVideoModelId
except Exception:
  GoogleVertexVideoModelId: Any = None

try:
  from .google_vertex_provider_node import createVertex, vertex
except Exception:
  createVertex: Any = None
  vertex: Any = None

try:
  from .google_vertex_provider_node import GoogleVertexProvider, GoogleVertexProviderSettings
except Exception:
  GoogleVertexProvider: Any = None
  GoogleVertexProviderSettings: Any = None

try:
  from .version import VERSION
except Exception:
  VERSION: Any = None


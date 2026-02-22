"""
Auto-translated Python mirror for `src/middleware/index.ts`.
"""

from __future__ import annotations

from typing import Any, TypeAlias

try:
  from .default_embedding_settings_middleware import defaultEmbeddingSettingsMiddleware
except Exception:
  defaultEmbeddingSettingsMiddleware: Any = None

try:
  from .default_settings_middleware import defaultSettingsMiddleware
except Exception:
  defaultSettingsMiddleware: Any = None

try:
  from .extract_json_middleware import extractJsonMiddleware
except Exception:
  extractJsonMiddleware: Any = None

try:
  from .extract_reasoning_middleware import extractReasoningMiddleware
except Exception:
  extractReasoningMiddleware: Any = None

try:
  from .simulate_streaming_middleware import simulateStreamingMiddleware
except Exception:
  simulateStreamingMiddleware: Any = None

try:
  from .add_tool_input_examples_middleware import addToolInputExamplesMiddleware
except Exception:
  addToolInputExamplesMiddleware: Any = None

try:
  from .wrap_language_model import wrapLanguageModel
except Exception:
  wrapLanguageModel: Any = None

try:
  from .wrap_embedding_model import wrapEmbeddingModel
except Exception:
  wrapEmbeddingModel: Any = None

try:
  from .wrap_image_model import wrapImageModel
except Exception:
  wrapImageModel: Any = None

try:
  from .wrap_provider import wrapProvider
except Exception:
  wrapProvider: Any = None


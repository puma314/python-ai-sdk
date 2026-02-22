"""
Auto-translated Python mirror for `src/index.ts`.
"""

from __future__ import annotations

from typing import Any, TypeAlias

try:
  from .google_error import GoogleErrorData
except Exception:
  GoogleErrorData: Any = None

try:
  from .google_generative_ai_options import GoogleLanguageModelOptions, GoogleGenerativeAIProviderOptions
except Exception:
  GoogleLanguageModelOptions: Any = None
  GoogleGenerativeAIProviderOptions: Any = None

try:
  from .google_generative_ai_prompt import GoogleGenerativeAIProviderMetadata
except Exception:
  GoogleGenerativeAIProviderMetadata: Any = None

try:
  from .google_generative_ai_image_model import GoogleImageModelOptions, GoogleGenerativeAIImageProviderOptions
except Exception:
  GoogleImageModelOptions: Any = None
  GoogleGenerativeAIImageProviderOptions: Any = None

try:
  from .google_generative_ai_embedding_options import GoogleEmbeddingModelOptions, GoogleGenerativeAIEmbeddingProviderOptions
except Exception:
  GoogleEmbeddingModelOptions: Any = None
  GoogleGenerativeAIEmbeddingProviderOptions: Any = None

try:
  from .google_generative_ai_video_model import GoogleVideoModelOptions, GoogleGenerativeAIVideoProviderOptions
except Exception:
  GoogleVideoModelOptions: Any = None
  GoogleGenerativeAIVideoProviderOptions: Any = None

try:
  from .google_generative_ai_video_settings import GoogleGenerativeAIVideoModelId
except Exception:
  GoogleGenerativeAIVideoModelId: Any = None

try:
  from .google_provider import createGoogleGenerativeAI, google
except Exception:
  createGoogleGenerativeAI: Any = None
  google: Any = None

try:
  from .google_provider import GoogleGenerativeAIProvider, GoogleGenerativeAIProviderSettings
except Exception:
  GoogleGenerativeAIProvider: Any = None
  GoogleGenerativeAIProviderSettings: Any = None

try:
  from .version import VERSION
except Exception:
  VERSION: Any = None


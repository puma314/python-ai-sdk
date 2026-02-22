"""
Auto-translated Python mirror for `src/types/index.ts`.
"""

from __future__ import annotations

from typing import Any, TypeAlias

JSONSchema7: Any = None

try:
  from .embedding_model import Embedding, EmbeddingModel
except Exception:
  Embedding: Any = None
  EmbeddingModel: Any = None

try:
  from .embedding_model_middleware import EmbeddingModelMiddleware
except Exception:
  EmbeddingModelMiddleware: Any = None

try:
  from .image_model import ImageModel, ImageModelProviderMetadata
except Exception:
  ImageModel: Any = None
  ImageModelProviderMetadata: Any = None

try:
  from .image_model_middleware import ImageModelMiddleware
except Exception:
  ImageModelMiddleware: Any = None

try:
  from .image_model_response_metadata import ImageModelResponseMetadata
except Exception:
  ImageModelResponseMetadata: Any = None

try:
  from .json_value import JSONValue
except Exception:
  JSONValue: Any = None

try:
  from .language_model import CallWarning, FinishReason, LanguageModel, ToolChoice
except Exception:
  CallWarning: Any = None
  FinishReason: Any = None
  LanguageModel: Any = None
  ToolChoice: Any = None

try:
  from .language_model_middleware import LanguageModelMiddleware
except Exception:
  LanguageModelMiddleware: Any = None

try:
  from .language_model_request_metadata import LanguageModelRequestMetadata
except Exception:
  LanguageModelRequestMetadata: Any = None

try:
  from .language_model_response_metadata import LanguageModelResponseMetadata
except Exception:
  LanguageModelResponseMetadata: Any = None

try:
  from .provider import Provider
except Exception:
  Provider: Any = None

try:
  from .provider_metadata import ProviderMetadata
except Exception:
  ProviderMetadata: Any = None

try:
  from .reranking_model import RerankingModel
except Exception:
  RerankingModel: Any = None

try:
  from .speech_model import SpeechModel
except Exception:
  SpeechModel: Any = None

try:
  from .speech_model_response_metadata import SpeechModelResponseMetadata
except Exception:
  SpeechModelResponseMetadata: Any = None

try:
  from .transcription_model import TranscriptionModel
except Exception:
  TranscriptionModel: Any = None

try:
  from .transcription_model_response_metadata import TranscriptionModelResponseMetadata
except Exception:
  TranscriptionModelResponseMetadata: Any = None

try:
  from .usage import EmbeddingModelUsage, ImageModelUsage, LanguageModelUsage
except Exception:
  EmbeddingModelUsage: Any = None
  ImageModelUsage: Any = None
  LanguageModelUsage: Any = None

try:
  from .warning import Warning
except Exception:
  Warning: Any = None


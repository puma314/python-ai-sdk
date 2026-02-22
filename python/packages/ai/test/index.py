"""
Auto-translated Python mirror for `test/index.ts`.
"""

from __future__ import annotations

from typing import Any, TypeAlias

convertArrayToAsyncIterable: Any = None
convertArrayToReadableStream: Any = None
convertReadableStreamToArray: Any = None
mockId: Any = None

try:
  from ..src.test.mock_embedding_model_v3 import MockEmbeddingModelV3
except Exception:
  MockEmbeddingModelV3: Any = None

try:
  from ..src.test.mock_image_model_v3 import MockImageModelV3
except Exception:
  MockImageModelV3: Any = None

try:
  from ..src.test.mock_language_model_v3 import MockLanguageModelV3
except Exception:
  MockLanguageModelV3: Any = None

try:
  from ..src.test.mock_provider_v3 import MockProviderV3
except Exception:
  MockProviderV3: Any = None

try:
  from ..src.test.mock_speech_model_v3 import MockSpeechModelV3
except Exception:
  MockSpeechModelV3: Any = None

try:
  from ..src.test.mock_transcription_model_v3 import MockTranscriptionModelV3
except Exception:
  MockTranscriptionModelV3: Any = None

try:
  from ..src.test.mock_reranking_model_v3 import MockRerankingModelV3
except Exception:
  MockRerankingModelV3: Any = None

try:
  from ..src.test.mock_values import mockValues
except Exception:
  mockValues: Any = None

simulateReadableStream: Any = None

__all__ = ['simulateReadableStream']

"""Provider interface version 2."""

from __future__ import annotations

from typing import Protocol

from ...embedding_model.v2.embedding_model_v2 import EmbeddingModelV2
from ...image_model.v2.image_model_v2 import ImageModelV2
from ...language_model.v2.language_model_v2 import LanguageModelV2
from ...speech_model.v2.speech_model_v2 import SpeechModelV2
from ...transcription_model.v2.transcription_model_v2 import TranscriptionModelV2


class ProviderV2(Protocol):
  """Provider contract for v2 language/embedding/image/etc models."""

  def languageModel(self, modelId: str) -> LanguageModelV2: ...

  def textEmbeddingModel(self, modelId: str) -> EmbeddingModelV2[str]: ...

  def imageModel(self, modelId: str) -> ImageModelV2: ...

  def transcriptionModel(self, modelId: str) -> TranscriptionModelV2: ...

  def speechModel(self, modelId: str) -> SpeechModelV2: ...

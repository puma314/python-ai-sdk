"""Provider interface version 3."""

from __future__ import annotations

from typing import Literal, Protocol

from ...embedding_model.v3.embedding_model_v3 import EmbeddingModelV3
from ...image_model.v3.image_model_v3 import ImageModelV3
from ...language_model.v3.language_model_v3 import LanguageModelV3
from ...reranking_model.v3.reranking_model_v3 import RerankingModelV3
from ...speech_model.v3.speech_model_v3 import SpeechModelV3
from ...transcription_model.v3.transcription_model_v3 import TranscriptionModelV3


class ProviderV3(Protocol):
  specificationVersion: Literal['v3']

  def languageModel(self, modelId: str) -> LanguageModelV3: ...

  def embeddingModel(self, modelId: str) -> EmbeddingModelV3: ...

  def textEmbeddingModel(self, modelId: str) -> EmbeddingModelV3: ...

  def imageModel(self, modelId: str) -> ImageModelV3: ...

  def transcriptionModel(self, modelId: str) -> TranscriptionModelV3: ...

  def speechModel(self, modelId: str) -> SpeechModelV3: ...

  def rerankingModel(self, modelId: str) -> RerankingModelV3: ...

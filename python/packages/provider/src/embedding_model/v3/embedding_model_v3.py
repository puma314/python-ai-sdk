from __future__ import annotations

from typing import Awaitable, Protocol

from .embedding_model_v3_call_options import EmbeddingModelV3CallOptions
from .embedding_model_v3_result import EmbeddingModelV3Result


class EmbeddingModelV3(Protocol):
  specificationVersion: str
  provider: str
  modelId: str
  maxEmbeddingsPerCall: Awaitable[int | None] | int | None
  supportsParallelCalls: Awaitable[bool] | bool

  def doEmbed(
    self, options: EmbeddingModelV3CallOptions
  ) -> Awaitable[EmbeddingModelV3Result]: ...

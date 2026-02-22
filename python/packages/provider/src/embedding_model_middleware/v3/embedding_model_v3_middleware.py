from typing import Callable, NotRequired, TypedDict

from ...embedding_model.v3.embedding_model_v3 import EmbeddingModelV3
from ...embedding_model.v3.embedding_model_v3_call_options import (
  EmbeddingModelV3CallOptions,
)
from ...embedding_model.v3.embedding_model_v3_result import EmbeddingModelV3Result


class EmbeddingModelV3Middleware(TypedDict):
  specificationVersion: str
  overrideProvider: NotRequired[Callable[[dict[str, EmbeddingModelV3]], str]]
  overrideModelId: NotRequired[Callable[[dict[str, EmbeddingModelV3]], str]]
  overrideMaxEmbeddingsPerCall: NotRequired[
    Callable[[dict[str, EmbeddingModelV3]], int | None]
  ]
  overrideSupportsParallelCalls: NotRequired[
    Callable[[dict[str, EmbeddingModelV3]], bool]
  ]
  transformParams: NotRequired[
    Callable[[dict[str, object]], EmbeddingModelV3CallOptions]
  ]
  wrapEmbed: NotRequired[Callable[[dict[str, object]], EmbeddingModelV3Result]]

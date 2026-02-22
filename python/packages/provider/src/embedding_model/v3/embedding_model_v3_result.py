from typing import NotRequired, TypedDict

from ...shared.v3.shared_v3_headers import SharedV3Headers
from ...shared.v3.shared_v3_provider_metadata import SharedV3ProviderMetadata
from ...shared.v3.shared_v3_warning import SharedV3Warning
from .embedding_model_v3_embedding import EmbeddingModelV3Embedding


class EmbeddingModelV3Usage(TypedDict):
  tokens: int


class EmbeddingModelV3Response(TypedDict):
  headers: NotRequired[SharedV3Headers]
  body: NotRequired[object]


class EmbeddingModelV3Result(TypedDict):
  embeddings: list[EmbeddingModelV3Embedding]
  usage: NotRequired[EmbeddingModelV3Usage]
  providerMetadata: NotRequired[SharedV3ProviderMetadata]
  response: NotRequired[EmbeddingModelV3Response]
  warnings: list[SharedV3Warning]

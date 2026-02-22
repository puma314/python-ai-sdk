from __future__ import annotations

from typing import Awaitable, Generic, NotRequired, Protocol, TypeVar, TypedDict

from ...shared.v2.shared_v2_headers import SharedV2Headers
from ...shared.v2.shared_v2_provider_metadata import SharedV2ProviderMetadata
from ...shared.v2.shared_v2_provider_options import SharedV2ProviderOptions
from .embedding_model_v2_embedding import EmbeddingModelV2Embedding

VALUE = TypeVar('VALUE')


class EmbeddingModelV2CallOptions(TypedDict, Generic[VALUE]):
  values: list[VALUE]
  abortSignal: NotRequired[object]
  providerOptions: NotRequired[SharedV2ProviderOptions]
  headers: NotRequired[dict[str, str | None]]


class EmbeddingModelV2Usage(TypedDict):
  tokens: int


class EmbeddingModelV2Response(TypedDict):
  headers: NotRequired[SharedV2Headers]
  body: NotRequired[object]


class EmbeddingModelV2Result(TypedDict):
  embeddings: list[EmbeddingModelV2Embedding]
  usage: NotRequired[EmbeddingModelV2Usage]
  providerMetadata: NotRequired[SharedV2ProviderMetadata]
  response: NotRequired[EmbeddingModelV2Response]


class EmbeddingModelV2(Protocol, Generic[VALUE]):
  specificationVersion: str
  provider: str
  modelId: str
  maxEmbeddingsPerCall: Awaitable[int | None] | int | None
  supportsParallelCalls: Awaitable[bool] | bool

  def doEmbed(
    self, options: EmbeddingModelV2CallOptions[VALUE]
  ) -> Awaitable[EmbeddingModelV2Result]: ...

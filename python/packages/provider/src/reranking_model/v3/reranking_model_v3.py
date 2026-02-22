"""Reranking model specification version 3."""

from __future__ import annotations

from datetime import datetime
from typing import Awaitable, NotRequired, Protocol, TypedDict

from ...shared.v3.shared_v3_headers import SharedV3Headers
from ...shared.v3.shared_v3_provider_metadata import SharedV3ProviderMetadata
from ...shared.v3.shared_v3_warning import SharedV3Warning
from .reranking_model_v3_call_options import RerankingModelV3CallOptions


class RerankingModelV3RankingEntry(TypedDict):
  index: int
  relevanceScore: float


class RerankingModelV3Response(TypedDict):
  id: NotRequired[str]
  timestamp: NotRequired[datetime]
  modelId: NotRequired[str]
  headers: NotRequired[SharedV3Headers]
  body: NotRequired[object]


class RerankingModelV3Result(TypedDict):
  ranking: list[RerankingModelV3RankingEntry]
  providerMetadata: NotRequired[SharedV3ProviderMetadata]
  warnings: NotRequired[list[SharedV3Warning]]
  response: NotRequired[RerankingModelV3Response]


class RerankingModelV3(Protocol):
  specificationVersion: str
  provider: str
  modelId: str

  def doRerank(
    self, options: RerankingModelV3CallOptions
  ) -> Awaitable[RerankingModelV3Result]: ...

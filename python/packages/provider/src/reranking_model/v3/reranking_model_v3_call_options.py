"""Call options for reranking-model v3."""

from typing import Literal, NotRequired, TypedDict

from ...json_value.json_value import JSONObject
from ...shared.v3.shared_v3_headers import SharedV3Headers
from ...shared.v3.shared_v3_provider_options import SharedV3ProviderOptions


class RerankingModelV3TextDocuments(TypedDict):
  type: Literal['text']
  values: list[str]


class RerankingModelV3ObjectDocuments(TypedDict):
  type: Literal['object']
  values: list[JSONObject]


class RerankingModelV3CallOptions(TypedDict):
  documents: RerankingModelV3TextDocuments | RerankingModelV3ObjectDocuments
  query: str
  topN: NotRequired[int]
  abortSignal: NotRequired[object]
  providerOptions: NotRequired[SharedV3ProviderOptions]
  headers: NotRequired[SharedV3Headers]

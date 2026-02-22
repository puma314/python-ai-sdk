from __future__ import annotations

"""Reranking model V3 call options.

Translated from: packages/provider/src/reranking-model/v3/reranking-model-v3-call-options.ts
"""

import asyncio
from dataclasses import dataclass, field
from typing import Literal, Union

from ...json_value.json_value import JSONObject
from ...shared.v3 import SharedV3Headers, SharedV3ProviderOptions


@dataclass(frozen=True)
class TextDocuments:
    """Text-based documents for reranking."""

    type: Literal['text'] = 'text'
    values: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ObjectDocuments:
    """Object-based documents for reranking."""

    type: Literal['object'] = 'object'
    values: list[JSONObject] = field(default_factory=list)


Documents = Union[TextDocuments, ObjectDocuments]


@dataclass(frozen=True)
class RerankingModelV3CallOptions:
    """Options for reranking model V3 calls."""

    documents: Documents
    """Documents to rerank.
    Either a list of texts or a list of JSON objects.
    """

    query: str
    """The query is a string that represents the query to rerank the documents against."""

    top_n: int | None = None
    """Optional limit returned documents to the top n documents."""

    abort_signal: asyncio.Event | None = None
    """Abort signal for cancelling the operation."""

    provider_options: SharedV3ProviderOptions | None = None
    """Additional provider-specific options. They are passed through
    to the provider from the AI SDK and enable provider-specific
    functionality that can be fully encapsulated in the provider.
    """

    headers: SharedV3Headers | None = None
    """Additional HTTP headers to be sent with the request.
    Only applicable for HTTP-based providers.
    """

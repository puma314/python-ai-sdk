from __future__ import annotations

"""A source that has been used as input to generate the response.

Translated from: packages/provider/src/language-model/v2/language-model-v2-source.ts
"""

from dataclasses import dataclass
from typing import Literal, Union

from ai_sdk.provider.shared.v2.shared_v2_provider_metadata import (
    SharedV2ProviderMetadata,
)


@dataclass(frozen=True)
class LanguageModelV2UrlSource:
    """A URL source that references web content."""

    type: Literal['source'] = 'source'

    source_type: Literal['url'] = 'url'
    """The type of source - URL sources reference web content."""

    id: str = ''
    """The ID of the source."""

    url: str = ''
    """The URL of the source."""

    title: str | None = None
    """The title of the source."""

    provider_metadata: SharedV2ProviderMetadata | None = None
    """Additional provider metadata for the source."""


@dataclass(frozen=True)
class LanguageModelV2DocumentSource:
    """A document source that references files/documents."""

    type: Literal['source'] = 'source'

    source_type: Literal['document'] = 'document'
    """The type of source - document sources reference files/documents."""

    id: str = ''
    """The ID of the source."""

    media_type: str = ''
    """IANA media type of the document (e.g., 'application/pdf')."""

    title: str = ''
    """The title of the document."""

    filename: str | None = None
    """Optional filename of the document."""

    provider_metadata: SharedV2ProviderMetadata | None = None
    """Additional provider metadata for the source."""


LanguageModelV2Source = Union[LanguageModelV2UrlSource, LanguageModelV2DocumentSource]
"""A source that has been used as input to generate the response."""

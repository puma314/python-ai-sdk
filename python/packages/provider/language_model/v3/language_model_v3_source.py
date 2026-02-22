from __future__ import annotations

"""A source that has been used as input to generate the response.

Translated from: packages/provider/src/language-model/v3/language-model-v3-source.ts
"""

from dataclasses import dataclass
from typing import Literal, Union

from ai_sdk.provider.shared.v3.shared_v3_provider_metadata import (
    SharedV3ProviderMetadata,
)


@dataclass(frozen=True)
class LanguageModelV3UrlSource:
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

    provider_metadata: SharedV3ProviderMetadata | None = None
    """Additional provider metadata for the source."""


@dataclass(frozen=True)
class LanguageModelV3DocumentSource:
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

    provider_metadata: SharedV3ProviderMetadata | None = None
    """Additional provider metadata for the source."""


LanguageModelV3Source = Union[LanguageModelV3UrlSource, LanguageModelV3DocumentSource]
"""A source that has been used as input to generate the response."""

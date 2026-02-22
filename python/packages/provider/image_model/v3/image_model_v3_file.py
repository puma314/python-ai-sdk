from __future__ import annotations

"""An image file that can be used for image editing or variation generation.

Translated from: packages/provider/src/image-model/v3/image-model-v3-file.ts
"""

from dataclasses import dataclass, field
from typing import Literal, Union

from ai_sdk.provider.shared import SharedV3ProviderMetadata


@dataclass(frozen=True)
class ImageModelV3FileData:
    """An image file with inline data.

    An image file that can be used for image editing or variation generation,
    provided as base64 encoded strings or binary data.
    """

    type: Literal['file'] = 'file'

    media_type: str = ''
    """The IANA media type of the file, e.g. ``image/png``. Any string is supported.

    See https://www.iana.org/assignments/media-types/media-types.xhtml
    """

    data: str | bytes = b''
    """Generated file data as base64 encoded strings or binary data.

    The file data should be returned without any unnecessary conversion.
    If the API returns base64 encoded strings, the file data should be returned
    as base64 encoded strings. If the API returns binary data, the file data should
    be returned as binary data.
    """

    provider_options: SharedV3ProviderMetadata | None = field(default=None)
    """Optional provider-specific metadata for the file part."""


@dataclass(frozen=True)
class ImageModelV3FileUrl:
    """An image file referenced by URL.

    An image file that can be used for image editing or variation generation,
    provided as a URL reference.
    """

    type: Literal['url'] = 'url'

    url: str = ''
    """The URL of the image file."""

    provider_options: SharedV3ProviderMetadata | None = field(default=None)
    """Optional provider-specific metadata for the file part."""


ImageModelV3File = Union[ImageModelV3FileData, ImageModelV3FileUrl]
"""An image file that can be used for image editing or variation generation."""

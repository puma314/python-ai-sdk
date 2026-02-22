from __future__ import annotations

"""A video or image file for video editing or image-to-video generation.

Translated from: packages/provider/src/video-model/v3/video-model-v3-file.ts
"""

from dataclasses import dataclass, field
from typing import Literal, Union

from ai_sdk.provider.shared.v3.shared_v3_provider_metadata import (
    SharedV3ProviderMetadata,
)


@dataclass(frozen=True)
class VideoModelV3FileData:
    """A video or image file that can be used for video editing or image-to-video generation.

    Supports both image inputs (for image-to-video) and video inputs (for editing).
    This variant provides file data directly.
    """

    type: Literal['file'] = 'file'

    media_type: str = ''
    """The IANA media type of the file.

    Video types: 'video/mp4', 'video/webm', 'video/quicktime'
    Image types: 'image/png', 'image/jpeg', 'image/webp'
    """

    data: str | bytes = b''
    """File data as base64 encoded string or binary data."""

    provider_options: SharedV3ProviderMetadata | None = None
    """Optional provider-specific metadata for the file part."""


@dataclass(frozen=True)
class VideoModelV3FileUrl:
    """A video or image file referenced by URL.

    Supports both image inputs (for image-to-video) and video inputs (for editing).
    This variant provides a URL to the file.
    """

    type: Literal['url'] = 'url'

    url: str = ''
    """The URL of the video or image file."""

    provider_options: SharedV3ProviderMetadata | None = None
    """Optional provider-specific metadata for the file part."""


VideoModelV3File = Union[VideoModelV3FileData, VideoModelV3FileUrl]
"""A video or image file that can be used for video editing or image-to-video generation.

Supports both image inputs (for image-to-video) and video inputs (for editing).
"""

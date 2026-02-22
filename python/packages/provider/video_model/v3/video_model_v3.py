from __future__ import annotations

"""Video generation model specification version 3.

Translated from: packages/provider/src/video-model/v3/video-model-v3.ts
"""

import datetime
from collections.abc import Awaitable
from dataclasses import dataclass, field
from typing import Callable, Literal, Protocol, TypedDict, Union

from ...shared.v3.shared_v3_provider_metadata import (
    SharedV3ProviderMetadata,
)
from ...shared.v3.shared_v3_warning import SharedV3Warning
from .video_model_v3_call_options import (
    VideoModelV3CallOptions,
)


class GetMaxVideosPerCallOptions(TypedDict):
    """Options passed to the GetMaxVideosPerCallFunction."""

    model_id: str


GetMaxVideosPerCallFunction = Callable[
    [GetMaxVideosPerCallOptions], int | None | Awaitable[int | None]
]
"""Function type that returns the max number of videos per call.

Takes an options object with a model_id property and returns a number,
None, or an awaitable of those.
"""


@dataclass(frozen=True)
class VideoModelV3VideoDataUrl:
    """Video available as a URL (most common for video providers)."""

    type: Literal['url'] = 'url'
    url: str = ''
    media_type: str = ''


@dataclass(frozen=True)
class VideoModelV3VideoDataBase64:
    """Video as base64-encoded string."""

    type: Literal['base64'] = 'base64'
    data: str = ''
    media_type: str = ''


@dataclass(frozen=True)
class VideoModelV3VideoDataBinary:
    """Video as binary data."""

    type: Literal['binary'] = 'binary'
    data: bytes = b''
    media_type: str = ''


VideoModelV3VideoData = Union[
    VideoModelV3VideoDataUrl,
    VideoModelV3VideoDataBase64,
    VideoModelV3VideoDataBinary,
]
"""Generated video data. Can be a URL, base64-encoded string, or binary data."""


@dataclass(frozen=True)
class VideoModelV3GenerateResponseInfo:
    """Response information for telemetry and debugging purposes."""

    timestamp: datetime.datetime = field(
        default_factory=datetime.datetime.now
    )
    """Timestamp for the start of the generated response."""

    model_id: str = ''
    """The ID of the response model that was used to generate the response."""

    headers: dict[str, str] | None = None
    """Response headers."""


@dataclass(frozen=True)
class VideoModelV3GenerateResult:
    """Result of a video generation call."""

    videos: list[VideoModelV3VideoData] = field(default_factory=list)
    """Generated videos as URLs, base64 strings, or binary data.

    Most providers return URLs to video files (MP4, WebM) due to large file sizes.
    Use the discriminated union to indicate the type of video data being returned.
    """

    warnings: list[SharedV3Warning] = field(default_factory=list)
    """Warnings for the call, e.g. unsupported features."""

    provider_metadata: SharedV3ProviderMetadata | None = None
    """Additional provider-specific metadata. They are passed through
    from the provider to the AI SDK and enable provider-specific
    results that can be fully encapsulated in the provider.

    The outer record is keyed by the provider name, and the inner
    record is provider-specific metadata.

    Example::

        {
            "fal": {
                "videos": [{
                    "duration": 5.0,
                    "fps": 24,
                    "width": 1280,
                    "height": 720
                }]
            }
        }
    """

    response: VideoModelV3GenerateResponseInfo = field(
        default_factory=VideoModelV3GenerateResponseInfo
    )
    """Response information for telemetry and debugging purposes."""


class VideoModelV3(Protocol):
    """Video generation model specification version 3."""

    @property
    def specification_version(self) -> Literal['v3']:
        """The video model must specify which video model interface
        version it implements. This will allow us to evolve the video
        model interface and retain backwards compatibility. The different
        implementation versions can be handled as a discriminated union
        on our side.
        """
        ...

    @property
    def provider(self) -> str:
        """Name of the provider for logging purposes."""
        ...

    @property
    def model_id(self) -> str:
        """Provider-specific model ID for logging purposes."""
        ...

    @property
    def max_videos_per_call(
        self,
    ) -> int | None | GetMaxVideosPerCallFunction:
        """Limit of how many videos can be generated in a single API call.
        Can be set to a number for a fixed limit, to None to use
        the global limit, or a function that returns a number or None,
        optionally as an awaitable.

        Most video models only support generating 1 video at a time due to
        computational cost. Default is typically 1.
        """
        ...

    def do_generate(
        self, options: VideoModelV3CallOptions
    ) -> Awaitable[VideoModelV3GenerateResult]:
        """Generates an array of videos."""
        ...

from __future__ import annotations

"""Call options for video model v3.

Translated from: packages/provider/src/video-model/v3/video-model-v3-call-options.ts
"""

import asyncio
from dataclasses import dataclass, field
from typing import Any

from ...shared import SharedV3ProviderOptions
from .video_model_v3_file import VideoModelV3File


@dataclass(frozen=True)
class VideoModelV3CallOptions:
    """Call options for video model v3."""

    prompt: str | None = None
    """Text prompt for the video generation."""

    n: int = 1
    """Number of videos to generate. Default: 1.

    Most video models only support n=1 due to computational cost.
    """

    aspect_ratio: str | None = None
    """Aspect ratio of the videos to generate.

    Must have the format ``{width}:{height}``.
    None will use the provider's default aspect ratio.
    Common values: '16:9', '9:16', '1:1', '21:9', '4:3'
    """

    resolution: str | None = None
    """Resolution of the video to generate.

    Format: ``{width}x{height}`` (e.g., '1280x720', '1920x1080')
    None will use the provider's default resolution.
    """

    duration: float | None = None
    """Duration of the video in seconds.

    None will use the provider's default duration.
    Typically 3-10 seconds for most models.
    """

    fps: float | None = None
    """Frames per second (FPS) for the video.

    None will use the provider's default FPS.
    Common values: 24, 30, 60
    """

    seed: int | None = None
    """Seed for deterministic video generation.

    None will use a random seed.
    """

    image: VideoModelV3File | None = None
    """Input image for image-to-video generation.

    The image serves as the starting frame that the model will animate.
    """

    provider_options: SharedV3ProviderOptions = field(default_factory=dict)
    """Additional provider-specific options that are passed through to the provider
    as body parameters.

    Example::

        {
            "fal": {
                "loop": True,
                "motionStrength": 0.8
            }
        }
    """

    abort_signal: asyncio.Event | None = None
    """Abort signal for cancelling the operation."""

    headers: dict[str, str | None] | None = None
    """Additional HTTP headers to be sent with the request.

    Only applicable for HTTP-based providers.
    """

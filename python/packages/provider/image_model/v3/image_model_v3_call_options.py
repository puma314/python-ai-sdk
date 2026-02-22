from __future__ import annotations

"""Call options for image model v3.

Translated from: packages/provider/src/image-model/v3/image-model-v3-call-options.ts
"""

import asyncio
import re
from dataclasses import dataclass, field
from typing import Any

from .image_model_v3_file import ImageModelV3File
from ...shared import SharedV3ProviderOptions


def _validate_size(size: str) -> str:
    """Validate that size matches the pattern '{width}x{height}'."""
    if not re.fullmatch(r'\d+x\d+', size):
        raise ValueError(
            f"Invalid size format: {size!r}. Expected '{{width}}x{{height}}', e.g. '1024x768'."
        )
    return size


def _validate_aspect_ratio(aspect_ratio: str) -> str:
    """Validate that aspect_ratio matches the pattern '{width}:{height}'."""
    if not re.fullmatch(r'\d+:\d+', aspect_ratio):
        raise ValueError(
            f"Invalid aspect ratio format: {aspect_ratio!r}. Expected '{{width}}:{{height}}', e.g. '16:9'."
        )
    return aspect_ratio


@dataclass(frozen=True)
class ImageModelV3CallOptions:
    """Call options for image model v3."""

    prompt: str | None = None
    """Prompt for the image generation. Some operations, like upscaling, may not require a prompt."""

    n: int = 1
    """Number of images to generate."""

    size: str | None = None
    """Size of the images to generate.

    Must have the format ``{width}x{height}``.
    ``None`` will use the provider's default size.
    """

    aspect_ratio: str | None = None
    """Aspect ratio of the images to generate.

    Must have the format ``{width}:{height}``.
    ``None`` will use the provider's default aspect ratio.
    """

    seed: int | None = None
    """Seed for the image generation.

    ``None`` will use the provider's default seed.
    """

    files: list[ImageModelV3File] | None = None
    """Array of images for image editing or variation generation.

    The images should be provided as base64 encoded strings or binary data.
    """

    mask: ImageModelV3File | None = None
    """Mask image for inpainting operations.

    The mask should be provided as base64 encoded strings or binary data.
    """

    provider_options: SharedV3ProviderOptions = field(default_factory=dict)
    """Additional provider-specific options that are passed through to the provider
    as body parameters.

    The outer record is keyed by the provider name, and the inner
    record is keyed by the provider-specific metadata key.

    Example::

        {
            "openai": {
                "style": "vivid"
            }
        }
    """

    abort_signal: asyncio.Event | None = None
    """Abort signal for cancelling the operation."""

    headers: dict[str, str | None] | None = None
    """Additional HTTP headers to be sent with the request.

    Only applicable for HTTP-based providers.
    """

    def __post_init__(self) -> None:
        if self.size is not None:
            _validate_size(self.size)
        if self.aspect_ratio is not None:
            _validate_aspect_ratio(self.aspect_ratio)

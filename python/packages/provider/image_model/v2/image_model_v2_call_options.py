from __future__ import annotations

"""Image model v2 call options.

Translated from: packages/provider/src/image-model/v2/image-model-v2-call-options.ts
"""

import asyncio
from dataclasses import dataclass, field

from ai_sdk.provider.shared.v2.shared_v2_provider_options import SharedV2ProviderOptions


@dataclass(frozen=True)
class ImageModelV2CallOptions:
    """Options for image model v2 calls."""

    prompt: str
    """Prompt for the image generation."""

    n: int
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

    provider_options: SharedV2ProviderOptions = field(default_factory=dict)
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

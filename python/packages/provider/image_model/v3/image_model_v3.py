from __future__ import annotations

"""Image generation model specification version 3.

Translated from: packages/provider/src/image-model/v3/image-model-v3.ts
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Awaitable, Callable, Literal, Protocol, Union, runtime_checkable

from ai_sdk.provider.image_model.v3.image_model_v3_call_options import (
    ImageModelV3CallOptions,
)
from ai_sdk.provider.image_model.v3.image_model_v3_usage import ImageModelV3Usage
from ai_sdk.provider.json_value import JSONArray, JSONValue
from ai_sdk.provider.shared.v3.shared_v3_warning import SharedV3Warning

ImageModelV3ProviderMetadata = dict[str, Any]
"""Provider-specific metadata.

The outer record is keyed by the provider name, and the inner
record is provider-specific metadata. It always includes an
``images`` key with image-specific metadata.
"""

GetMaxImagesPerCallFunction = Callable[
    ..., int | None | Awaitable[int | None]
]
"""Function that returns the max images per call limit for a given model ID.

Takes a dict with a ``model_id`` key and returns a number, ``None``,
or an awaitable of the same.
"""


@dataclass(frozen=True)
class ImageModelV3GenerateResponse:
    """Response from an image model generation call."""

    images: list[str] | list[bytes]
    """Generated images as base64 encoded strings or binary data.

    The images should be returned without any unnecessary conversion.
    If the API returns base64 encoded strings, the images should be returned
    as base64 encoded strings. If the API returns binary data, the images should
    be returned as binary data.
    """

    warnings: list[SharedV3Warning] = field(default_factory=list)
    """Warnings for the call, e.g. unsupported features."""

    provider_metadata: ImageModelV3ProviderMetadata | None = None
    """Additional provider-specific metadata. They are passed through
    from the provider to the AI SDK and enable provider-specific
    results that can be fully encapsulated in the provider.

    The outer record is keyed by the provider name, and the inner
    record is provider-specific metadata. It always includes an
    ``images`` key with image-specific metadata.

    Example::

        {
            "openai": {
                "images": [{"revisedPrompt": "Revised prompt here."}]
            }
        }
    """

    response: ImageModelV3ResponseMetadata = field(
        default_factory=lambda: ImageModelV3ResponseMetadata(
            timestamp=datetime.now(),
            model_id="",
            headers=None,
        )
    )
    """Response information for telemetry and debugging purposes."""

    usage: ImageModelV3Usage | None = None
    """Optional token usage for the image generation call (if the provider reports it)."""


@dataclass(frozen=True)
class ImageModelV3ResponseMetadata:
    """Response metadata for an image model generation call."""

    timestamp: datetime
    """Timestamp for the start of the generated response."""

    model_id: str
    """The ID of the response model that was used to generate the response."""

    headers: dict[str, str] | None
    """Response headers."""


@runtime_checkable
class ImageModelV3(Protocol):
    """Image generation model specification version 3."""

    @property
    def specification_version(self) -> Literal['v3']:
        """The image model must specify which image model interface
        version it implements. This will allow us to evolve the image
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
    def max_images_per_call(
        self,
    ) -> int | None | GetMaxImagesPerCallFunction:
        """Limit of how many images can be generated in a single API call.

        Can be set to a number for a fixed limit, to ``None`` to use
        the global limit, or a function that returns a number or ``None``,
        optionally as a coroutine.
        """
        ...

    async def do_generate(
        self, options: ImageModelV3CallOptions
    ) -> ImageModelV3GenerateResponse:
        """Generates an array of images."""
        ...

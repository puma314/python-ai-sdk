from __future__ import annotations

"""Image model v2 specification.

Translated from: packages/provider/src/image-model/v2/image-model-v2.ts
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Awaitable, Literal, Protocol, runtime_checkable

from .image_model_v2_call_options import (
    ImageModelV2CallOptions,
)
from .image_model_v2_call_warning import (
    ImageModelV2CallWarning,
)
from ...json_value import JSONArray, JSONValue

ImageModelV2ProviderMetadata = dict[str, JSONValue]
"""Provider metadata keyed by provider name.

Each value contains an ``images`` key with image-specific metadata,
along with any additional provider-specific JSON values.
"""


@dataclass(frozen=True)
class _GetMaxImagesPerCallOptions:
    """Options passed to the GetMaxImagesPerCallFunction."""

    model_id: str


@runtime_checkable
class _GetMaxImagesPerCallFunction(Protocol):
    """Callable that resolves the max images per call for a given model."""

    def __call__(
        self, options: _GetMaxImagesPerCallOptions
    ) -> int | None | Awaitable[int | None]: ...


@dataclass(frozen=True)
class ImageModelV2GenerateResponseInfo:
    """Response information for telemetry and debugging purposes."""

    timestamp: datetime
    """Timestamp for the start of the generated response."""

    model_id: str
    """The ID of the response model that was used to generate the response."""

    headers: dict[str, str] | None = None
    """Response headers."""


@dataclass(frozen=True)
class ImageModelV2GenerateResult:
    """Result returned from ``ImageModelV2.do_generate``."""

    images: list[str] | list[bytes]
    """Generated images as base64 encoded strings or binary data.

    The images should be returned without any unnecessary conversion.
    If the API returns base64 encoded strings, the images should be returned
    as base64 encoded strings. If the API returns binary data, the images should
    be returned as binary data.
    """

    warnings: list[ImageModelV2CallWarning]
    """Warnings for the call, e.g. unsupported settings."""

    response: ImageModelV2GenerateResponseInfo
    """Response information for telemetry and debugging purposes."""

    provider_metadata: ImageModelV2ProviderMetadata | None = None
    """Additional provider-specific metadata. They are passed through
    from the provider to the AI SDK and enable provider-specific
    results that can be fully encapsulated in the provider.

    The outer record is keyed by the provider name, and the inner
    record is provider-specific metadata. It always includes an
    ``images`` key with image-specific metadata.

    Example::

        {
            "openai": {
                "images": ["revisedPrompt": "Revised prompt here."]
            }
        }
    """


@runtime_checkable
class ImageModelV2(Protocol):
    """Image generation model specification version 2."""

    @property
    def specification_version(self) -> Literal['v2']:
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
    ) -> int | None | _GetMaxImagesPerCallFunction:
        """Limit of how many images can be generated in a single API call.

        Can be set to a number for a fixed limit, to None to use
        the global limit, or a function that returns a number or None,
        optionally as an awaitable.
        """
        ...

    def do_generate(
        self, options: ImageModelV2CallOptions
    ) -> Awaitable[ImageModelV2GenerateResult]:
        """Generates an array of images."""
        ...

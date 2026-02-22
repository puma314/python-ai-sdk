from __future__ import annotations

"""Middleware for ImageModelV3.

Translated from: packages/provider/src/image-model-middleware/v3/image-model-v3-middleware.ts
"""

from typing import Awaitable, Callable, Literal, Protocol, runtime_checkable

from ai_sdk.provider.image_model.v3.image_model_v3 import (
    ImageModelV3,
    ImageModelV3GenerateResponse,
    GetMaxImagesPerCallFunction,
)
from ai_sdk.provider.image_model.v3.image_model_v3_call_options import (
    ImageModelV3CallOptions,
)


@runtime_checkable
class ImageModelV3Middleware(Protocol):
    """Middleware for ImageModelV3.

    This type defines the structure for middleware that can be used to modify
    the behavior of ImageModelV3 operations.
    """

    @property
    def specification_version(self) -> Literal['v3']:
        """Middleware specification version. Use ``v3`` for the current version."""
        ...

    def override_provider(
        self, *, model: ImageModelV3
    ) -> str | None:
        """Override the provider name if desired.

        Args:
            model: The image model instance.
        """
        ...

    def override_model_id(
        self, *, model: ImageModelV3
    ) -> str | None:
        """Override the model ID if desired.

        Args:
            model: The image model instance.
        """
        ...

    def override_max_images_per_call(
        self, *, model: ImageModelV3
    ) -> int | None | GetMaxImagesPerCallFunction | None:
        """Override the limit of how many images can be generated in a single API call if desired.

        Args:
            model: The image model instance.
        """
        ...

    def transform_params(
        self,
        *,
        params: ImageModelV3CallOptions,
        model: ImageModelV3,
    ) -> Awaitable[ImageModelV3CallOptions] | None:
        """Transform the parameters before they are passed to the image model.

        Args:
            params: The original parameters for the image model call.
            model: The image model instance.

        Returns:
            A coroutine that resolves to the transformed parameters.
        """
        ...

    def wrap_generate(
        self,
        *,
        do_generate: Callable[[], Awaitable[ImageModelV3GenerateResponse]],
        params: ImageModelV3CallOptions,
        model: ImageModelV3,
    ) -> Awaitable[ImageModelV3GenerateResponse] | None:
        """Wrap the generate operation of the image model.

        Args:
            do_generate: The original generate function.
            params: The parameters for the generate call. If the
                ``transform_params`` middleware is used, this will be the
                transformed parameters.
            model: The image model instance.

        Returns:
            A coroutine that resolves to the result of the generate operation.
        """
        ...

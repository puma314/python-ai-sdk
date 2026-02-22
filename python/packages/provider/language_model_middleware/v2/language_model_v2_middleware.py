from __future__ import annotations

"""Experimental middleware for LanguageModelV2.

This type defines the structure for middleware that can be used to modify
the behavior of LanguageModelV2 operations.

Translated from: packages/provider/src/language-model-middleware/v2/language-model-v2-middleware.ts
"""

import re
from dataclasses import dataclass
from typing import Awaitable, Callable, Literal

from ...language_model.v2.language_model_v2 import (
    LanguageModelV2,
    LanguageModelV2GenerateResult,
    LanguageModelV2StreamResult,
)
from ...language_model.v2.language_model_v2_call_options import LanguageModelV2CallOptions


@dataclass(frozen=True)
class LanguageModelV2Middleware:
    """Experimental middleware for LanguageModelV2.

    This type defines the structure for middleware that can be used to modify
    the behavior of LanguageModelV2 operations.

    All hook fields are optional. A middleware with only ``middleware_version``
    set to ``'v2'`` is fully valid.
    """

    middleware_version: Literal['v2'] | None = None
    """Middleware specification version. Use ``v2`` for the current version."""
    # backwards compatibility

    override_provider: Callable[[LanguageModelV2], str] | None = None
    """Override the provider name if desired.

    Called with the language model instance and should return the new provider name.
    """

    override_model_id: Callable[[LanguageModelV2], str] | None = None
    """Override the model ID if desired.

    Called with the language model instance and should return the new model ID.
    """

    override_supported_urls: (
        Callable[
            [LanguageModelV2],
            Awaitable[dict[str, list[re.Pattern[str]]]] | dict[str, list[re.Pattern[str]]],
        ]
        | None
    ) = None
    """Override the supported URLs if desired.

    Called with the language model instance.
    """

    transform_params: (
        Callable[
            [Literal['generate', 'stream'], LanguageModelV2CallOptions, LanguageModelV2],
            Awaitable[LanguageModelV2CallOptions],
        ]
        | None
    ) = None
    """Transform the parameters before they are passed to the language model.

    Called with:
        type: The type of operation ('generate' or 'stream').
        params: The original parameters for the language model call.
        model: The language model instance.

    Returns a promise that resolves to the transformed parameters.
    """

    wrap_generate: (
        Callable[
            [
                Callable[[], Awaitable[LanguageModelV2GenerateResult]],
                Callable[[], Awaitable[LanguageModelV2StreamResult]],
                LanguageModelV2CallOptions,
                LanguageModelV2,
            ],
            Awaitable[LanguageModelV2GenerateResult],
        ]
        | None
    ) = None
    """Wrap the generate operation of the language model.

    Called with:
        do_generate: The original generate function.
        do_stream: The original stream function.
        params: The parameters for the generate call. If the
            ``transform_params`` middleware is used, this will be the
            transformed parameters.
        model: The language model instance.

    Returns a promise that resolves to the result of the generate operation.
    """

    wrap_stream: (
        Callable[
            [
                Callable[[], Awaitable[LanguageModelV2GenerateResult]],
                Callable[[], Awaitable[LanguageModelV2StreamResult]],
                LanguageModelV2CallOptions,
                LanguageModelV2,
            ],
            Awaitable[LanguageModelV2StreamResult],
        ]
        | None
    ) = None
    """Wrap the stream operation of the language model.

    Called with:
        do_generate: The original generate function.
        do_stream: The original stream function.
        params: The parameters for the stream call. If the
            ``transform_params`` middleware is used, this will be the
            transformed parameters.
        model: The language model instance.

    Returns a promise that resolves to the result of the stream operation.
    """

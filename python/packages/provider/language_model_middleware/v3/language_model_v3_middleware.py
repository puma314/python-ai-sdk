from __future__ import annotations

"""Experimental middleware for LanguageModelV3.

This type defines the structure for middleware that can be used to modify
the behavior of LanguageModelV3 operations.

Translated from: packages/provider/src/language-model-middleware/v3/language-model-v3-middleware.ts
"""

import re
from dataclasses import dataclass
from typing import Awaitable, Callable, Literal

from ...language_model.v3.language_model_v3 import LanguageModelV3
from ...language_model.v3.language_model_v3_call_options import LanguageModelV3CallOptions
from ...language_model.v3.language_model_v3_generate_result import LanguageModelV3GenerateResult
from ...language_model.v3.language_model_v3_stream_result import LanguageModelV3StreamResult


@dataclass(frozen=True)
class LanguageModelV3Middleware:
    """Experimental middleware for LanguageModelV3.

    This type defines the structure for middleware that can be used to modify
    the behavior of LanguageModelV3 operations.

    All hook fields are optional. A middleware with only ``specification_version``
    set to ``'v3'`` is fully valid.
    """

    specification_version: Literal['v3'] = 'v3'
    """Middleware specification version. Use ``v3`` for the current version."""

    override_provider: Callable[[LanguageModelV3], str] | None = None
    """Override the provider name if desired.

    Called with the language model instance and should return the new provider name.
    """

    override_model_id: Callable[[LanguageModelV3], str] | None = None
    """Override the model ID if desired.

    Called with the language model instance and should return the new model ID.
    """

    override_supported_urls: (
        Callable[
            [LanguageModelV3],
            Awaitable[dict[str, list[re.Pattern[str]]]] | dict[str, list[re.Pattern[str]]],
        ]
        | None
    ) = None
    """Override the supported URLs if desired.

    Called with the language model instance.
    """

    transform_params: (
        Callable[
            [Literal['generate', 'stream'], LanguageModelV3CallOptions, LanguageModelV3],
            Awaitable[LanguageModelV3CallOptions],
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
                Callable[[], Awaitable[LanguageModelV3GenerateResult]],
                Callable[[], Awaitable[LanguageModelV3StreamResult]],
                LanguageModelV3CallOptions,
                LanguageModelV3,
            ],
            Awaitable[LanguageModelV3GenerateResult],
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
                Callable[[], Awaitable[LanguageModelV3GenerateResult]],
                Callable[[], Awaitable[LanguageModelV3StreamResult]],
                LanguageModelV3CallOptions,
                LanguageModelV3,
            ],
            Awaitable[LanguageModelV3StreamResult],
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

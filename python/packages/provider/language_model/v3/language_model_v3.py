from __future__ import annotations

"""Specification for a language model that implements the language model interface version 3.

Translated from: packages/provider/src/language-model/v3/language-model-v3.ts
"""

import re
from collections.abc import Awaitable
from typing import Literal, Protocol, runtime_checkable

from .language_model_v3_call_options import LanguageModelV3CallOptions
from .language_model_v3_generate_result import LanguageModelV3GenerateResult
from .language_model_v3_stream_result import LanguageModelV3StreamResult


@runtime_checkable
class LanguageModelV3(Protocol):
    """Specification for a language model that implements the language model interface version 3."""

    @property
    def specification_version(self) -> Literal['v3']:
        """The language model must specify which language model interface version it implements."""
        ...

    @property
    def provider(self) -> str:
        """Provider ID."""
        ...

    @property
    def model_id(self) -> str:
        """Provider-specific model ID."""
        ...

    @property
    def supported_urls(
        self,
    ) -> Awaitable[dict[str, list[re.Pattern[str]]]] | dict[str, list[re.Pattern[str]]]:
        """Supported URL patterns by media type for the provider.

        The keys are media type patterns or full media types (e.g. ``*/*`` for
        everything, ``audio/*``, ``video/*``, or ``application/pdf``) and the
        values are arrays of regular expressions that match the URL paths.

        The matching should be against lower-case URLs.

        Matched URLs are supported natively by the model and are not downloaded.

        Returns:
            A map of supported URL patterns by media type (as an awaitable or a
            plain object).
        """
        ...

    def do_generate(
        self,
        options: LanguageModelV3CallOptions,
    ) -> Awaitable[LanguageModelV3GenerateResult]:
        """Generate a language model output (non-streaming).

        Naming: "do" prefix to prevent accidental direct usage of the method
        by the user.
        """
        ...

    def do_stream(
        self,
        options: LanguageModelV3CallOptions,
    ) -> Awaitable[LanguageModelV3StreamResult]:
        """Generate a language model output (streaming).

        Naming: "do" prefix to prevent accidental direct usage of the method
        by the user.

        Returns:
            A stream of higher-level language model output parts.
        """
        ...

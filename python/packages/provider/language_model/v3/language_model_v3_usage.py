from __future__ import annotations

"""Usage information for a language model call.

Translated from: packages/provider/src/language-model/v3/language-model-v3-usage.ts
"""

from dataclasses import dataclass

from ai_sdk.provider.json_value.json_value import JSONObject


@dataclass(frozen=True)
class LanguageModelV3InputTokenUsage:
    """Information about the input tokens."""

    total: int | None = None
    """The total number of input (prompt) tokens used."""

    no_cache: int | None = None
    """The number of non-cached input (prompt) tokens used."""

    cache_read: int | None = None
    """The number of cached input (prompt) tokens read."""

    cache_write: int | None = None
    """The number of cached input (prompt) tokens written."""


@dataclass(frozen=True)
class LanguageModelV3OutputTokenUsage:
    """Information about the output tokens."""

    total: int | None = None
    """The total number of output (completion) tokens used."""

    text: int | None = None
    """The number of text tokens used."""

    reasoning: int | None = None
    """The number of reasoning tokens used."""


@dataclass(frozen=True)
class LanguageModelV3Usage:
    """Usage information for a language model call."""

    input_tokens: LanguageModelV3InputTokenUsage = LanguageModelV3InputTokenUsage()
    """Information about the input tokens."""

    output_tokens: LanguageModelV3OutputTokenUsage = LanguageModelV3OutputTokenUsage()
    """Information about the output tokens."""

    raw: JSONObject | None = None
    """Raw usage information from the provider.

    This is the usage information in the shape that the provider returns.
    It can include additional information that is not part of the standard usage information.
    """

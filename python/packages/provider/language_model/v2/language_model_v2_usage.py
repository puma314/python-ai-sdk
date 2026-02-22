from __future__ import annotations

"""Usage information for a language model call.

Translated from: packages/provider/src/language-model/v2/language-model-v2-usage.ts
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class LanguageModelV2Usage:
    """Usage information for a language model call.

    If your API returns additional usage information, you can add it to the
    provider metadata under your provider's key.
    """

    input_tokens: int | None = None
    """The number of input (prompt) tokens used."""

    output_tokens: int | None = None
    """The number of output (completion) tokens used."""

    total_tokens: int | None = None
    """The total number of tokens as reported by the provider.

    This number might be different from the sum of ``input_tokens`` and
    ``output_tokens`` and e.g. include reasoning tokens or other overhead.
    """

    reasoning_tokens: int | None = None
    """The number of reasoning tokens used."""

    cached_input_tokens: int | None = None
    """The number of cached input tokens."""

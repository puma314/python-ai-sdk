from __future__ import annotations

"""Usage information for image model calls.

Translated from: packages/provider/src/image-model/v3/image-model-v3-usage.ts
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ImageModelV3Usage:
    """Usage information for an image model call."""

    input_tokens: int | None = None
    """The number of input (prompt) tokens used."""

    output_tokens: int | None = None
    """The number of output tokens used, if reported by the provider."""

    total_tokens: int | None = None
    """The total number of tokens as reported by the provider."""

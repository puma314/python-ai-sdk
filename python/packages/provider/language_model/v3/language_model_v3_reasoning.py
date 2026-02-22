from __future__ import annotations

"""Reasoning that the model has generated.

Translated from: packages/provider/src/language-model/v3/language-model-v3-reasoning.ts
"""

from dataclasses import dataclass, field
from typing import Literal

from ...shared.v3.shared_v3_provider_metadata import SharedV3ProviderMetadata


@dataclass(frozen=True)
class LanguageModelV3Reasoning:
    """Reasoning that the model has generated."""

    type: Literal['reasoning'] = 'reasoning'
    text: str = ''

    provider_metadata: SharedV3ProviderMetadata | None = None
    """Optional provider-specific metadata for the reasoning part."""

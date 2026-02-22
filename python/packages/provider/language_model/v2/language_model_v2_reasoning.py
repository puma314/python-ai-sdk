from __future__ import annotations
"""Reasoning that the model has generated.

Translated from: packages/provider/src/language-model/v2/language-model-v2-reasoning.ts
"""

from dataclasses import dataclass, field
from typing import Literal

from ...shared.v2.shared_v2_provider_metadata import SharedV2ProviderMetadata


@dataclass(frozen=True)
class LanguageModelV2Reasoning:
    """Reasoning that the model has generated."""

    type: Literal['reasoning'] = 'reasoning'
    text: str = ''

    provider_metadata: SharedV2ProviderMetadata | None = None
    """Optional provider-specific metadata for the reasoning part."""

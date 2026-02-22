from __future__ import annotations

"""Text that the model has generated.

Translated from: packages/provider/src/language-model/v3/language-model-v3-text.ts
"""

from dataclasses import dataclass
from typing import Literal

from ...shared.v3.shared_v3_provider_metadata import SharedV3ProviderMetadata


@dataclass(frozen=True)
class LanguageModelV3Text:
    """Text that the model has generated."""

    type: Literal['text'] = 'text'

    # The text content.
    text: str = ''

    provider_metadata: SharedV3ProviderMetadata | None = None

from __future__ import annotations

"""Text that the model has generated.

Translated from: packages/provider/src/language-model/v2/language-model-v2-text.ts
"""

from dataclasses import dataclass, field
from typing import Literal

from ...shared.v2.shared_v2_provider_metadata import (
    SharedV2ProviderMetadata,
)


@dataclass(frozen=True)
class LanguageModelV2Text:
    """Text that the model has generated."""

    type: Literal['text'] = 'text'

    # The text content.
    text: str = ''

    provider_metadata: SharedV2ProviderMetadata | None = None

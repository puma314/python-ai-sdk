from __future__ import annotations

"""Language model v3 response metadata.

Translated from: packages/provider/src/language-model/v3/language-model-v3-response-metadata.ts
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class LanguageModelV3ResponseMetadata:
    """Metadata for a language model v3 response."""

    id: str | None = None
    """ID for the generated response, if the provider sends one."""

    timestamp: datetime | None = None
    """Timestamp for the start of the generated response, if the provider sends one."""

    model_id: str | None = None
    """The ID of the response model that was used to generate the response, if the provider sends one."""

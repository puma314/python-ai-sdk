from __future__ import annotations

"""Language model v2 response metadata.

Translated from: packages/provider/src/language-model/v2/language-model-v2-response-metadata.ts
"""

from datetime import datetime
from typing import TypedDict


class LanguageModelV2ResponseMetadata(TypedDict, total=False):
    """Metadata for a language model v2 response."""

    id: str
    """ID for the generated response, if the provider sends one."""

    timestamp: datetime
    """Timestamp for the start of the generated response, if the provider sends one."""

    model_id: str
    """The ID of the response model that was used to generate the response, if the provider sends one."""

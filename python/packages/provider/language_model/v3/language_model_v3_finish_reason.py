from __future__ import annotations

"""Reason why a language model finished generating a response.

Contains both a unified finish reason and a raw finish reason from the provider.
The unified finish reason is used to provide a consistent finish reason across different providers.
The raw finish reason is used to provide the original finish reason from the provider.

Translated from: packages/provider/src/language-model/v3/language-model-v3-finish-reason.ts
"""

from dataclasses import dataclass
from typing import Literal


# Unified finish reason type. This enables using the same finish reason across different providers.
#
# Can be one of the following:
# - `stop`: model generated stop sequence
# - `length`: model generated maximum number of tokens
# - `content-filter`: content filter violation stopped the model
# - `tool-calls`: model triggered tool calls
# - `error`: model stopped because of an error
# - `other`: model stopped for other reasons
UnifiedFinishReason = Literal[
    "stop",
    "length",
    "content-filter",
    "tool-calls",
    "error",
    "other",
]


@dataclass(frozen=True)
class LanguageModelV3FinishReason:
    """Reason why a language model finished generating a response.

    Contains both a unified finish reason and a raw finish reason from the provider.
    The unified finish reason is used to provide a consistent finish reason across
    different providers. The raw finish reason is used to provide the original finish
    reason from the provider.
    """

    unified: UnifiedFinishReason
    """Unified finish reason. This enables using the same finish reason across different providers.

    Can be one of the following:
    - ``stop``: model generated stop sequence
    - ``length``: model generated maximum number of tokens
    - ``content-filter``: content filter violation stopped the model
    - ``tool-calls``: model triggered tool calls
    - ``error``: model stopped because of an error
    - ``other``: model stopped for other reasons
    """

    raw: str | None = None
    """Raw finish reason from the provider.

    This is the original finish reason from the provider.
    """

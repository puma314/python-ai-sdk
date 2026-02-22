from __future__ import annotations
"""Public API for transcription model.

Translated from: packages/provider/src/transcription-model/index.ts
"""

from .v2 import (
    TranscriptionModelV2,
    TranscriptionModelV2CallOptions,
    TranscriptionModelV2CallWarning,
)
from .v3 import (
    TranscriptionModelV3,
    TranscriptionModelV3CallOptions,
)

__all__ = [
    "TranscriptionModelV2",
    "TranscriptionModelV2CallOptions",
    "TranscriptionModelV2CallWarning",
    "TranscriptionModelV3",
    "TranscriptionModelV3CallOptions",
]

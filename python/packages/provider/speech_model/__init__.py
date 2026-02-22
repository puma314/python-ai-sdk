from __future__ import annotations

"""Public API for speech model.

Translated from: packages/provider/src/speech-model/index.ts
"""

from .v2 import SpeechModelV2, SpeechModelV2CallOptions, SpeechModelV2CallWarning
from .v3 import SpeechModelV3, SpeechModelV3CallOptions

__all__ = [
    "SpeechModelV2",
    "SpeechModelV2CallOptions",
    "SpeechModelV2CallWarning",
    "SpeechModelV3",
    "SpeechModelV3CallOptions",
]

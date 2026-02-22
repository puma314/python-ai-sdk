from __future__ import annotations
"""Public API for speech model v2.

Translated from: packages/provider/src/speech-model/v2/index.ts
"""

from .speech_model_v2 import SpeechModelV2
from .speech_model_v2_call_options import SpeechModelV2CallOptions
from .speech_model_v2_call_warning import SpeechModelV2CallWarning

__all__ = [
    "SpeechModelV2",
    "SpeechModelV2CallOptions",
    "SpeechModelV2CallWarning",
]

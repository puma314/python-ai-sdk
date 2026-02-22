from __future__ import annotations
"""Speech model V2 call warning type definitions.

Translated from: packages/provider/src/speech-model/v2/speech-model-v2-call-warning.ts
"""

from dataclasses import dataclass
from typing import Literal, Union


@dataclass(frozen=True)
class SpeechModelV2CallWarningUnsupportedSetting:
    """Warning for an unsupported setting.

    Warning from the model provider for this call. The call will proceed, but e.g.
    some settings might not be supported, which can lead to suboptimal results.
    """

    type: Literal['unsupported-setting'] = 'unsupported-setting'
    setting: Literal[
        'text',
        'voice',
        'output_format',
        'instructions',
        'speed',
        'language',
        'provider_options',
        'abort_signal',
        'headers',
    ] = 'text'
    details: str | None = None


@dataclass(frozen=True)
class SpeechModelV2CallWarningOther:
    """Warning of type 'other'.

    Warning from the model provider for this call. The call will proceed, but e.g.
    some settings might not be supported, which can lead to suboptimal results.
    """

    type: Literal['other'] = 'other'
    message: str = ''


SpeechModelV2CallWarning = Union[
    SpeechModelV2CallWarningUnsupportedSetting,
    SpeechModelV2CallWarningOther,
]
"""Warning from the model provider for this call. The call will proceed, but e.g.
some settings might not be supported, which can lead to suboptimal results.
"""

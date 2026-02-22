from __future__ import annotations

"""Transcription model v2 call warning types.

Translated from: packages/provider/src/transcription-model/v2/transcription-model-v2-call-warning.ts
"""

from dataclasses import dataclass
from typing import Literal, Union


@dataclass(frozen=True)
class TranscriptionModelV2CallWarningUnsupportedSetting:
    """Warning from the model provider for this call. The call will proceed, but e.g.
    some settings might not be supported, which can lead to suboptimal results.
    """

    type: Literal['unsupported-setting'] = 'unsupported-setting'
    setting: Literal[
        'audio', 'media_type', 'provider_options', 'abort_signal', 'headers'
    ] = 'audio'
    details: str | None = None


@dataclass(frozen=True)
class TranscriptionModelV2CallWarningOther:
    """Warning from the model provider for this call. The call will proceed, but e.g.
    some settings might not be supported, which can lead to suboptimal results.
    """

    type: Literal['other'] = 'other'
    message: str = ''


TranscriptionModelV2CallWarning = Union[
    TranscriptionModelV2CallWarningUnsupportedSetting,
    TranscriptionModelV2CallWarningOther,
]

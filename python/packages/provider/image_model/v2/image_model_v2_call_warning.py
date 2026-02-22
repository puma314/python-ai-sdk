from __future__ import annotations

"""Image model v2 call warning types.

Translated from: packages/provider/src/image-model/v2/image-model-v2-call-warning.ts
"""

from dataclasses import dataclass
from typing import Literal, Union


@dataclass(frozen=True)
class ImageModelV2CallWarningUnsupportedSetting:
    """Warning from the model provider for this call. The call will proceed, but e.g.
    some settings might not be supported, which can lead to suboptimal results.
    """

    type: Literal['unsupported-setting'] = 'unsupported-setting'
    setting: Literal[
        'prompt',
        'n',
        'size',
        'aspect_ratio',
        'seed',
        'provider_options',
        'abort_signal',
        'headers',
    ] = 'prompt'
    details: str | None = None


@dataclass(frozen=True)
class ImageModelV2CallWarningOther:
    """Warning from the model provider for this call. The call will proceed, but e.g.
    some settings might not be supported, which can lead to suboptimal results.
    """

    type: Literal['other'] = 'other'
    message: str = ''


ImageModelV2CallWarning = Union[
    ImageModelV2CallWarningUnsupportedSetting,
    ImageModelV2CallWarningOther,
]

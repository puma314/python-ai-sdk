from __future__ import annotations

"""Warning from the model provider for this call.

The call will proceed, but e.g. some settings might not be supported,
which can lead to suboptimal results.

Translated from: packages/provider/src/language-model/v2/language-model-v2-call-warning.ts
"""

from dataclasses import dataclass
from typing import Literal, Union

from .language_model_v2_function_tool import (
    LanguageModelV2FunctionTool,
)
from .language_model_v2_provider_defined_tool import (
    LanguageModelV2ProviderDefinedTool,
)


# The setting field corresponds to keyof LanguageModelV2CallOptions excluding 'prompt'.
LanguageModelV2CallOptionKey = Literal[
    'max_output_tokens',
    'temperature',
    'stop_sequences',
    'top_p',
    'top_k',
    'presence_penalty',
    'frequency_penalty',
    'response_format',
    'seed',
    'tools',
    'tool_choice',
    'include_raw_chunks',
    'abort_signal',
    'headers',
    'provider_options',
]


@dataclass(frozen=True)
class UnsupportedSettingWarning:
    """Warning for an unsupported setting."""

    type: Literal['unsupported-setting'] = 'unsupported-setting'
    setting: LanguageModelV2CallOptionKey = 'temperature'
    details: str | None = None


@dataclass(frozen=True)
class UnsupportedToolWarning:
    """Warning for an unsupported tool."""

    type: Literal['unsupported-tool'] = 'unsupported-tool'
    tool: LanguageModelV2FunctionTool | LanguageModelV2ProviderDefinedTool = None  # type: ignore[assignment]
    details: str | None = None


@dataclass(frozen=True)
class OtherWarning:
    """Other warning."""

    type: Literal['other'] = 'other'
    message: str = ''


LanguageModelV2CallWarning = Union[
    UnsupportedSettingWarning,
    UnsupportedToolWarning,
    OtherWarning,
]

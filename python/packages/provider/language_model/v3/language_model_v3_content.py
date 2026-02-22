from __future__ import annotations

"""Language model v3 content type union.

Translated from: packages/provider/src/language-model/v3/language-model-v3-content.ts
"""

from typing import Union

from .language_model_v3_file import LanguageModelV3File
from .language_model_v3_reasoning import LanguageModelV3Reasoning
from .language_model_v3_source import LanguageModelV3Source
from .language_model_v3_text import LanguageModelV3Text
from .language_model_v3_tool_approval_request import LanguageModelV3ToolApprovalRequest
from .language_model_v3_tool_call import LanguageModelV3ToolCall
from .language_model_v3_tool_result import LanguageModelV3ToolResult

LanguageModelV3Content = Union[
    LanguageModelV3Text,
    LanguageModelV3Reasoning,
    LanguageModelV3File,
    LanguageModelV3ToolApprovalRequest,
    LanguageModelV3Source,
    LanguageModelV3ToolCall,
    LanguageModelV3ToolResult,
]

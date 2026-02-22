from typing import TypeAlias

from .language_model_v3_file import LanguageModelV3File
from .language_model_v3_reasoning import LanguageModelV3Reasoning
from .language_model_v3_source import LanguageModelV3Source
from .language_model_v3_text import LanguageModelV3Text
from .language_model_v3_tool_approval_request import (
  LanguageModelV3ToolApprovalRequest,
)
from .language_model_v3_tool_call import LanguageModelV3ToolCall
from .language_model_v3_tool_result import LanguageModelV3ToolResult

LanguageModelV3Content: TypeAlias = (
  LanguageModelV3Text
  | LanguageModelV3Reasoning
  | LanguageModelV3File
  | LanguageModelV3ToolApprovalRequest
  | LanguageModelV3Source
  | LanguageModelV3ToolCall
  | LanguageModelV3ToolResult
)

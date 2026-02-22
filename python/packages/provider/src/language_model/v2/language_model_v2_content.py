from typing import TypeAlias

from .language_model_v2_file import LanguageModelV2File
from .language_model_v2_reasoning import LanguageModelV2Reasoning
from .language_model_v2_source import LanguageModelV2Source
from .language_model_v2_text import LanguageModelV2Text
from .language_model_v2_tool_call import LanguageModelV2ToolCall
from .language_model_v2_tool_result import LanguageModelV2ToolResult

LanguageModelV2Content: TypeAlias = (
  LanguageModelV2Text
  | LanguageModelV2Reasoning
  | LanguageModelV2File
  | LanguageModelV2Source
  | LanguageModelV2ToolCall
  | LanguageModelV2ToolResult
)

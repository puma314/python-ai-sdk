"""
Auto-translated Python mirror for `src/types/index.ts`.
"""

from __future__ import annotations

from typing import Any, TypeAlias

try:
  from .assistant_model_message import AssistantContent, AssistantModelMessage
except Exception:
  AssistantContent: Any = None
  AssistantModelMessage: Any = None

try:
  from .content_part import FilePart, ImagePart, ReasoningPart, TextPart, ToolCallPart, ToolResultOutput, ToolResultPart
except Exception:
  FilePart: Any = None
  ImagePart: Any = None
  ReasoningPart: Any = None
  TextPart: Any = None
  ToolCallPart: Any = None
  ToolResultOutput: Any = None
  ToolResultPart: Any = None

try:
  from .data_content import DataContent
except Exception:
  DataContent: Any = None

try:
  from .execute_tool import executeTool
except Exception:
  executeTool: Any = None

try:
  from .model_message import ModelMessage
except Exception:
  ModelMessage: Any = None

try:
  from .provider_options import ProviderOptions
except Exception:
  ProviderOptions: Any = None

try:
  from .system_model_message import SystemModelMessage
except Exception:
  SystemModelMessage: Any = None

try:
  from .tool import dynamicTool, tool, type_InferToolInput, type_InferToolOutput, type_Tool, type_ToolExecutionOptions, type_ToolExecuteFunction, type_ToolNeedsApprovalFunction
except Exception:
  dynamicTool: Any = None
  tool: Any = None
  type_InferToolInput: Any = None
  type_InferToolOutput: Any = None
  type_Tool: Any = None
  type_ToolExecutionOptions: Any = None
  type_ToolExecuteFunction: Any = None
  type_ToolNeedsApprovalFunction: Any = None

try:
  from .tool_approval_request import ToolApprovalRequest
except Exception:
  ToolApprovalRequest: Any = None

try:
  from .tool_approval_response import ToolApprovalResponse
except Exception:
  ToolApprovalResponse: Any = None

try:
  from .tool_call import ToolCall
except Exception:
  ToolCall: Any = None

try:
  from .tool_model_message import ToolContent, ToolModelMessage
except Exception:
  ToolContent: Any = None
  ToolModelMessage: Any = None

try:
  from .tool_result import ToolResult
except Exception:
  ToolResult: Any = None

try:
  from .user_model_message import UserContent, UserModelMessage
except Exception:
  UserContent: Any = None
  UserModelMessage: Any = None

ToolCallOptions: TypeAlias = Any

__all__ = ['ToolCallOptions']

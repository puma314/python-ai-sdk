"""
Auto-translated Python mirror for `src/generate-text/index.ts`.
"""

from __future__ import annotations

from typing import Any, TypeAlias

try:
  from .generate_text import generateText, type_GenerateTextOnFinishCallback, type_GenerateTextOnStartCallback, type_GenerateTextOnStepStartCallback, type_GenerateTextOnStepFinishCallback, type_GenerateTextOnToolCallStartCallback, type_GenerateTextOnToolCallFinishCallback
except Exception:
  generateText: Any = None
  type_GenerateTextOnFinishCallback: Any = None
  type_GenerateTextOnStartCallback: Any = None
  type_GenerateTextOnStepStartCallback: Any = None
  type_GenerateTextOnStepFinishCallback: Any = None
  type_GenerateTextOnToolCallStartCallback: Any = None
  type_GenerateTextOnToolCallFinishCallback: Any = None

try:
  from .content_part import ContentPart
except Exception:
  ContentPart: Any = None

try:
  from .generate_text_result import GenerateTextResult
except Exception:
  GenerateTextResult: Any = None

try:
  from .generated_file import DefaultGeneratedFile, Experimental_GeneratedImage, ___Image_for_backwards_compatibility, TODO_remove_in_v7___type_GeneratedFile
except Exception:
  DefaultGeneratedFile: Any = None
  Experimental_GeneratedImage: Any = None
  ___Image_for_backwards_compatibility: Any = None
  TODO_remove_in_v7___type_GeneratedFile: Any = None

try:
  from .output_utils import InferGenerateOutput, InferStreamOutput
except Exception:
  InferGenerateOutput: Any = None
  InferStreamOutput: Any = None

try:
  from .prepare_step import PrepareStepFunction, PrepareStepResult
except Exception:
  PrepareStepFunction: Any = None
  PrepareStepResult: Any = None

try:
  from .prune_messages import pruneMessages
except Exception:
  pruneMessages: Any = None

try:
  from .reasoning_output import ReasoningOutput
except Exception:
  ReasoningOutput: Any = None

try:
  from .smooth_stream import smoothStream, type_ChunkDetector
except Exception:
  smoothStream: Any = None
  type_ChunkDetector: Any = None

try:
  from .step_result import StepResult
except Exception:
  StepResult: Any = None

try:
  from .stop_condition import hasToolCall, stepCountIs, type_StopCondition
except Exception:
  hasToolCall: Any = None
  stepCountIs: Any = None
  type_StopCondition: Any = None

try:
  from .stream_text import streamText, type_StreamTextOnChunkCallback, type_StreamTextOnErrorCallback, type_StreamTextOnFinishCallback, type_StreamTextOnStartCallback, type_StreamTextOnStepFinishCallback, type_StreamTextOnStepStartCallback, type_StreamTextOnToolCallFinishCallback, type_StreamTextOnToolCallStartCallback, type_StreamTextTransform
except Exception:
  streamText: Any = None
  type_StreamTextOnChunkCallback: Any = None
  type_StreamTextOnErrorCallback: Any = None
  type_StreamTextOnFinishCallback: Any = None
  type_StreamTextOnStartCallback: Any = None
  type_StreamTextOnStepFinishCallback: Any = None
  type_StreamTextOnStepStartCallback: Any = None
  type_StreamTextOnToolCallFinishCallback: Any = None
  type_StreamTextOnToolCallStartCallback: Any = None
  type_StreamTextTransform: Any = None

try:
  from .stream_text_result import StreamTextResult, TextStreamPart, UIMessageStreamOptions
except Exception:
  StreamTextResult: Any = None
  TextStreamPart: Any = None
  UIMessageStreamOptions: Any = None

try:
  from .tool_approval_request_output import ToolApprovalRequestOutput
except Exception:
  ToolApprovalRequestOutput: Any = None

try:
  from .tool_call import DynamicToolCall, StaticToolCall, TypedToolCall
except Exception:
  DynamicToolCall: Any = None
  StaticToolCall: Any = None
  TypedToolCall: Any = None

try:
  from .tool_call_repair_function import ToolCallRepairFunction
except Exception:
  ToolCallRepairFunction: Any = None

try:
  from .tool_error import DynamicToolError, StaticToolError, TypedToolError
except Exception:
  DynamicToolError: Any = None
  StaticToolError: Any = None
  TypedToolError: Any = None

try:
  from .tool_output_denied import StaticToolOutputDenied, TypedToolOutputDenied
except Exception:
  StaticToolOutputDenied: Any = None
  TypedToolOutputDenied: Any = None

try:
  from .tool_result import DynamicToolResult, StaticToolResult, TypedToolResult
except Exception:
  DynamicToolResult: Any = None
  StaticToolResult: Any = None
  TypedToolResult: Any = None

try:
  from .tool_set import ToolSet
except Exception:
  ToolSet: Any = None


"""
Auto-translated Python mirror for `src/ui/index.ts`.
"""

from __future__ import annotations

from typing import Any, TypeAlias

try:
  from .call_completion_api import callCompletionApi
except Exception:
  callCompletionApi: Any = None

try:
  from .chat import AbstractChat, type_ChatAddToolApproveResponseFunction, type_ChatInit, type_ChatOnDataCallback, type_ChatOnErrorCallback, type_ChatOnFinishCallback, type_ChatOnToolCallCallback, type_ChatRequestOptions, type_ChatState, type_ChatStatus, type_CreateUIMessage, type_InferUIDataParts, type_UIDataPartSchemas
except Exception:
  AbstractChat: Any = None
  type_ChatAddToolApproveResponseFunction: Any = None
  type_ChatInit: Any = None
  type_ChatOnDataCallback: Any = None
  type_ChatOnErrorCallback: Any = None
  type_ChatOnFinishCallback: Any = None
  type_ChatOnToolCallCallback: Any = None
  type_ChatRequestOptions: Any = None
  type_ChatState: Any = None
  type_ChatStatus: Any = None
  type_CreateUIMessage: Any = None
  type_InferUIDataParts: Any = None
  type_UIDataPartSchemas: Any = None

try:
  from .chat_transport import type_ChatTransport
except Exception:
  type_ChatTransport: Any = None

try:
  from .convert_file_list_to_file_ui_parts import convertFileListToFileUIParts
except Exception:
  convertFileListToFileUIParts: Any = None

try:
  from .convert_to_model_messages import convertToModelMessages
except Exception:
  convertToModelMessages: Any = None

try:
  from .default_chat_transport import DefaultChatTransport
except Exception:
  DefaultChatTransport: Any = None

try:
  from .direct_chat_transport import DirectChatTransport, type_DirectChatTransportOptions
except Exception:
  DirectChatTransport: Any = None
  type_DirectChatTransportOptions: Any = None

try:
  from .http_chat_transport import HttpChatTransport, type_HttpChatTransportInitOptions, type_PrepareReconnectToStreamRequest, type_PrepareSendMessagesRequest
except Exception:
  HttpChatTransport: Any = None
  type_HttpChatTransportInitOptions: Any = None
  type_PrepareReconnectToStreamRequest: Any = None
  type_PrepareSendMessagesRequest: Any = None

try:
  from .last_assistant_message_is_complete_with_approval_responses import lastAssistantMessageIsCompleteWithApprovalResponses
except Exception:
  lastAssistantMessageIsCompleteWithApprovalResponses: Any = None

try:
  from .last_assistant_message_is_complete_with_tool_calls import lastAssistantMessageIsCompleteWithToolCalls
except Exception:
  lastAssistantMessageIsCompleteWithToolCalls: Any = None

try:
  from .text_stream_chat_transport import TextStreamChatTransport
except Exception:
  TextStreamChatTransport: Any = None

try:
  from .ui_messages import getStaticToolName, getToolName, getToolOrDynamicToolName, isDataUIPart, isFileUIPart, isReasoningUIPart, isStaticToolUIPart, isTextUIPart, isToolOrDynamicToolUIPart, isToolUIPart, type_DataUIPart, type_DynamicToolUIPart, type_FileUIPart, type_InferUITool, type_InferUITools, type_ReasoningUIPart, type_SourceDocumentUIPart, type_SourceUrlUIPart, type_StepStartUIPart, type_TextUIPart, type_ToolUIPart, type_UIDataTypes, type_UIMessage, type_UIMessagePart, type_UITool, type_UIToolInvocation, type_UITools
except Exception:
  getStaticToolName: Any = None
  getToolName: Any = None
  getToolOrDynamicToolName: Any = None
  isDataUIPart: Any = None
  isFileUIPart: Any = None
  isReasoningUIPart: Any = None
  isStaticToolUIPart: Any = None
  isTextUIPart: Any = None
  isToolOrDynamicToolUIPart: Any = None
  isToolUIPart: Any = None
  type_DataUIPart: Any = None
  type_DynamicToolUIPart: Any = None
  type_FileUIPart: Any = None
  type_InferUITool: Any = None
  type_InferUITools: Any = None
  type_ReasoningUIPart: Any = None
  type_SourceDocumentUIPart: Any = None
  type_SourceUrlUIPart: Any = None
  type_StepStartUIPart: Any = None
  type_TextUIPart: Any = None
  type_ToolUIPart: Any = None
  type_UIDataTypes: Any = None
  type_UIMessage: Any = None
  type_UIMessagePart: Any = None
  type_UITool: Any = None
  type_UIToolInvocation: Any = None
  type_UITools: Any = None

try:
  from .use_completion import type_CompletionRequestOptions, type_UseCompletionOptions
except Exception:
  type_CompletionRequestOptions: Any = None
  type_UseCompletionOptions: Any = None

try:
  from .validate_ui_messages import safeValidateUIMessages, validateUIMessages, type_SafeValidateUIMessagesResult
except Exception:
  safeValidateUIMessages: Any = None
  validateUIMessages: Any = None
  type_SafeValidateUIMessagesResult: Any = None


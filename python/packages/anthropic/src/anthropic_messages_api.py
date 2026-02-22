"""Anthropic messages API types and schema models."""

from __future__ import annotations

from typing import Literal, NotRequired, TypeAlias, TypedDict

from pydantic import BaseModel

AnthropicSpeed: TypeAlias = Literal['fast', 'standard']
AnthropicCacheControl: TypeAlias = dict[str, str]


class AnthropicReasoningMetadata(TypedDict, total=False):
  signature: str
  redactedData: str


class AnthropicTextContent(TypedDict, total=False):
  type: Literal['text']
  text: str
  cache_control: AnthropicCacheControl
  citations: list[dict[str, object]]


class AnthropicThinkingContent(TypedDict):
  type: Literal['thinking']
  thinking: str
  signature: str


class AnthropicRedactedThinkingContent(TypedDict):
  type: Literal['redacted_thinking']
  data: str


class AnthropicCompactionContent(TypedDict):
  type: Literal['compaction']
  content: str


class AnthropicToolCallContent(TypedDict, total=False):
  type: Literal['tool_use', 'server_tool_use', 'mcp_tool_use']
  id: str
  name: str
  input: dict[str, object]
  cache_control: AnthropicCacheControl
  server_name: str


class AnthropicToolResultContent(TypedDict, total=False):
  type: str
  tool_use_id: str
  content: object
  is_error: bool
  cache_control: AnthropicCacheControl


class AnthropicUserMessage(TypedDict):
  role: Literal['user']
  content: list[dict[str, object]]


class AnthropicAssistantMessage(TypedDict):
  role: Literal['assistant']
  content: list[dict[str, object]]


AnthropicMessage: TypeAlias = AnthropicUserMessage | AnthropicAssistantMessage


class AnthropicMessagesPrompt(TypedDict):
  messages: list[AnthropicMessage]
  system: NotRequired[list[dict[str, object]] | None]


class AnthropicContainer(TypedDict, total=False):
  id: str
  skills: list[dict[str, object]]


class Citation(TypedDict, total=False):
  type: str
  url: str
  title: str
  cited_text: str
  encrypted_index: str
  document_index: int
  document_title: str
  start_page_number: int
  end_page_number: int
  start_char_index: int
  end_char_index: int


class AnthropicResponseContextManagementEdit(TypedDict, total=False):
  type: str
  cleared_tool_uses: int
  cleared_input_tokens: int
  cleared_thinking_turns: int


class AnthropicResponseContextManagement(TypedDict):
  applied_edits: list[AnthropicResponseContextManagementEdit]


AnthropicClearToolUsesEdit: TypeAlias = dict[str, object]
AnthropicClearThinkingBlockEdit: TypeAlias = dict[str, object]
AnthropicCompactEdit: TypeAlias = dict[str, object]
AnthropicInputTokensTrigger: TypeAlias = dict[str, object]
AnthropicToolUsesTrigger: TypeAlias = dict[str, object]
AnthropicContextManagementTrigger: TypeAlias = dict[str, object]
AnthropicContextManagementEdit: TypeAlias = dict[str, object]
AnthropicContextManagementConfig: TypeAlias = dict[str, object]
AnthropicResponseClearToolUsesEdit: TypeAlias = dict[str, object]
AnthropicResponseClearThinkingBlockEdit: TypeAlias = dict[str, object]
AnthropicResponseCompactEdit: TypeAlias = dict[str, object]
AnthropicImageContent: TypeAlias = dict[str, object]
AnthropicDocumentContent: TypeAlias = dict[str, object]
AnthropicServerToolUseContent: TypeAlias = dict[str, object]
AnthropicMcpToolUseContent: TypeAlias = dict[str, object]
AnthropicMcpToolResultContent: TypeAlias = dict[str, object]
AnthropicWebFetchToolResultContent: TypeAlias = dict[str, object]
AnthropicWebSearchToolResultContent: TypeAlias = dict[str, object]
AnthropicCodeExecutionToolResultContent: TypeAlias = dict[str, object]
AnthropicBashCodeExecutionToolResultContent: TypeAlias = dict[str, object]
AnthropicTextEditorCodeExecutionToolResultContent: TypeAlias = dict[str, object]
AnthropicToolReferenceContent: TypeAlias = dict[str, object]
AnthropicToolSearchToolResultContent: TypeAlias = dict[str, object]
AnthropicTool: TypeAlias = dict[str, object]
AnthropicToolChoice: TypeAlias = dict[str, object]
AnthropicToolCallCaller: TypeAlias = dict[str, object]


class _AnthropicReasoningMetadataSchema(BaseModel):
  signature: str | None = None
  redactedData: str | None = None


class _AnthropicMessagesResponseSchema(BaseModel):
  id: str | None = None
  model: str | None = None
  content: list[dict[str, object]]
  stop_reason: str | None = None
  usage: dict[str, object]


class _AnthropicMessagesChunkSchema(BaseModel):
  type: str
  index: int | None = None
  content_block: dict[str, object] | None = None
  delta: dict[str, object] | None = None
  message: dict[str, object] | None = None
  usage: dict[str, object] | None = None
  context_management: dict[str, object] | None = None
  error: dict[str, object] | None = None


def anthropicReasoningMetadataSchema() -> type[_AnthropicReasoningMetadataSchema]:
  """Return pydantic schema for Anthropic reasoning metadata."""

  return _AnthropicReasoningMetadataSchema


def anthropicMessagesResponseSchema() -> type[_AnthropicMessagesResponseSchema]:
  """Return pydantic schema for Anthropic messages API responses."""

  return _AnthropicMessagesResponseSchema


def anthropicMessagesChunkSchema() -> type[_AnthropicMessagesChunkSchema]:
  """Return pydantic schema for Anthropic streaming chunk payloads."""

  return _AnthropicMessagesChunkSchema


__all__ = [
  'AnthropicAssistantMessage',
  'AnthropicBashCodeExecutionToolResultContent',
  'AnthropicCacheControl',
  'AnthropicClearThinkingBlockEdit',
  'AnthropicClearToolUsesEdit',
  'AnthropicCodeExecutionToolResultContent',
  'AnthropicCompactEdit',
  'AnthropicCompactionContent',
  'AnthropicContainer',
  'AnthropicContextManagementConfig',
  'AnthropicContextManagementEdit',
  'AnthropicContextManagementTrigger',
  'AnthropicDocumentContent',
  'AnthropicImageContent',
  'AnthropicInputTokensTrigger',
  'AnthropicMcpToolResultContent',
  'AnthropicMcpToolUseContent',
  'AnthropicMessage',
  'AnthropicMessagesPrompt',
  'AnthropicReasoningMetadata',
  'AnthropicRedactedThinkingContent',
  'AnthropicResponseClearThinkingBlockEdit',
  'AnthropicResponseClearToolUsesEdit',
  'AnthropicResponseCompactEdit',
  'AnthropicResponseContextManagement',
  'AnthropicResponseContextManagementEdit',
  'AnthropicServerToolUseContent',
  'AnthropicSpeed',
  'AnthropicTextContent',
  'AnthropicTextEditorCodeExecutionToolResultContent',
  'AnthropicThinkingContent',
  'AnthropicTool',
  'AnthropicToolCallCaller',
  'AnthropicToolCallContent',
  'AnthropicToolChoice',
  'AnthropicToolReferenceContent',
  'AnthropicToolResultContent',
  'AnthropicToolSearchToolResultContent',
  'AnthropicToolUsesTrigger',
  'AnthropicUserMessage',
  'AnthropicWebFetchToolResultContent',
  'AnthropicWebSearchToolResultContent',
  'Citation',
  'anthropicMessagesChunkSchema',
  'anthropicMessagesResponseSchema',
  'anthropicReasoningMetadataSchema',
]

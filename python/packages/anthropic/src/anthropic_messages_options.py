"""Anthropic message model options schemas."""

from __future__ import annotations

from typing import Literal, TypeAlias

from pydantic import BaseModel


AnthropicMessagesModelId: TypeAlias = str


class _CitationsOptions(BaseModel):
  enabled: bool


class AnthropicFilePartProviderOptions(BaseModel):
  citations: _CitationsOptions | None = None
  title: str | None = None
  context: str | None = None


class AnthropicThinkingOptions(BaseModel):
  type: Literal['adaptive', 'enabled', 'disabled']
  budgetTokens: int | None = None


class AnthropicLanguageModelOptions(BaseModel):
  sendReasoning: bool | None = None
  structuredOutputMode: Literal['outputFormat', 'jsonTool', 'auto'] | None = None
  thinking: AnthropicThinkingOptions | None = None
  disableParallelToolUse: bool | None = None
  cacheControl: dict[str, object] | None = None
  mcpServers: list[dict[str, object]] | None = None
  container: dict[str, object] | None = None
  toolStreaming: bool | None = None
  effort: Literal['low', 'medium', 'high', 'max'] | None = None
  speed: Literal['fast', 'standard'] | None = None
  contextManagement: dict[str, object] | None = None


anthropicFilePartProviderOptions = AnthropicFilePartProviderOptions
anthropicLanguageModelOptions = AnthropicLanguageModelOptions


__all__ = [
  'AnthropicFilePartProviderOptions',
  'AnthropicLanguageModelOptions',
  'AnthropicMessagesModelId',
  'anthropicFilePartProviderOptions',
  'anthropicLanguageModelOptions',
]

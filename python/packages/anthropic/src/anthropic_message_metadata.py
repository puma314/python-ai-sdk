"""Anthropic provider metadata structures."""

from __future__ import annotations

from typing import Literal, TypedDict


class AnthropicUsageIteration(TypedDict):
  """Usage breakdown entry when compaction occurs."""

  type: Literal['compaction', 'message']
  inputTokens: int
  outputTokens: int


class AnthropicSkillMetadata(TypedDict):
  type: Literal['anthropic', 'custom']
  skillId: str
  version: str


class AnthropicContainerMetadata(TypedDict):
  expiresAt: str
  id: str
  skills: list[AnthropicSkillMetadata] | None


class AnthropicClearToolUsesEdit(TypedDict):
  type: Literal['clear_tool_uses_20250919']
  clearedToolUses: int
  clearedInputTokens: int


class AnthropicClearThinkingEdit(TypedDict):
  type: Literal['clear_thinking_20251015']
  clearedThinkingTurns: int
  clearedInputTokens: int


class AnthropicCompactionEdit(TypedDict):
  type: Literal['compact_20260112']


class AnthropicContextManagement(TypedDict):
  appliedEdits: list[
    AnthropicClearToolUsesEdit | AnthropicClearThinkingEdit | AnthropicCompactionEdit
  ]


class AnthropicMessageMetadata(TypedDict):
  usage: dict[str, object]
  cacheCreationInputTokens: int | None
  stopSequence: str | None
  iterations: list[AnthropicUsageIteration] | None
  container: AnthropicContainerMetadata | None
  contextManagement: AnthropicContextManagement | None


__all__ = ['AnthropicMessageMetadata', 'AnthropicUsageIteration']

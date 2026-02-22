"""Anthropic stop-reason mapping helpers."""

from typing import Literal


def mapAnthropicStopReason(
  *,
  finishReason: str | None,
  isJsonResponseFromTool: bool = False,
) -> Literal['stop', 'content-filter', 'tool-calls', 'length', 'other']:
  """Map Anthropic stop reasons into unified v3 finish reasons."""

  if finishReason in {'pause_turn', 'end_turn', 'stop_sequence'}:
    return 'stop'
  if finishReason == 'refusal':
    return 'content-filter'
  if finishReason == 'tool_use':
    return 'stop' if isJsonResponseFromTool else 'tool-calls'
  if finishReason in {'max_tokens', 'model_context_window_exceeded'}:
    return 'length'
  if finishReason == 'compaction':
    return 'other'
  return 'other'


__all__ = ['mapAnthropicStopReason']

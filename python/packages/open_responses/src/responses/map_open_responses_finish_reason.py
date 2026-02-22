"""Map Open Responses finish reason strings to v3 unified reasons."""

from typing import Literal


def mapOpenResponsesFinishReason(
  *,
  finishReason: str | None,
  hasToolCalls: bool,
) -> Literal['stop', 'length', 'content-filter', 'tool-calls', 'other']:
  """Translate provider finish-reason codes into AI SDK unified reasons."""

  if finishReason in (None,):
    return 'tool-calls' if hasToolCalls else 'stop'
  if finishReason == 'max_output_tokens':
    return 'length'
  if finishReason == 'content_filter':
    return 'content-filter'
  return 'tool-calls' if hasToolCalls else 'other'

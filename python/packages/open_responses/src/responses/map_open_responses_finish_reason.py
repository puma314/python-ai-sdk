"""Map Open Responses finish reason strings to v3 unified reasons."""

from packages.provider.src.language_model.v3.language_model_v3_finish_reason import (
  LanguageModelV3FinishReason,
)


def mapOpenResponsesFinishReason(
  *,
  finishReason: str | None,
  hasToolCalls: bool,
) -> LanguageModelV3FinishReason['unified']:
  """Translate provider finish-reason codes into AI SDK unified reasons."""

  if finishReason in (None,):
    return 'tool-calls' if hasToolCalls else 'stop'
  if finishReason == 'max_output_tokens':
    return 'length'
  if finishReason == 'content_filter':
    return 'content-filter'
  return 'tool-calls' if hasToolCalls else 'other'

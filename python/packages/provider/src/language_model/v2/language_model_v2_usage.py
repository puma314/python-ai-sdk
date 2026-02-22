from typing import NotRequired, TypedDict


class LanguageModelV2Usage(TypedDict):
  inputTokens: int | None
  outputTokens: int | None
  totalTokens: int | None
  reasoningTokens: NotRequired[int | None]
  cachedInputTokens: NotRequired[int | None]

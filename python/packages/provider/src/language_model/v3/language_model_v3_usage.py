from typing import NotRequired, TypedDict

from ...json_value.json_value import JSONObject


class LanguageModelV3InputTokens(TypedDict):
  total: int | None
  noCache: int | None
  cacheRead: int | None
  cacheWrite: int | None


class LanguageModelV3OutputTokens(TypedDict):
  total: int | None
  text: int | None
  reasoning: int | None


class LanguageModelV3Usage(TypedDict):
  inputTokens: LanguageModelV3InputTokens
  outputTokens: LanguageModelV3OutputTokens
  raw: NotRequired[JSONObject]

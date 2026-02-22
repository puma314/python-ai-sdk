from typing import Literal, TypedDict


class LanguageModelV3FinishReason(TypedDict):
  unified: Literal[
    'stop',
    'length',
    'content-filter',
    'tool-calls',
    'error',
    'other',
  ]
  raw: str | None

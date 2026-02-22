from typing import Literal, TypeAlias

LanguageModelV2FinishReason: TypeAlias = Literal[
  'stop',
  'length',
  'content-filter',
  'tool-calls',
  'error',
  'other',
  'unknown',
]

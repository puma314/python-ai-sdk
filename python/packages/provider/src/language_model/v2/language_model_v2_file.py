from typing import Literal, TypedDict


class LanguageModelV2File(TypedDict):
  type: Literal['file']
  mediaType: str
  data: str | bytes

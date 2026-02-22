from datetime import datetime
from typing import NotRequired, TypedDict


class LanguageModelV2ResponseMetadata(TypedDict):
  id: NotRequired[str]
  timestamp: NotRequired[datetime]
  modelId: NotRequired[str]

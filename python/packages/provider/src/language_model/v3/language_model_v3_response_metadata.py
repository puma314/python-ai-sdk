from datetime import datetime
from typing import NotRequired, TypedDict


class LanguageModelV3ResponseMetadata(TypedDict):
  id: NotRequired[str]
  timestamp: NotRequired[datetime]
  modelId: NotRequired[str]

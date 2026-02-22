"""Error raised when a requested model identifier does not exist."""

from typing import Literal

from .ai_sdk_error import AISDKError

ModelType = Literal[
  'languageModel',
  'embeddingModel',
  'imageModel',
  'transcriptionModel',
  'speechModel',
  'rerankingModel',
  'videoModel',
]


class NoSuchModelError(AISDKError):
  """Raised by providers for unknown model IDs."""

  def __init__(
    self,
    *,
    modelId: str,
    modelType: ModelType,
    message: str | None = None,
    errorName: str = 'AI_NoSuchModelError',
  ):
    super().__init__(
      name=errorName,
      message=message or f'No such {modelType}: {modelId}',
    )
    self.modelId = modelId
    self.modelType = modelType

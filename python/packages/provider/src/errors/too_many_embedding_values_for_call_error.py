"""Error raised when embedding call input size exceeds model limits."""

from .ai_sdk_error import AISDKError


class TooManyEmbeddingValuesForCallError(AISDKError):
  """Raised when too many values are sent to a single embedding call."""

  def __init__(
    self,
    *,
    provider: str,
    modelId: str,
    maxEmbeddingsPerCall: int,
    values: list[object],
  ):
    super().__init__(
      name='AI_TooManyEmbeddingValuesForCallError',
      message=(
        'Too many values for a single embedding call. '
        f'The {provider} model "{modelId}" can only embed up to '
        f'{maxEmbeddingsPerCall} values per call, but {len(values)} values were provided.'
      ),
    )
    self.provider = provider
    self.modelId = modelId
    self.maxEmbeddingsPerCall = maxEmbeddingsPerCall
    self.values = values

"""API key loading utility."""

from __future__ import annotations

import os

from packages.provider.src.errors.load_api_key_error import LoadAPIKeyError


def loadApiKey(
  *,
  apiKey: str | None = None,
  environmentVariableName: str,
  description: str,
) -> str:
  """Load API key from parameter or environment."""

  if apiKey:
    return apiKey
  env_value = os.getenv(environmentVariableName)
  if env_value:
    return env_value
  raise LoadAPIKeyError(
    message=(
      f'{description} API key is missing. '
      f'Set `{environmentVariableName}` or pass `apiKey`.'
    )
  )


__all__ = ['loadApiKey']

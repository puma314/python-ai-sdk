"""Configuration setting loaders."""

from __future__ import annotations

import os


def loadOptionalSetting(
  *,
  settingValue: str | None = None,
  environmentVariableName: str,
) -> str | None:
  """Load optional string setting from explicit value or environment."""

  if settingValue is not None:
    return settingValue
  return os.getenv(environmentVariableName)


__all__ = ['loadOptionalSetting']

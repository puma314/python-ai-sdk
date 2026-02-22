"""
Auto-translated Python mirror for `src/prompt/call-settings.ts`.

Timeout configuration for API calls. Can be specified as:
- A number representing milliseconds
- An object with `totalMs` property for the total timeout in milliseconds
- An object with `stepMs` property for the timeout of each step in milliseconds
- An object with `chunkMs` property for the timeout between stream chunks (streaming only)
/
"""

from __future__ import annotations

from typing import Any, TypeAlias

CallSettings: TypeAlias = Any
TimeoutConfiguration: TypeAlias = Any

def getChunkTimeoutMs(*args: Any, **kwargs: Any) -> Any:
  """Auto-translated function placeholder."""
  return None

def getStepTimeoutMs(*args: Any, **kwargs: Any) -> Any:
  """Auto-translated function placeholder."""
  return None

def getTotalTimeoutMs(*args: Any, **kwargs: Any) -> Any:
  """Auto-translated function placeholder."""
  return None

__all__ = ['CallSettings', 'TimeoutConfiguration', 'getChunkTimeoutMs', 'getStepTimeoutMs', 'getTotalTimeoutMs']

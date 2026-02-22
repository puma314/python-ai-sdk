"""
Auto-translated Python mirror for `src/util/merge-abort-signals.ts`.

Merges multiple AbortSignals into a single AbortSignal.
The returned signal will abort when any of the input signals abort,
with the same reason as the first signal to abort.
@param signals - The AbortSignals to merge. Null and undefined values are filtered out.
@returns An AbortSignal that aborts when any of the input signals abort,
or undefined if no valid signals are provided.
/
"""

from __future__ import annotations

from typing import Any, TypeAlias


def mergeAbortSignals(*args: Any, **kwargs: Any) -> Any:
  """Auto-translated function placeholder."""
  return None

__all__ = ['mergeAbortSignals']

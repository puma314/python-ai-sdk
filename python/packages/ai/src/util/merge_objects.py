"""
Auto-translated Python mirror for `src/util/merge-objects.ts`.

Deeply merges two objects together.
- Properties from the `overrides` object override those in the `base` object with the same key.
- For nested objects, the merge is performed recursively (deep merge).
- Arrays are replaced, not merged.
- Primitive values are replaced.
- If both `base` and `overrides` are undefined, returns undefined.
- If one of `base` or `overrides` is undefined, returns the other.
@param base The target object to merge into
@param overrides The source object to merge from
@returns A new object with the merged properties, or undefined if both inputs are undefined
/
"""

from __future__ import annotations

from typing import Any, TypeAlias


def mergeObjects(*args: Any, **kwargs: Any) -> Any:
  """Auto-translated function placeholder."""
  return None

__all__ = ['mergeObjects']

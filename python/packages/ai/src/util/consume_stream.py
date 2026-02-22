"""
Auto-translated Python mirror for `src/util/consume-stream.ts`.

Consumes a ReadableStream until it's fully read.
This function reads the stream chunk by chunk until the stream is exhausted.
It doesn't process or return the data from the stream; it simply ensures
that the entire stream is read.
@param options - The options for consuming the stream.
@param options.stream - The ReadableStream to be consumed.
@param options.onError - Optional callback to handle errors that occur during consumption.
@returns A promise that resolves when the stream is fully consumed.
/
"""

from __future__ import annotations

from typing import Any, TypeAlias


def consumeStream(*args: Any, **kwargs: Any) -> Any:
  """Auto-translated function placeholder."""
  return None

__all__ = ['consumeStream']

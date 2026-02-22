"""
Auto-translated Python mirror for `src/ui-message-stream/json-to-sse-transform-stream.ts`.

A TransformStream that converts JSON objects to Server-Sent Events (SSE) format.
Each object is serialized to JSON and wrapped in `data: ...\n\n` format.
When the stream ends, a `data: [DONE]\n\n` message is sent.
/
"""

from __future__ import annotations

from typing import Any, TypeAlias


class JsonToSseTransformStream:
  """Auto-translated class placeholder."""

  def __init__(self, *args: Any, **kwargs: Any):
    pass

__all__ = ['JsonToSseTransformStream']

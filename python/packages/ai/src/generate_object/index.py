"""
Auto-translated Python mirror for `src/generate-object/index.ts`.
"""

from __future__ import annotations

from typing import Any, TypeAlias

try:
  from .generate_object import generateObject
except Exception:
  generateObject: Any = None

try:
  from .repair_text import RepairTextFunction
except Exception:
  RepairTextFunction: Any = None

try:
  from .generate_object_result import GenerateObjectResult
except Exception:
  GenerateObjectResult: Any = None

try:
  from .stream_object import streamObject
except Exception:
  streamObject: Any = None

try:
  from .stream_object import StreamObjectOnFinishCallback
except Exception:
  StreamObjectOnFinishCallback: Any = None

try:
  from .stream_object_result import ObjectStreamPart, StreamObjectResult
except Exception:
  ObjectStreamPart: Any = None
  StreamObjectResult: Any = None


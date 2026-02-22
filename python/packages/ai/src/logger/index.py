"""
Auto-translated Python mirror for `src/logger/index.ts`.

@deprecated  Use `LogWarningsFunction` instead.
/
"""

from __future__ import annotations

from typing import Any, TypeAlias

try:
  from .log_warnings import Experimental_LogWarningsFunction
except Exception:
  Experimental_LogWarningsFunction: Any = None

try:
  from .log_warnings import type_LogWarningsFunction
except Exception:
  type_LogWarningsFunction: Any = None


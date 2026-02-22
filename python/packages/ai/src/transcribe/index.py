"""
Auto-translated Python mirror for `src/transcribe/index.ts`.
"""

from __future__ import annotations

from typing import Any, TypeAlias

try:
  from .transcribe import experimental_transcribe
except Exception:
  experimental_transcribe: Any = None

try:
  from .transcribe_result import Experimental_TranscriptionResult
except Exception:
  Experimental_TranscriptionResult: Any = None


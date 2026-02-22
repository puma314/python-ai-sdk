"""
Auto-translated Python mirror for `src/generate-speech/index.ts`.
"""

from __future__ import annotations

from typing import Any, TypeAlias

try:
  from .generate_speech import experimental_generateSpeech
except Exception:
  experimental_generateSpeech: Any = None

try:
  from .generate_speech_result import Experimental_SpeechResult
except Exception:
  Experimental_SpeechResult: Any = None

try:
  from .generated_audio_file import GeneratedAudioFile
except Exception:
  GeneratedAudioFile: Any = None


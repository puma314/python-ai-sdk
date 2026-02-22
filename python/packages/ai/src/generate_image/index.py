"""
Auto-translated Python mirror for `src/generate-image/index.ts`.
"""

from __future__ import annotations

from typing import Any, TypeAlias

try:
  from .generate_image import generateImage
except Exception:
  generateImage: Any = None

try:
  from .generate_image_result import GenerateImageResult
except Exception:
  GenerateImageResult: Any = None

experimental_generateImage: Any = None

__all__ = ['experimental_generateImage']

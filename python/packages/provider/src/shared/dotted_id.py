from __future__ import annotations

import re
from typing import NewType, TypeGuard

DottedId = NewType('DottedId', str)

_DOTTED_ID_PATTERN = re.compile(r'^[^.]+\.[^.]+$')


def is_dotted_id(value: str) -> TypeGuard[DottedId]:
  return bool(_DOTTED_ID_PATTERN.match(value))


def validate_dotted_id(value: str) -> DottedId:
  if not is_dotted_id(value):
    raise ValueError(
      f"Invalid dotted ID '{value}': expected format 'namespace.name'"
    )
  return DottedId(value)

"""Identifier generation helpers."""

from __future__ import annotations

from typing import Callable, TypeAlias
from uuid import uuid4

IdGenerator: TypeAlias = Callable[[], str]


def createIdGenerator(prefix: str = '') -> IdGenerator:
  """Create an ID generator function with optional prefix."""

  def _generate() -> str:
    core = uuid4().hex
    return f'{prefix}{core}'

  return _generate


def generateId() -> str:
  """Generate a random identifier."""

  return createIdGenerator()()


__all__ = ['IdGenerator', 'createIdGenerator', 'generateId']

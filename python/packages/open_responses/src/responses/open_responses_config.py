"""Configuration for OpenResponses language model instances."""

from dataclasses import dataclass
from typing import Callable


@dataclass
class OpenResponsesConfig:
  provider: str
  url: str
  headers: Callable[[], dict[str, str | None]]
  fetch: Callable[..., object] | None = None
  generateId: Callable[[], str] | None = None

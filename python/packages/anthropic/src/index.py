"""
Auto-translated Python mirror for `src/index.ts`.
"""

from __future__ import annotations

from typing import Any, TypeAlias

try:
  from .anthropic_message_metadata import AnthropicMessageMetadata, AnthropicUsageIteration
except Exception:
  AnthropicMessageMetadata: Any = None
  AnthropicUsageIteration: Any = None

try:
  from .anthropic_messages_options import AnthropicLanguageModelOptions, AnthropicProviderOptions
except Exception:
  AnthropicLanguageModelOptions: Any = None
  AnthropicProviderOptions: Any = None

try:
  from .anthropic_prepare_tools import AnthropicToolOptions
except Exception:
  AnthropicToolOptions: Any = None

try:
  from .anthropic_provider import anthropic, createAnthropic
except Exception:
  anthropic: Any = None
  createAnthropic: Any = None

try:
  from .anthropic_provider import AnthropicProvider, AnthropicProviderSettings
except Exception:
  AnthropicProvider: Any = None
  AnthropicProviderSettings: Any = None

try:
  from .forward_anthropic_container_id_from_last_step import forwardAnthropicContainerIdFromLastStep
except Exception:
  forwardAnthropicContainerIdFromLastStep: Any = None

try:
  from .version import VERSION
except Exception:
  VERSION: Any = None


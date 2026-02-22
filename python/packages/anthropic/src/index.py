"""Public exports for anthropic provider package."""

from .anthropic_message_metadata import AnthropicMessageMetadata, AnthropicUsageIteration
from .anthropic_messages_options import (
  AnthropicLanguageModelOptions,
)
from .anthropic_prepare_tools import AnthropicToolOptions
from .anthropic_provider import (
  AnthropicProvider,
  AnthropicProviderSettings,
  anthropic,
  createAnthropic,
)
from .forward_anthropic_container_id_from_last_step import (
  forwardAnthropicContainerIdFromLastStep,
)
from .version import VERSION

# Deprecated alias kept for compatibility with TS exports.
AnthropicProviderOptions = AnthropicLanguageModelOptions

__all__ = [
  'AnthropicMessageMetadata',
  'AnthropicUsageIteration',
  'AnthropicLanguageModelOptions',
  'AnthropicProviderOptions',
  'AnthropicToolOptions',
  'anthropic',
  'createAnthropic',
  'AnthropicProvider',
  'AnthropicProviderSettings',
  'forwardAnthropicContainerIdFromLastStep',
  'VERSION',
]


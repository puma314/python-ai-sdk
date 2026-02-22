from __future__ import annotations

"""Tool calls that the model has generated.

Translated from: packages/provider/src/language-model/v2/language-model-v2-tool-call.ts
"""

from dataclasses import dataclass, field
from typing import Literal

from ...shared.v2.shared_v2_provider_metadata import SharedV2ProviderMetadata


@dataclass(frozen=True)
class LanguageModelV2ToolCall:
    """Tool calls that the model has generated."""

    type: Literal['tool-call'] = 'tool-call'
    """The type discriminator for tool calls."""

    tool_call_id: str = ''
    """The identifier of the tool call. It must be unique across all tool calls."""

    tool_name: str = ''
    """The name of the tool that should be called."""

    input: str = ''
    """Stringified JSON object with the tool call arguments. Must match the
    parameters schema of the tool."""

    provider_executed: bool | None = None
    """Whether the tool call will be executed by the provider.
    If this flag is not set or is False, the tool call will be executed by the client."""

    provider_metadata: SharedV2ProviderMetadata | None = None
    """Additional provider-specific metadata for the tool call."""

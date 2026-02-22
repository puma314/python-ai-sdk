from __future__ import annotations
"""Tool calls that the model has generated.

Translated from: packages/provider/src/language-model/v3/language-model-v3-tool-call.ts
"""

from dataclasses import dataclass, field
from typing import Literal

from ...shared.v3.shared_v3_provider_metadata import SharedV3ProviderMetadata


@dataclass(frozen=True)
class LanguageModelV3ToolCall:
    """Tool calls that the model has generated."""

    type: Literal['tool-call'] = 'tool-call'

    tool_call_id: str = ''
    """The identifier of the tool call. It must be unique across all tool calls."""

    tool_name: str = ''
    """The name of the tool that should be called."""

    input: str = ''
    """Stringified JSON object with the tool call arguments. Must match the
    parameters schema of the tool."""

    provider_executed: bool | None = None
    """Whether the tool call will be executed by the provider.
    If this flag is not set or is false, the tool call will be executed by the client."""

    dynamic: bool | None = None
    """Whether the tool is dynamic, i.e. defined at runtime.
    For example, MCP (Model Context Protocol) tools that are executed by the provider."""

    provider_metadata: SharedV3ProviderMetadata | None = None
    """Additional provider-specific metadata for the tool call."""

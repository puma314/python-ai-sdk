from __future__ import annotations

"""Result of a tool call that has been executed by the provider.

Translated from: packages/provider/src/language-model/v3/language-model-v3-tool-result.ts
"""

from dataclasses import dataclass, field
from typing import Literal

from ...json_value.json_value import JSONValue
from ...shared.v3.shared_v3_provider_metadata import SharedV3ProviderMetadata


@dataclass(frozen=True)
class LanguageModelV3ToolResult:
    """Result of a tool call that has been executed by the provider."""

    type: Literal['tool-result'] = 'tool-result'

    tool_call_id: str = ''
    """The ID of the tool call that this result is associated with."""

    tool_name: str = ''
    """Name of the tool that generated this result."""

    result: JSONValue = field(default_factory=dict)
    """Result of the tool call. This is a JSON-serializable object."""

    is_error: bool | None = None
    """Optional flag if the result is an error or an error message."""

    preliminary: bool | None = None
    """Whether the tool result is preliminary.

    Preliminary tool results replace each other, e.g. image previews.
    There always has to be a final, non-preliminary tool result.

    If this flag is set to True, the tool result is preliminary.
    If this flag is not set or is False, the tool result is not preliminary.
    """

    dynamic: bool | None = None
    """Whether the tool is dynamic, i.e. defined at runtime.
    For example, MCP (Model Context Protocol) tools that are executed by the provider.
    """

    provider_metadata: SharedV3ProviderMetadata | None = None
    """Additional provider-specific metadata for the tool result."""

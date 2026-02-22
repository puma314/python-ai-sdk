"""The configuration of a tool that is defined by the provider.

Translated from: packages/provider/src/language-model/v2/language-model-v2-provider-defined-tool.ts
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal


def _validate_provider_tool_id(tool_id: str) -> str:
    """Validate that tool_id matches the pattern 'provider.tool_name'.

    Args:
        tool_id: The tool ID to validate.

    Returns:
        The validated tool ID.

    Raises:
        ValueError: If the ID does not match the expected format.
    """
    if "." not in tool_id or tool_id.startswith(".") or tool_id.endswith("."):
        raise ValueError(
            f"Invalid provider tool id format: {tool_id!r}. "
            "Expected '<provider-name>.<unique-tool-name>'."
        )
    return tool_id


@dataclass(frozen=True)
class LanguageModelV2ProviderDefinedTool:
    """The configuration of a tool that is defined by the provider."""

    id: str
    """The ID of the tool. Should follow the format '<provider-name>.<unique-tool-name>'."""

    name: str
    """The name of the tool that the user must use in the tool set."""

    args: dict[str, Any]
    """The arguments for configuring the tool.

    Must match the expected arguments defined by the provider for this tool.
    """

    type: Literal["provider-defined"] = "provider-defined"
    """The type of the tool (always 'provider-defined')."""

    def __post_init__(self) -> None:
        _validate_provider_tool_id(self.id)

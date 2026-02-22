from __future__ import annotations
"""The configuration of a provider tool.

Provider tools are tools that are specific to a certain provider.
The input and output schemas are defined by the provider, and
some of the tools are also executed on the provider systems.

Translated from: packages/provider/src/language-model/v3/language-model-v3-provider-tool.ts
"""

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
            "Expected '<provider-id>.<unique-tool-name>'."
        )
    return tool_id


@dataclass(frozen=True)
class LanguageModelV3ProviderTool:
    """The configuration of a provider tool.

    Provider tools are tools that are specific to a certain provider.
    The input and output schemas are defined by the provider, and
    some of the tools are also executed on the provider systems.
    """

    id: str
    """The ID of the tool. Should follow the format '<provider-id>.<unique-tool-name>'."""

    name: str
    """The name of the tool. Unique within this model call."""

    args: dict[str, Any]
    """The arguments for configuring the tool.

    Must match the expected arguments defined by the provider for this tool.
    """

    type: Literal["provider"] = "provider"
    """The type of the tool (always 'provider')."""

    def __post_init__(self) -> None:
        _validate_provider_tool_id(self.id)

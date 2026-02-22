from __future__ import annotations

"""A function tool definition for language model v2.

Translated from: packages/provider/src/language-model/v2/language-model-v2-function-tool.ts
"""

from dataclasses import dataclass, field
from typing import Any, Literal

from ai_sdk.provider.shared.v2.shared_v2_provider_options import SharedV2ProviderOptions


@dataclass(frozen=True)
class LanguageModelV2FunctionTool:
    """A tool has a name, a description, and a set of parameters.

    Note: this is **not** the user-facing tool definition. The AI SDK methods will
    map the user-facing tool definitions to this format.
    """

    type: Literal['function'] = 'function'
    """The type of the tool (always 'function')."""

    name: str = ''
    """The name of the tool. Unique within this model call."""

    description: str | None = None
    """A description of the tool. The language model uses this to understand the
    tool's purpose and to provide better completion suggestions."""

    input_schema: dict[str, Any] = field(default_factory=dict)
    """The parameters that the tool expects. The language model uses this to
    understand the tool's input requirements and to provide matching suggestions."""

    provider_options: SharedV2ProviderOptions | None = None
    """The provider-specific options for the tool."""

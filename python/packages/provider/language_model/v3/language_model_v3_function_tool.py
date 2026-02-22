from __future__ import annotations

"""A tool has a name, a description, and a set of parameters.

Translated from: packages/provider/src/language-model/v3/language-model-v3-function-tool.ts
"""

from dataclasses import dataclass, field
from typing import Any, Literal

from ...json_value.json_value import JSONObject
from ...shared.v3.shared_v3_provider_options import SharedV3ProviderOptions


@dataclass(frozen=True)
class InputExample:
    """An input example for a function tool."""

    input: JSONObject = field(default_factory=dict)


@dataclass(frozen=True)
class LanguageModelV3FunctionTool:
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

    input_examples: list[InputExample] | None = None
    """An optional list of input examples that show the language
    model what the input should look like."""

    strict: bool | None = None
    """Strict mode setting for the tool.

    Providers that support strict mode will use this setting to determine
    how the input should be generated. Strict mode will always produce
    valid inputs, but it might limit what input schemas are supported."""

    provider_options: SharedV3ProviderOptions | None = None
    """The provider-specific options for the tool."""

from __future__ import annotations
"""Language model v3 tool choice types.

Translated from: packages/provider/src/language-model/v3/language-model-v3-tool-choice.ts
"""

from dataclasses import dataclass
from typing import Literal, Union


@dataclass(frozen=True)
class LanguageModelV3ToolChoiceAuto:
    """The tool selection is automatic (can be no tool)."""

    type: Literal["auto"] = "auto"


@dataclass(frozen=True)
class LanguageModelV3ToolChoiceNone:
    """No tool must be selected."""

    type: Literal["none"] = "none"


@dataclass(frozen=True)
class LanguageModelV3ToolChoiceRequired:
    """One of the available tools must be selected."""

    type: Literal["required"] = "required"


@dataclass(frozen=True)
class LanguageModelV3ToolChoiceTool:
    """A specific tool must be selected."""

    type: Literal["tool"] = "tool"
    tool_name: str = ""


LanguageModelV3ToolChoice = Union[
    LanguageModelV3ToolChoiceAuto,
    LanguageModelV3ToolChoiceNone,
    LanguageModelV3ToolChoiceRequired,
    LanguageModelV3ToolChoiceTool,
]

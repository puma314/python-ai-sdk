from __future__ import annotations
"""Language model v2 tool choice types.

Translated from: packages/provider/src/language-model/v2/language-model-v2-tool-choice.ts
"""

from dataclasses import dataclass
from typing import Literal, Union


@dataclass(frozen=True)
class AutoToolChoice:
    """The tool selection is automatic (can be no tool)."""

    type: Literal["auto"] = "auto"


@dataclass(frozen=True)
class NoneToolChoice:
    """No tool must be selected."""

    type: Literal["none"] = "none"


@dataclass(frozen=True)
class RequiredToolChoice:
    """One of the available tools must be selected."""

    type: Literal["required"] = "required"


@dataclass(frozen=True)
class SpecificToolChoice:
    """A specific tool must be selected."""

    type: Literal["tool"] = "tool"
    tool_name: str = ""


LanguageModelV2ToolChoice = Union[
    AutoToolChoice,
    NoneToolChoice,
    RequiredToolChoice,
    SpecificToolChoice,
]

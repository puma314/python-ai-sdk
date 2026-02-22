from __future__ import annotations

"""Warning from the model.

For example, that certain features are unsupported or compatibility
functionality is used (which might lead to suboptimal results).

Translated from: packages/provider/src/shared/v3/shared-v3-warning.ts
"""

from dataclasses import dataclass
from typing import Literal, Union


@dataclass(frozen=True)
class UnsupportedWarning:
    """A feature is not supported by the model."""

    type: Literal['unsupported'] = 'unsupported'
    """A feature is not supported by the model."""

    feature: str = ''
    """The feature that is not supported."""

    details: str | None = None
    """Additional details about the warning."""


@dataclass(frozen=True)
class CompatibilityWarning:
    """A compatibility feature is used that might lead to suboptimal results."""

    type: Literal['compatibility'] = 'compatibility'
    """A compatibility feature is used that might lead to suboptimal results."""

    feature: str = ''
    """The feature that is used in a compatibility mode."""

    details: str | None = None
    """Additional details about the warning."""


@dataclass(frozen=True)
class OtherWarning:
    """Other warning."""

    type: Literal['other'] = 'other'
    """Other warning."""

    message: str = ''
    """The message of the warning."""


SharedV3Warning = Union[UnsupportedWarning, CompatibilityWarning, OtherWarning]

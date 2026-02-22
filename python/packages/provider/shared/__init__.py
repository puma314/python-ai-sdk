from __future__ import annotations
"""Public API for shared types.

Translated from: packages/provider/src/shared/index.ts
"""

from .v3 import (
    CompatibilityWarning,
    OtherWarning,
    SharedV3Headers,
    SharedV3ProviderMetadata,
    SharedV3ProviderOptions,
    SharedV3Warning,
    UnsupportedWarning,
)
from .v2 import (
    SharedV2Headers,
    SharedV2ProviderMetadata,
    SharedV2ProviderOptions,
)

__all__ = [
    "CompatibilityWarning",
    "OtherWarning",
    "SharedV2Headers",
    "SharedV2ProviderMetadata",
    "SharedV2ProviderOptions",
    "SharedV3Headers",
    "SharedV3ProviderMetadata",
    "SharedV3ProviderOptions",
    "SharedV3Warning",
    "UnsupportedWarning",
]

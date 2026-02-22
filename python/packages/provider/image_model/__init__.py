from __future__ import annotations

"""Public API for image model.

Translated from: packages/provider/src/image-model/index.ts
"""

from .v3 import (
    ImageModelV3,
    ImageModelV3CallOptions,
    ImageModelV3File,
    ImageModelV3ProviderMetadata,
    ImageModelV3Usage,
)
from .v2 import (
    ImageModelV2,
    ImageModelV2CallOptions,
    ImageModelV2CallWarning,
    ImageModelV2ProviderMetadata,
)

__all__ = [
    # v3
    "ImageModelV3",
    "ImageModelV3CallOptions",
    "ImageModelV3File",
    "ImageModelV3ProviderMetadata",
    "ImageModelV3Usage",
    # v2
    "ImageModelV2",
    "ImageModelV2CallOptions",
    "ImageModelV2CallWarning",
    "ImageModelV2ProviderMetadata",
]

from __future__ import annotations

"""Additional provider-specific metadata.

Metadata are additional outputs from the provider.
They are passed through to the provider from the AI SDK
and enable provider-specific functionality
that can be fully encapsulated in the provider.

This enables us to quickly ship provider-specific functionality
without affecting the core AI SDK.

The outer record is keyed by the provider name, and the inner
record is keyed by the provider-specific metadata key.

Example::

    {
        "anthropic": {
            "cacheControl": {"type": "ephemeral"}
        }
    }

Translated from: packages/provider/src/shared/v2/shared-v2-provider-metadata.ts
"""

from ...json_value.json_value import JSONValue

SharedV2ProviderMetadata = dict[str, dict[str, JSONValue]]

from __future__ import annotations

"""Additional provider-specific options.

Options are additional input to the provider.
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

Translated from: packages/provider/src/shared/v3/shared-v3-provider-options.ts
"""

from ...json_value.json_value import JSONObject

SharedV3ProviderOptions = dict[str, JSONObject]

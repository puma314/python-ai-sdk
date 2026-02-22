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

Translated from: packages/provider/src/shared/v2/shared-v2-provider-options.ts
"""

from ai_sdk.provider.json_value.json_value import JSONValue

SharedV2ProviderOptions = dict[str, dict[str, JSONValue]]

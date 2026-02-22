from __future__ import annotations
"""Speech model V2 call options type definition.

Translated from: packages/provider/src/speech-model/v2/speech-model-v2-call-options.ts
"""

import asyncio
from dataclasses import dataclass, field
from typing import Any

from ...json_value.json_value import JSONValue

SpeechModelV2ProviderOptions = dict[str, dict[str, JSONValue]]


@dataclass(frozen=True)
class SpeechModelV2CallOptions:
    """Options for calling a speech model V2."""

    text: str
    """Text to convert to speech."""

    voice: str | None = None
    """The voice to use for speech synthesis.

    This is provider-specific and may be a voice ID, name, or other identifier.
    """

    output_format: str | None = None
    """The desired output format for the audio e.g. "mp3", "wav", etc."""

    instructions: str | None = None
    """Instructions for the speech generation e.g. "Speak in a slow and steady tone"."""

    speed: float | None = None
    """The speed of the speech generation."""

    language: str | None = None
    """The language for speech generation.

    This should be an ISO 639-1 language code (e.g. "en", "es", "fr")
    or "auto" for automatic language detection. Provider support varies.
    """

    provider_options: SpeechModelV2ProviderOptions | None = None
    """Additional provider-specific options that are passed through to the provider
    as body parameters.

    The outer record is keyed by the provider name, and the inner
    record is keyed by the provider-specific metadata key.

    Example::

        {
            "openai": {}
        }
    """

    abort_signal: asyncio.Event | None = None
    """Abort signal for cancelling the operation."""

    headers: dict[str, str | None] | None = None
    """Additional HTTP headers to be sent with the request.

    Only applicable for HTTP-based providers.
    """

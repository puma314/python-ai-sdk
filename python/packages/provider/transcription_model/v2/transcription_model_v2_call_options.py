from __future__ import annotations

"""Transcription model v2 call options.

Translated from: packages/provider/src/transcription-model/v2/transcription-model-v2-call-options.ts
"""

import asyncio
from dataclasses import dataclass

from ...json_value.json_value import JSONValue

TranscriptionModelV2ProviderOptions = dict[str, dict[str, JSONValue]]


@dataclass(frozen=True)
class TranscriptionModelV2CallOptions:
    """Options for a transcription model v2 call."""

    audio: bytes | str
    """Audio data to transcribe.

    Accepts ``bytes`` or ``str``, where ``str`` is a base64 encoded audio file.
    """

    media_type: str
    """The IANA media type of the audio data.

    See https://www.iana.org/assignments/media-types/media-types.xhtml
    """

    provider_options: TranscriptionModelV2ProviderOptions | None = None
    """Additional provider-specific options that are passed through to the provider
    as body parameters.

    The outer dict is keyed by the provider name, and the inner
    dict is keyed by the provider-specific metadata key.

    Example::

        {
            "openai": {
                "timestampGranularities": ["word"]
            }
        }
    """

    abort_signal: asyncio.Event | None = None
    """Abort signal for cancelling the operation."""

    headers: dict[str, str | None] | None = None
    """Additional HTTP headers to be sent with the request.

    Only applicable for HTTP-based providers.
    """

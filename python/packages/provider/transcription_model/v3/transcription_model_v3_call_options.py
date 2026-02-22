from __future__ import annotations

"""Transcription model v3 call options.

Translated from: packages/provider/src/transcription-model/v3/transcription-model-v3-call-options.ts
"""

import asyncio
from dataclasses import dataclass

from ...json_value.json_value import JSONObject

TranscriptionModelV3ProviderOptions = dict[str, JSONObject]


@dataclass(frozen=True)
class TranscriptionModelV3CallOptions:
    """Options for a transcription model v3 call."""

    audio: bytes | str
    """Audio data to transcribe.
    Accepts ``bytes`` or ``str``, where ``str`` is a base64 encoded audio file.
    """

    media_type: str
    """The IANA media type of the audio data.

    See https://www.iana.org/assignments/media-types/media-types.xhtml
    """

    provider_options: TranscriptionModelV3ProviderOptions | None = None
    """Additional provider-specific options that are passed through to the provider
    as body parameters.

    The outer record is keyed by the provider name, and the inner
    record is keyed by the provider-specific metadata key.

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

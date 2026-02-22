"""Call options for transcription-model v3."""

from typing import NotRequired, TypeAlias, TypedDict

from ...json_value.json_value import JSONObject

TranscriptionModelV3ProviderOptions: TypeAlias = dict[str, JSONObject]


class TranscriptionModelV3CallOptions(TypedDict):
  audio: bytes | str
  mediaType: str
  providerOptions: NotRequired[TranscriptionModelV3ProviderOptions]
  abortSignal: NotRequired[object]
  headers: NotRequired[dict[str, str | None]]

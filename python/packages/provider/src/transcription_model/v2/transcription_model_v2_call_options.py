"""Call options for transcription-model v2."""

from typing import NotRequired, TypeAlias, TypedDict

from ...json_value.json_value import JSONValue

TranscriptionModelV2ProviderOptions: TypeAlias = dict[str, dict[str, JSONValue]]


class TranscriptionModelV2CallOptions(TypedDict):
  audio: bytes | str
  mediaType: str
  providerOptions: NotRequired[TranscriptionModelV2ProviderOptions]
  abortSignal: NotRequired[object]
  headers: NotRequired[dict[str, str | None]]

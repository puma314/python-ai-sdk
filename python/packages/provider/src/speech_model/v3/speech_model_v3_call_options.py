"""Call options for speech-model v3."""

from typing import NotRequired, TypeAlias, TypedDict

from ...json_value.json_value import JSONObject

SpeechModelV3ProviderOptions: TypeAlias = dict[str, JSONObject]


class SpeechModelV3CallOptions(TypedDict):
  text: str
  voice: NotRequired[str]
  outputFormat: NotRequired[str]
  instructions: NotRequired[str]
  speed: NotRequired[float]
  language: NotRequired[str]
  providerOptions: NotRequired[SpeechModelV3ProviderOptions]
  abortSignal: NotRequired[object]
  headers: NotRequired[dict[str, str | None]]

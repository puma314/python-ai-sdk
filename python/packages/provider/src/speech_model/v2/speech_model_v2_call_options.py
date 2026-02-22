"""Call options for speech-model v2."""

from typing import NotRequired, TypeAlias, TypedDict

from ...json_value.json_value import JSONValue

SpeechModelV2ProviderOptions: TypeAlias = dict[str, dict[str, JSONValue]]


class SpeechModelV2CallOptions(TypedDict):
  text: str
  voice: NotRequired[str]
  outputFormat: NotRequired[str]
  instructions: NotRequired[str]
  speed: NotRequired[float]
  language: NotRequired[str]
  providerOptions: NotRequired[SpeechModelV2ProviderOptions]
  abortSignal: NotRequired[object]
  headers: NotRequired[dict[str, str | None]]

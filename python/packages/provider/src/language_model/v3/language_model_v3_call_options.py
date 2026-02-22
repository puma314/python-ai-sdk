from typing import Any, Literal, NotRequired, TypeAlias, TypedDict

from ...shared.v3.shared_v3_provider_options import SharedV3ProviderOptions
from .language_model_v3_function_tool import JSONSchema7, LanguageModelV3FunctionTool
from .language_model_v3_prompt import LanguageModelV3Prompt
from .language_model_v3_provider_tool import LanguageModelV3ProviderTool
from .language_model_v3_tool_choice import LanguageModelV3ToolChoice


class LanguageModelV3TextResponseFormat(TypedDict):
  type: Literal['text']


class LanguageModelV3JsonResponseFormat(TypedDict):
  type: Literal['json']
  schema: NotRequired[JSONSchema7]
  name: NotRequired[str]
  description: NotRequired[str]


LanguageModelV3ResponseFormat: TypeAlias = (
  LanguageModelV3TextResponseFormat | LanguageModelV3JsonResponseFormat
)


class LanguageModelV3CallOptions(TypedDict):
  prompt: LanguageModelV3Prompt
  maxOutputTokens: NotRequired[int]
  temperature: NotRequired[float]
  stopSequences: NotRequired[list[str]]
  topP: NotRequired[float]
  topK: NotRequired[int]
  presencePenalty: NotRequired[float]
  frequencyPenalty: NotRequired[float]
  responseFormat: NotRequired[LanguageModelV3ResponseFormat]
  seed: NotRequired[int]
  tools: NotRequired[list[LanguageModelV3FunctionTool | LanguageModelV3ProviderTool]]
  toolChoice: NotRequired[LanguageModelV3ToolChoice]
  includeRawChunks: NotRequired[bool]
  abortSignal: NotRequired[Any]
  headers: NotRequired[dict[str, str | None]]
  providerOptions: NotRequired[SharedV3ProviderOptions]

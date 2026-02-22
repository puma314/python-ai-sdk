from typing import Any, Literal, NotRequired, TypeAlias, TypedDict

from ...shared.v2.shared_v2_provider_options import SharedV2ProviderOptions
from .language_model_v2_function_tool import JSONSchema7, LanguageModelV2FunctionTool
from .language_model_v2_prompt import LanguageModelV2Prompt
from .language_model_v2_provider_defined_tool import (
  LanguageModelV2ProviderDefinedTool,
)
from .language_model_v2_tool_choice import LanguageModelV2ToolChoice


class LanguageModelV2TextResponseFormat(TypedDict):
  type: Literal['text']


class LanguageModelV2JSONResponseFormat(TypedDict):
  type: Literal['json']
  schema: NotRequired[JSONSchema7]
  name: NotRequired[str]
  description: NotRequired[str]


LanguageModelV2ResponseFormat: TypeAlias = (
  LanguageModelV2TextResponseFormat | LanguageModelV2JSONResponseFormat
)


class LanguageModelV2CallOptions(TypedDict):
  prompt: LanguageModelV2Prompt
  maxOutputTokens: NotRequired[int]
  temperature: NotRequired[float]
  stopSequences: NotRequired[list[str]]
  topP: NotRequired[float]
  topK: NotRequired[int]
  presencePenalty: NotRequired[float]
  frequencyPenalty: NotRequired[float]
  responseFormat: NotRequired[LanguageModelV2ResponseFormat]
  seed: NotRequired[int]
  tools: NotRequired[
    list[LanguageModelV2FunctionTool | LanguageModelV2ProviderDefinedTool]
  ]
  toolChoice: NotRequired[LanguageModelV2ToolChoice]
  includeRawChunks: NotRequired[bool]
  abortSignal: NotRequired[Any]
  headers: NotRequired[dict[str, str | None]]
  providerOptions: NotRequired[SharedV2ProviderOptions]

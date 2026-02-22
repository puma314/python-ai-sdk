from typing import Any, Literal, NotRequired, TypeAlias, TypedDict

from ...json_value.json_value import JSONObject
from ...shared.v3.shared_v3_provider_options import SharedV3ProviderOptions

JSONSchema7: TypeAlias = dict[str, Any]


class LanguageModelV3FunctionToolInputExample(TypedDict):
  input: JSONObject


class LanguageModelV3FunctionTool(TypedDict):
  type: Literal['function']
  name: str
  description: NotRequired[str]
  inputSchema: JSONSchema7
  inputExamples: NotRequired[list[LanguageModelV3FunctionToolInputExample]]
  strict: NotRequired[bool]
  providerOptions: NotRequired[SharedV3ProviderOptions]

from typing import Any, Literal, NotRequired, TypeAlias, TypedDict

from ...shared.v2.shared_v2_provider_options import SharedV2ProviderOptions

JSONSchema7: TypeAlias = dict[str, Any]


class LanguageModelV2FunctionTool(TypedDict):
  type: Literal['function']
  name: str
  description: NotRequired[str]
  inputSchema: JSONSchema7
  providerOptions: NotRequired[SharedV2ProviderOptions]

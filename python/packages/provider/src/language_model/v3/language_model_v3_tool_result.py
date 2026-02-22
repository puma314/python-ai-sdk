from typing import Literal, NotRequired, TypeAlias, TypedDict

from ...shared.v3.shared_v3_provider_metadata import SharedV3ProviderMetadata

NonNullableJSONValue: TypeAlias = (
  str
  | int
  | float
  | bool
  | dict[str, 'NonNullableJSONValue']
  | list['NonNullableJSONValue']
)


class LanguageModelV3ToolResult(TypedDict):
  type: Literal['tool-result']
  toolCallId: str
  toolName: str
  result: NonNullableJSONValue
  isError: NotRequired[bool]
  preliminary: NotRequired[bool]
  dynamic: NotRequired[bool]
  providerMetadata: NotRequired[SharedV3ProviderMetadata]

from typing import Any, Literal, NotRequired, TypedDict

from ...shared.v2.shared_v2_provider_metadata import SharedV2ProviderMetadata


class LanguageModelV2ToolResult(TypedDict):
  type: Literal['tool-result']
  toolCallId: str
  toolName: str
  result: Any
  isError: NotRequired[bool]
  providerExecuted: NotRequired[bool]
  providerMetadata: NotRequired[SharedV2ProviderMetadata]

from typing import Literal, NotRequired, TypedDict

from ...shared.v2.shared_v2_provider_metadata import SharedV2ProviderMetadata


class LanguageModelV2ToolCall(TypedDict):
  type: Literal['tool-call']
  toolCallId: str
  toolName: str
  input: str
  providerExecuted: NotRequired[bool]
  providerMetadata: NotRequired[SharedV2ProviderMetadata]

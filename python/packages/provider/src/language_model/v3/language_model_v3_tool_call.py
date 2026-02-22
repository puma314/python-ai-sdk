from typing import Literal, NotRequired, TypedDict

from ...shared.v3.shared_v3_provider_metadata import SharedV3ProviderMetadata


class LanguageModelV3ToolCall(TypedDict):
  type: Literal['tool-call']
  toolCallId: str
  toolName: str
  input: str
  providerExecuted: NotRequired[bool]
  dynamic: NotRequired[bool]
  title: NotRequired[str]
  providerMetadata: NotRequired[SharedV3ProviderMetadata]

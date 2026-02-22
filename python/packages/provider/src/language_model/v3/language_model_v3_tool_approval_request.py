from typing import Literal, NotRequired, TypedDict

from ...shared.v3.shared_v3_provider_metadata import SharedV3ProviderMetadata


class LanguageModelV3ToolApprovalRequest(TypedDict):
  type: Literal['tool-approval-request']
  approvalId: str
  toolCallId: str
  providerMetadata: NotRequired[SharedV3ProviderMetadata]

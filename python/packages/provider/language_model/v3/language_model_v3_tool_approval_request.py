from __future__ import annotations

"""Tool approval request emitted by a provider for a provider-executed tool call.

Translated from: packages/provider/src/language-model/v3/language-model-v3-tool-approval-request.ts
"""

from dataclasses import dataclass, field
from typing import Literal

from ...shared.v3.shared_v3_provider_metadata import SharedV3ProviderMetadata


@dataclass(frozen=True)
class LanguageModelV3ToolApprovalRequest:
    """Tool approval request emitted by a provider for a provider-executed tool call.

    This is used for flows where the provider executes the tool (e.g. MCP tools)
    but requires an explicit user approval before continuing.
    """

    type: Literal['tool-approval-request'] = 'tool-approval-request'

    approval_id: str = ''
    """ID of the approval request. This ID is referenced by the subsequent
    tool-approval-response (tool message) to approve or deny execution."""

    tool_call_id: str = ''
    """The tool call ID that this approval request is for."""

    provider_metadata: SharedV3ProviderMetadata | None = None
    """Additional provider-specific metadata for the approval request."""

"""
Auto-translated Python mirror for `src/prompt/index.ts`.
"""

from __future__ import annotations

from typing import Any, TypeAlias

try:
  from .call_settings import CallSettings, TimeoutConfiguration
except Exception:
  CallSettings: Any = None
  TimeoutConfiguration: Any = None

try:
  from .message import assistantModelMessageSchema, modelMessageSchema, systemModelMessageSchema, toolModelMessageSchema, userModelMessageSchema
except Exception:
  assistantModelMessageSchema: Any = None
  modelMessageSchema: Any = None
  systemModelMessageSchema: Any = None
  toolModelMessageSchema: Any = None
  userModelMessageSchema: Any = None

try:
  from .prompt import Prompt
except Exception:
  Prompt: Any = None

AssistantContent: Any = None
AssistantModelMessage: Any = None
DataContent: Any = None
FilePart: Any = None
ImagePart: Any = None
ModelMessage: Any = None
SystemModelMessage: Any = None
TextPart: Any = None
ToolCallPart: Any = None
ToolContent: Any = None
ToolModelMessage: Any = None
ToolResultPart: Any = None
UserContent: Any = None
UserModelMessage: Any = None


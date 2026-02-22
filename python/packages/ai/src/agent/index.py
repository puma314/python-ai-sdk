"""
Auto-translated Python mirror for `src/agent/index.ts`.
"""

from __future__ import annotations

from typing import Any, TypeAlias

try:
  from .agent import type_Agent, type_AgentCallParameters, type_AgentStreamParameters
except Exception:
  type_Agent: Any = None
  type_AgentCallParameters: Any = None
  type_AgentStreamParameters: Any = None

try:
  from .tool_loop_agent_settings import type_ToolLoopAgentOnFinishCallback, type_ToolLoopAgentOnStartCallback, type_ToolLoopAgentOnStepFinishCallback, type_ToolLoopAgentOnStepStartCallback, type_ToolLoopAgentOnToolCallFinishCallback, type_ToolLoopAgentOnToolCallStartCallback, type_ToolLoopAgentSettings, Experimental_AgentSettings
except Exception:
  type_ToolLoopAgentOnFinishCallback: Any = None
  type_ToolLoopAgentOnStartCallback: Any = None
  type_ToolLoopAgentOnStepFinishCallback: Any = None
  type_ToolLoopAgentOnStepStartCallback: Any = None
  type_ToolLoopAgentOnToolCallFinishCallback: Any = None
  type_ToolLoopAgentOnToolCallStartCallback: Any = None
  type_ToolLoopAgentSettings: Any = None
  Experimental_AgentSettings: Any = None

try:
  from .tool_loop_agent import ToolLoopAgent, Experimental_Agent
except Exception:
  ToolLoopAgent: Any = None
  Experimental_Agent: Any = None

try:
  from .infer_agent_ui_message import Experimental_InferAgentUIMessage, type_InferAgentUIMessage
except Exception:
  Experimental_InferAgentUIMessage: Any = None
  type_InferAgentUIMessage: Any = None

try:
  from .create_agent_ui_stream_response import createAgentUIStreamResponse
except Exception:
  createAgentUIStreamResponse: Any = None

try:
  from .create_agent_ui_stream import createAgentUIStream
except Exception:
  createAgentUIStream: Any = None

try:
  from .pipe_agent_ui_stream_to_response import pipeAgentUIStreamToResponse
except Exception:
  pipeAgentUIStreamToResponse: Any = None


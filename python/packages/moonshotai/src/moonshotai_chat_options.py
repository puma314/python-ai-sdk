"""MoonshotAI model identifiers and language model options."""

from typing import Literal, TypeAlias

from pydantic import BaseModel


MoonshotAIChatModelId: TypeAlias = Literal[
  'moonshot-v1-8k',
  'moonshot-v1-32k',
  'moonshot-v1-128k',
  'kimi-k2',
  'kimi-k2-0905',
  'kimi-k2-thinking',
  'kimi-k2-thinking-turbo',
  'kimi-k2-turbo',
  'kimi-k2.5',
] | str


class MoonshotAIThinkingOptions(BaseModel):
  """Thinking configuration for Moonshot reasoning models."""

  type: Literal['enabled', 'disabled'] | None = None
  budgetTokens: int | None = None


class MoonshotAILanguageModelOptions(BaseModel):
  """Provider-specific Moonshot language-model settings."""

  thinking: MoonshotAIThinkingOptions | None = None
  reasoningHistory: Literal['disabled', 'interleaved', 'preserved'] | None = None

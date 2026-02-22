"""Model identifiers for Cerebras chat models."""

from typing import Literal, TypeAlias

# https://inference-docs.cerebras.ai/models/overview
CerebrasChatModelId: TypeAlias = Literal[
  'llama3.1-8b',
  'gpt-oss-120b',
  'qwen-3-235b-a22b-instruct-2507',
  'qwen-3-235b-a22b-thinking-2507',
  'zai-glm-4.6',
  'zai-glm-4.7',
] | str

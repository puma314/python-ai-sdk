"""Moonshot chat language model wrapper."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .convert_moonshotai_chat_usage import convertMoonshotAIChatUsage


@dataclass
class OpenAICompatibleChatLanguageModel:
  """Small runtime placeholder for openai-compatible chat model."""

  modelId: str
  config: dict[str, Any]

  async def doGenerate(self, options: dict[str, Any]) -> dict[str, Any]:
    return {
      'content': [],
      'finishReason': {'unified': 'other', 'raw': None},
      'usage': convertMoonshotAIChatUsage(None),
      'warnings': [],
      'response': {'body': {'usage': None}},
    }

  async def doStream(self, options: dict[str, Any]) -> dict[str, Any]:
    async def _empty():
      if False:
        yield {}

    return {
      'stream': _empty(),
      'response': {},
    }


class MoonshotAIChatLanguageModel(OpenAICompatibleChatLanguageModel):
  """Moonshot-specific chat model that normalizes usage payloads."""

  async def doGenerate(self, options: dict[str, Any]) -> dict[str, Any]:
    result = await super().doGenerate(options)
    usage = ((result.get('response') or {}).get('body') or {}).get('usage')
    result['usage'] = convertMoonshotAIChatUsage(usage)
    return result

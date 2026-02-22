"""Tests for conversion to Anthropic messages prompt."""

import pytest

from .convert_to_anthropic_messages_prompt import convertToAnthropicMessagesPrompt


class _IdentityToolNameMapping:
  def toProviderToolName(self, name: str) -> str:
    return name


@pytest.mark.asyncio
async def test_converts_single_system_message():
  result = await convertToAnthropicMessagesPrompt(
    prompt=[{'role': 'system', 'content': 'System message'}],
    sendReasoning=True,
    warnings=[],
    toolNameMapping=_IdentityToolNameMapping(),
  )
  assert result['prompt']['messages'] == []
  assert result['prompt']['system'] == [{'type': 'text', 'text': 'System message', 'cache_control': None}]


@pytest.mark.asyncio
async def test_converts_user_text_message():
  result = await convertToAnthropicMessagesPrompt(
    prompt=[{'role': 'user', 'content': [{'type': 'text', 'text': 'Hello'}]}],
    sendReasoning=True,
    warnings=[],
    toolNameMapping=_IdentityToolNameMapping(),
  )
  assert result['prompt']['messages'][0]['role'] == 'user'
  assert result['prompt']['messages'][0]['content'][0]['text'] == 'Hello'


@pytest.mark.asyncio
async def test_converts_assistant_tool_call():
  result = await convertToAnthropicMessagesPrompt(
    prompt=[
      {
        'role': 'assistant',
        'content': [
          {
            'type': 'tool-call',
            'toolCallId': 'call_1',
            'toolName': 'weather',
            'input': {'city': 'Berlin'},
          }
        ],
      }
    ],
    sendReasoning=True,
    warnings=[],
    toolNameMapping=_IdentityToolNameMapping(),
  )
  assert result['prompt']['messages'][0]['content'][0]['type'] == 'tool_use'

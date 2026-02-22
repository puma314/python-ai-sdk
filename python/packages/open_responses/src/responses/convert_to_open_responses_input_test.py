"""Tests for prompt-to-open-responses conversion."""

import pytest

from .convert_to_open_responses_input import convertToOpenResponsesInput


@pytest.mark.asyncio
async def test_system_message_converted_to_instructions():
  result = await convertToOpenResponsesInput(
    prompt=[{'role': 'system', 'content': 'You are helpful.'}]
  )
  assert result['instructions'] == 'You are helpful.'
  assert result['input'] == []


@pytest.mark.asyncio
async def test_user_text_converted_to_message_item():
  result = await convertToOpenResponsesInput(
    prompt=[
      {
        'role': 'user',
        'content': [{'type': 'text', 'text': 'Hello'}],
      }
    ]
  )
  assert result['input'][0]['role'] == 'user'
  assert result['input'][0]['content'][0]['text'] == 'Hello'


@pytest.mark.asyncio
async def test_assistant_tool_call_converted():
  result = await convertToOpenResponsesInput(
    prompt=[
      {
        'role': 'assistant',
        'content': [
          {
            'type': 'tool-call',
            'toolCallId': 'call_1',
            'toolName': 'get_weather',
            'input': {'location': 'Tokyo'},
          }
        ],
      }
    ]
  )
  assert result['input'][0]['type'] == 'function_call'
  assert result['input'][0]['call_id'] == 'call_1'

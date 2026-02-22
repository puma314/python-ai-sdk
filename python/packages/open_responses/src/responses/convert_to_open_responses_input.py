"""Convert LanguageModelV3 prompt format into Open Responses API input."""

from __future__ import annotations

import base64
import json
from typing import Any, TypedDict

from packages.provider.src.shared.v3.shared_v3_warning import SharedV3Warning

from .open_responses_api import (
  FunctionCallItemParam,
  FunctionCallOutputItemParam,
  InputFileContentParam,
  InputImageContentParam,
  InputTextContentParam,
  OpenResponsesRequestBody,
  OutputTextContentParam,
  RefusalContentParam,
)


class OpenResponsesInputConversion(TypedDict):
  input: OpenResponsesRequestBody['input']
  instructions: str | None
  warnings: list[SharedV3Warning]


def _convert_to_base64(data: str | bytes) -> str:
  if isinstance(data, str):
    return data
  return base64.b64encode(data).decode('utf-8')


async def convertToOpenResponsesInput(*, prompt: list[dict[str, Any]]) -> OpenResponsesInputConversion:
  """Convert v3 prompt messages to Open Responses request items."""

  input_items: list[dict[str, Any]] = []
  warnings: list[SharedV3Warning] = []
  system_messages: list[str] = []

  for message in prompt:
    role = message['role']
    content = message['content']

    if role == 'system':
      system_messages.append(content)
      continue

    if role == 'user':
      user_content: list[
        InputTextContentParam | InputImageContentParam | InputFileContentParam
      ] = []
      for part in content:
        if part['type'] == 'text':
          user_content.append({'type': 'input_text', 'text': part['text']})
        elif part['type'] == 'file':
          media_type = part['mediaType']
          if not media_type.startswith('image/'):
            warnings.append(
              {
                'type': 'other',
                'message': f'unsupported file content type: {media_type}',
              }
            )
            continue
          image_data = part['data']
          if isinstance(image_data, str) and image_data.startswith(('http://', 'https://')):
            user_content.append({'type': 'input_image', 'image_url': image_data})
          else:
            fixed_type = 'image/jpeg' if media_type == 'image/*' else media_type
            encoded = _convert_to_base64(image_data)
            user_content.append(
              {
                'type': 'input_image',
                'image_url': f'data:{fixed_type};base64,{encoded}',
              }
            )
      input_items.append({'type': 'message', 'role': 'user', 'content': user_content})
      continue

    if role == 'assistant':
      assistant_content: list[OutputTextContentParam | RefusalContentParam] = []
      tool_calls: list[FunctionCallItemParam] = []
      for part in content:
        if part['type'] == 'text':
          assistant_content.append({'type': 'output_text', 'text': part['text']})
        elif part['type'] == 'tool-call':
          input_value = part['input']
          arguments_value = input_value if isinstance(input_value, str) else json.dumps(input_value)
          tool_calls.append(
            {
              'type': 'function_call',
              'call_id': part['toolCallId'],
              'name': part['toolName'],
              'arguments': arguments_value,
            }
          )
      if assistant_content:
        input_items.append(
          {'type': 'message', 'role': 'assistant', 'content': assistant_content}
        )
      input_items.extend(tool_calls)
      continue

    if role == 'tool':
      for part in content:
        if part.get('type') != 'tool-result':
          continue
        output = part['output']
        output_type = output['type']
        if output_type in ('text', 'error-text'):
          content_value: FunctionCallOutputItemParam['output'] = output['value']
        elif output_type == 'execution-denied':
          content_value = output.get('reason') or 'Tool execution denied.'
        elif output_type in ('json', 'error-json'):
          content_value = json.dumps(output['value'])
        else:
          # Compact fallback for rich content parts.
          content_value = json.dumps(output.get('value'))
        input_items.append(
          {
            'type': 'function_call_output',
            'call_id': part['toolCallId'],
            'output': content_value,
          }
        )

  instructions = '\n'.join(system_messages) if system_messages else None
  return {'input': input_items, 'instructions': instructions, 'warnings': warnings}

"""Prompt conversion into Anthropic messages format."""

from __future__ import annotations

import base64
import json
from typing import Any

from packages.provider.src.errors.unsupported_functionality_error import (
  UnsupportedFunctionalityError,
)

from .get_cache_control import CacheControlValidator


def _convertToBase64(data: str | bytes) -> str:
  if isinstance(data, bytes):
    return base64.b64encode(data).decode('utf-8')
  return data


def _convertToString(data: str | bytes) -> str:
  if isinstance(data, bytes):
    return data.decode('utf-8')
  return base64.b64decode(data).decode('utf-8')


def _isUrlData(data: object) -> bool:
  return isinstance(data, str) and data.lower().startswith(('http://', 'https://'))


def _groupIntoBlocks(prompt: list[dict[str, Any]]) -> list[dict[str, Any]]:
  blocks: list[dict[str, Any]] = []
  current: dict[str, Any] | None = None
  for message in prompt:
    role = message['role']
    block_type = 'user' if role in {'user', 'tool'} else role
    if current is None or current['type'] != block_type:
      current = {'type': block_type, 'messages': []}
      blocks.append(current)
    current['messages'].append(message)
  return blocks


async def convertToAnthropicMessagesPrompt(
  *,
  prompt: list[dict[str, Any]],
  sendReasoning: bool,
  warnings: list[dict[str, str]],
  cacheControlValidator: CacheControlValidator | None = None,
  toolNameMapping: Any,
) -> dict[str, Any]:
  """Convert generic prompt format to Anthropic messages API payload."""

  betas: set[str] = set()
  blocks = _groupIntoBlocks(prompt)
  validator = cacheControlValidator or CacheControlValidator()

  system: list[dict[str, Any]] | None = None
  messages: list[dict[str, Any]] = []

  for block_index, block in enumerate(blocks):
    block_type = block['type']
    is_last_block = block_index == len(blocks) - 1

    if block_type == 'system':
      if system is not None:
        raise UnsupportedFunctionalityError(
          functionality='Multiple system messages that are separated by user/assistant messages'
        )
      system = []
      for message in block['messages']:
        system.append(
          {
            'type': 'text',
            'text': message['content'],
            'cache_control': validator.getCacheControl(
              message.get('providerOptions'),
              {'type': 'system message', 'canCache': True},
            ),
          }
        )
      continue

    if block_type == 'user':
      anthropic_content: list[dict[str, Any]] = []
      for message in block['messages']:
        role = message['role']
        if role == 'user':
          for index, part in enumerate(message['content']):
            is_last_part = index == len(message['content']) - 1
            cache_control = validator.getCacheControl(
              part.get('providerOptions'),
              {'type': 'user message part', 'canCache': True},
            ) or (
              validator.getCacheControl(
                message.get('providerOptions'),
                {'type': 'user message', 'canCache': True},
              )
              if is_last_part
              else None
            )

            if part['type'] == 'text':
              anthropic_content.append(
                {'type': 'text', 'text': part['text'], 'cache_control': cache_control}
              )
              continue

            if part['type'] == 'file':
              media_type = part['mediaType']
              data = part['data']
              if media_type.startswith('image/'):
                anthropic_content.append(
                  {
                    'type': 'image',
                    'source': (
                      {'type': 'url', 'url': data}
                      if _isUrlData(data)
                      else {
                        'type': 'base64',
                        'media_type': 'image/jpeg' if media_type == 'image/*' else media_type,
                        'data': _convertToBase64(data),
                      }
                    ),
                    'cache_control': cache_control,
                  }
                )
                continue

              if media_type == 'application/pdf':
                betas.add('pdfs-2024-09-25')
                anthropic_options = ((part.get('providerOptions') or {}).get('anthropic') or {})
                document: dict[str, Any] = {
                  'type': 'document',
                  'source': (
                    {'type': 'url', 'url': data}
                    if _isUrlData(data)
                    else {
                      'type': 'base64',
                      'media_type': 'application/pdf',
                      'data': _convertToBase64(data),
                    }
                  ),
                  'title': anthropic_options.get('title') or part.get('filename'),
                  'cache_control': cache_control,
                }
                if anthropic_options.get('context'):
                  document['context'] = anthropic_options['context']
                citations = anthropic_options.get('citations')
                if isinstance(citations, dict) and citations.get('enabled'):
                  document['citations'] = {'enabled': True}
                anthropic_content.append(document)
                continue

              if media_type == 'text/plain':
                anthropic_options = ((part.get('providerOptions') or {}).get('anthropic') or {})
                document = {
                  'type': 'document',
                  'source': (
                    {'type': 'url', 'url': data}
                    if _isUrlData(data)
                    else {
                      'type': 'text',
                      'media_type': 'text/plain',
                      'data': _convertToString(data),
                    }
                  ),
                  'title': anthropic_options.get('title') or part.get('filename'),
                  'cache_control': cache_control,
                }
                if anthropic_options.get('context'):
                  document['context'] = anthropic_options['context']
                citations = anthropic_options.get('citations')
                if isinstance(citations, dict) and citations.get('enabled'):
                  document['citations'] = {'enabled': True}
                anthropic_content.append(document)
                continue

              raise UnsupportedFunctionalityError(functionality=f'media type: {media_type}')

        elif role == 'tool':
          for index, part in enumerate(message['content']):
            if part['type'] == 'tool-approval-response':
              continue
            is_last_part = index == len(message['content']) - 1
            cache_control = validator.getCacheControl(
              part.get('providerOptions'),
              {'type': 'tool result part', 'canCache': True},
            ) or (
              validator.getCacheControl(
                message.get('providerOptions'),
                {'type': 'tool result message', 'canCache': True},
              )
              if is_last_part
              else None
            )
            output = part['output']
            output_type = output['type']
            if output_type in {'text', 'error-text'}:
              content_value: Any = output['value']
            elif output_type == 'execution-denied':
              content_value = output.get('reason') or 'Tool execution denied.'
            elif output_type == 'content':
              converted_parts: list[dict[str, Any]] = []
              for content_part in output['value']:
                ctype = content_part['type']
                if ctype == 'text':
                  converted_parts.append({'type': 'text', 'text': content_part['text']})
                elif ctype == 'image-data':
                  converted_parts.append(
                    {
                      'type': 'image',
                      'source': {
                        'type': 'base64',
                        'media_type': content_part['mediaType'],
                        'data': content_part['data'],
                      },
                    }
                  )
                elif ctype == 'image-url':
                  converted_parts.append(
                    {'type': 'image', 'source': {'type': 'url', 'url': content_part['url']}}
                  )
                elif ctype == 'file-url':
                  converted_parts.append(
                    {'type': 'document', 'source': {'type': 'url', 'url': content_part['url']}}
                  )
                elif ctype == 'file-data' and content_part['mediaType'] == 'application/pdf':
                  betas.add('pdfs-2024-09-25')
                  converted_parts.append(
                    {
                      'type': 'document',
                      'source': {
                        'type': 'base64',
                        'media_type': content_part['mediaType'],
                        'data': content_part['data'],
                      },
                    }
                  )
                elif ctype == 'custom':
                  anthropic_options = (content_part.get('providerOptions') or {}).get('anthropic')
                  if isinstance(anthropic_options, dict) and anthropic_options.get('type') == 'tool-reference':
                    converted_parts.append(
                      {'type': 'tool_reference', 'tool_name': anthropic_options.get('toolName')}
                    )
                  else:
                    warnings.append({'type': 'other', 'message': 'unsupported custom tool content part'})
                else:
                  warnings.append({'type': 'other', 'message': f'unsupported tool content part type: {ctype}'})
              content_value = converted_parts
            else:
              content_value = json.dumps(output.get('value'))

            anthropic_content.append(
              {
                'type': 'tool_result',
                'tool_use_id': part['toolCallId'],
                'content': content_value,
                'is_error': output_type in {'error-text', 'error-json'} or None,
                'cache_control': cache_control,
              }
            )

      messages.append({'role': 'user', 'content': anthropic_content})
      continue

    if block_type == 'assistant':
      assistant_content: list[dict[str, Any]] = []
      for message_index, message in enumerate(block['messages']):
        is_last_message = message_index == len(block['messages']) - 1
        for index, part in enumerate(message['content']):
          is_last_part = index == len(message['content']) - 1
          cache_control = validator.getCacheControl(
            part.get('providerOptions'),
            {'type': 'assistant message part', 'canCache': True},
          ) or (
            validator.getCacheControl(
              message.get('providerOptions'),
              {'type': 'assistant message', 'canCache': True},
            )
            if is_last_part
            else None
          )
          part_type = part['type']
          if part_type == 'text':
            text_value = (
              part['text'].strip()
              if is_last_block and is_last_message and is_last_part
              else part['text']
            )
            assistant_content.append({'type': 'text', 'text': text_value, 'cache_control': cache_control})
          elif part_type == 'reasoning':
            if not sendReasoning:
              warnings.append({'type': 'other', 'message': 'sending reasoning content is disabled for this model'})
              continue
            anthropic_options = (part.get('providerOptions') or {}).get('anthropic')
            if isinstance(anthropic_options, dict) and anthropic_options.get('signature'):
              validator.getCacheControl(
                part.get('providerOptions'),
                {'type': 'thinking block', 'canCache': False},
              )
              assistant_content.append(
                {
                  'type': 'thinking',
                  'thinking': part['text'],
                  'signature': anthropic_options['signature'],
                }
              )
            elif isinstance(anthropic_options, dict) and anthropic_options.get('redactedData'):
              validator.getCacheControl(
                part.get('providerOptions'),
                {'type': 'redacted thinking block', 'canCache': False},
              )
              assistant_content.append(
                {
                  'type': 'redacted_thinking',
                  'data': anthropic_options['redactedData'],
                }
              )
            else:
              warnings.append({'type': 'other', 'message': 'unsupported reasoning metadata'})
          elif part_type == 'tool-call':
            if part.get('providerExecuted'):
              provider_tool_name = toolNameMapping.toProviderToolName(part['toolName'])
              assistant_content.append(
                {
                  'type': 'server_tool_use',
                  'id': part['toolCallId'],
                  'name': provider_tool_name,
                  'input': part['input'],
                  'cache_control': cache_control,
                }
              )
            else:
              caller_options = ((part.get('providerOptions') or {}).get('anthropic') or {}).get('caller')
              caller = None
              if isinstance(caller_options, dict):
                if caller_options.get('type') == 'code_execution_20250825' and caller_options.get('toolId'):
                  caller = {'type': 'code_execution_20250825', 'tool_id': caller_options['toolId']}
                elif caller_options.get('type') == 'direct':
                  caller = {'type': 'direct'}
              entry: dict[str, Any] = {
                'type': 'tool_use',
                'id': part['toolCallId'],
                'name': part['toolName'],
                'input': part['input'],
                'cache_control': cache_control,
              }
              if caller is not None:
                entry['caller'] = caller
              assistant_content.append(entry)
          elif part_type == 'tool-result':
            warnings.append(
              {
                'type': 'other',
                'message': f"provider executed tool result for tool {part.get('toolName')} is not supported",
              }
            )

      messages.append({'role': 'assistant', 'content': assistant_content})
      continue

    raise UnsupportedFunctionalityError(functionality=f'Unsupported block type: {block_type}')

  return {'prompt': {'system': system, 'messages': messages}, 'betas': betas}


__all__ = ['convertToAnthropicMessagesPrompt']

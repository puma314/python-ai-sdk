"""Tool conversion for Anthropic messages API."""

from __future__ import annotations

from typing import Literal, TypedDict

from packages.provider.src.errors.unsupported_functionality_error import (
  UnsupportedFunctionalityError,
)

from .get_cache_control import CacheControlValidator


class AnthropicToolOptions(TypedDict, total=False):
  deferLoading: bool
  allowedCallers: list[Literal['code_execution_20250825']]


async def prepareTools(
  *,
  tools: list[dict[str, object]] | None,
  toolChoice: dict[str, object] | None,
  disableParallelToolUse: bool | None = None,
  cacheControlValidator: CacheControlValidator | None = None,
  supportsStructuredOutput: bool,
) -> dict[str, object]:
  """Prepare Anthropic tools and tool choice payload."""

  if not tools:
    return {
      'tools': None,
      'toolChoice': None,
      'toolWarnings': [],
      'betas': set(),
    }

  validator = cacheControlValidator or CacheControlValidator()
  tool_warnings: list[dict[str, str]] = []
  betas: set[str] = set()
  anthropic_tools: list[dict[str, object]] = []

  for tool in tools:
    tool_type = tool.get('type')

    if tool_type == 'function':
      provider_options = tool.get('providerOptions')
      cache_control = validator.getCacheControl(
        provider_options if isinstance(provider_options, dict) else None,
        {'type': 'tool definition', 'canCache': True},
      )
      converted: dict[str, object] = {
        'name': tool.get('name'),
        'description': tool.get('description'),
        'input_schema': tool.get('inputSchema'),
        'cache_control': cache_control,
      }
      if supportsStructuredOutput and tool.get('strict') is not None:
        converted['strict'] = tool.get('strict')
        betas.add('structured-outputs-2025-11-13')

      provider_options_dict = (
        tool.get('providerOptions') if isinstance(tool.get('providerOptions'), dict) else {}
      )
      provider_options = (
        provider_options_dict.get('anthropic')
        if isinstance(provider_options_dict, dict)
        else None
      )
      if isinstance(provider_options, dict):
        if 'deferLoading' in provider_options:
          converted['defer_loading'] = provider_options['deferLoading']
        if 'allowedCallers' in provider_options:
          converted['allowed_callers'] = provider_options['allowedCallers']
          betas.add('advanced-tool-use-2025-11-20')
      if tool.get('inputExamples') is not None:
        converted['input_examples'] = [
          example.get('input')
          for example in tool.get('inputExamples', [])
          if isinstance(example, dict)
        ]
        betas.add('advanced-tool-use-2025-11-20')

      anthropic_tools.append(converted)
      continue

    if tool_type == 'provider':
      tool_id = str(tool.get('id'))
      args_obj = tool.get('args')
      args: dict[str, object] = args_obj if isinstance(args_obj, dict) else {}
      if tool_id == 'anthropic.web_fetch_20250910':
        betas.add('web-fetch-2025-09-10')
        anthropic_tools.append(
          {
            'type': 'web_fetch_20250910',
            'name': 'web_fetch',
            'max_uses': args.get('maxUses'),
            'allowed_domains': args.get('allowedDomains'),
            'blocked_domains': args.get('blockedDomains'),
            'citations': args.get('citations'),
            'max_content_tokens': args.get('maxContentTokens'),
            'cache_control': None,
          }
        )
      elif tool_id == 'anthropic.web_search_20250305':
        anthropic_tools.append(
          {
            'type': 'web_search_20250305',
            'name': 'web_search',
            'max_uses': args.get('maxUses'),
            'allowed_domains': args.get('allowedDomains'),
            'blocked_domains': args.get('blockedDomains'),
            'user_location': args.get('userLocation'),
            'cache_control': None,
          }
        )
      elif tool_id == 'anthropic.tool_search_regex_20251119':
        betas.add('advanced-tool-use-2025-11-20')
        anthropic_tools.append(
          {'type': 'tool_search_tool_regex_20251119', 'name': 'tool_search_tool_regex'}
        )
      elif tool_id == 'anthropic.tool_search_bm25_20251119':
        betas.add('advanced-tool-use-2025-11-20')
        anthropic_tools.append(
          {'type': 'tool_search_tool_bm25_20251119', 'name': 'tool_search_tool_bm25'}
        )
      elif tool_id.startswith('anthropic.'):
        # Preserve generic provider-defined Anthropic tools.
        anth_type = tool_id.split('.', maxsplit=1)[1]
        anthropic_tools.append(
          {
            'type': anth_type,
            'name': str(tool.get('name') or anth_type.split('_')[0]),
            **dict(args),
          }
        )
      else:
        tool_warnings.append(
          {
            'type': 'unsupported',
            'feature': f'provider-defined tool {tool_id}',
          }
        )
      continue

    tool_warnings.append({'type': 'unsupported', 'feature': f'tool {tool}'})

  if toolChoice is None:
    return {
      'tools': anthropic_tools,
      'toolChoice': (
        {'type': 'auto', 'disable_parallel_tool_use': bool(disableParallelToolUse)}
        if disableParallelToolUse
        else None
      ),
      'toolWarnings': tool_warnings + validator.getWarnings(),
      'betas': betas,
    }

  choice_type = str(toolChoice.get('type'))
  if choice_type == 'auto':
    anthropic_choice = {
      'type': 'auto',
      'disable_parallel_tool_use': disableParallelToolUse,
    }
  elif choice_type == 'required':
    anthropic_choice = {
      'type': 'any',
      'disable_parallel_tool_use': disableParallelToolUse,
    }
  elif choice_type == 'none':
    return {
      'tools': None,
      'toolChoice': None,
      'toolWarnings': tool_warnings + validator.getWarnings(),
      'betas': betas,
    }
  elif choice_type == 'tool':
    anthropic_choice = {
      'type': 'tool',
      'name': str(toolChoice.get('toolName')),
      'disable_parallel_tool_use': disableParallelToolUse,
    }
  else:
    raise UnsupportedFunctionalityError(
      functionality=f'tool choice type: {choice_type}'
    )

  return {
    'tools': anthropic_tools,
    'toolChoice': anthropic_choice,
    'toolWarnings': tool_warnings + validator.getWarnings(),
    'betas': betas,
  }


__all__ = ['AnthropicToolOptions', 'prepareTools']

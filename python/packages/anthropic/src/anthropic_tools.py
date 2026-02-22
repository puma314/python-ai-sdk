"""Anthropic tool factory exports."""

from __future__ import annotations

def _provider_tool(tool_id: str, **kwargs):
  return {'type': 'provider', 'id': tool_id, 'name': tool_id.split('.')[-1], 'args': kwargs}


def bash_20241022():
  return _provider_tool('anthropic.bash_20241022')


def bash_20250124():
  return _provider_tool('anthropic.bash_20250124')


def codeExecution_20250522():
  return _provider_tool('anthropic.code_execution_20250522')


def codeExecution_20250825():
  return _provider_tool('anthropic.code_execution_20250825')


def computer_20241022(*, displayWidthPx: int, displayHeightPx: int, displayNumber: int):
  return _provider_tool(
    'anthropic.computer_20241022',
    displayWidthPx=displayWidthPx,
    displayHeightPx=displayHeightPx,
    displayNumber=displayNumber,
  )


def computer_20250124(*, displayWidthPx: int, displayHeightPx: int, displayNumber: int):
  return _provider_tool(
    'anthropic.computer_20250124',
    displayWidthPx=displayWidthPx,
    displayHeightPx=displayHeightPx,
    displayNumber=displayNumber,
  )


def computer_20251124(
  *,
  displayWidthPx: int,
  displayHeightPx: int,
  displayNumber: int,
  enableZoom: bool = False,
):
  return _provider_tool(
    'anthropic.computer_20251124',
    displayWidthPx=displayWidthPx,
    displayHeightPx=displayHeightPx,
    displayNumber=displayNumber,
    enableZoom=enableZoom,
  )


def textEditor_20241022():
  return _provider_tool('anthropic.text_editor_20241022')


def textEditor_20250124():
  return _provider_tool('anthropic.text_editor_20250124')


def textEditor_20250429():
  return _provider_tool('anthropic.text_editor_20250429')


def textEditor_20250728(*, maxCharacters: int | None = None):
  return _provider_tool('anthropic.text_editor_20250728', maxCharacters=maxCharacters)


def memory_20250818():
  return _provider_tool('anthropic.memory_20250818')


def webSearch_20250305(**kwargs):
  return _provider_tool('anthropic.web_search_20250305', **kwargs)


def webFetch_20250910(**kwargs):
  return _provider_tool('anthropic.web_fetch_20250910', **kwargs)


def toolSearchRegex_20251119():
  return _provider_tool('anthropic.tool_search_regex_20251119')


def toolSearchBm25_20251119():
  return _provider_tool('anthropic.tool_search_bm25_20251119')


anthropicTools = {
  'bash_20241022': bash_20241022,
  'bash_20250124': bash_20250124,
  'codeExecution_20250522': codeExecution_20250522,
  'codeExecution_20250825': codeExecution_20250825,
  'computer_20241022': computer_20241022,
  'computer_20250124': computer_20250124,
  'computer_20251124': computer_20251124,
  'memory_20250818': memory_20250818,
  'textEditor_20241022': textEditor_20241022,
  'textEditor_20250124': textEditor_20250124,
  'textEditor_20250429': textEditor_20250429,
  'textEditor_20250728': textEditor_20250728,
  'webFetch_20250910': webFetch_20250910,
  'webSearch_20250305': webSearch_20250305,
  'toolSearchRegex_20251119': toolSearchRegex_20251119,
  'toolSearchBm25_20251119': toolSearchBm25_20251119,
}

__all__ = ['anthropicTools']

"""Tests for Anthropic tool preparation."""

import pytest

from .anthropic_prepare_tools import prepareTools


@pytest.mark.asyncio
async def test_returns_none_when_tools_missing():
  result = await prepareTools(
    tools=None,
    toolChoice=None,
    supportsStructuredOutput=True,
  )
  assert result == {
    'tools': None,
    'toolChoice': None,
    'toolWarnings': [],
    'betas': set(),
  }


@pytest.mark.asyncio
async def test_prepares_function_tool():
  result = await prepareTools(
    tools=[
      {
        'type': 'function',
        'name': 'testFunction',
        'description': 'A test function',
        'inputSchema': {'type': 'object', 'properties': {}},
      }
    ],
    toolChoice=None,
    supportsStructuredOutput=True,
  )
  assert result['tools'][0]['name'] == 'testFunction'
  assert result['toolChoice'] is None


@pytest.mark.asyncio
async def test_tool_choice_required_maps_to_any():
  result = await prepareTools(
    tools=[
      {
        'type': 'function',
        'name': 'testFunction',
        'description': 'A test function',
        'inputSchema': {'type': 'object', 'properties': {}},
      }
    ],
    toolChoice={'type': 'required'},
    supportsStructuredOutput=True,
  )
  assert result['toolChoice']['type'] == 'any'

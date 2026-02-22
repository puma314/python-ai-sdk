"""Tests for finish-reason mapper."""

from .map_open_responses_finish_reason import mapOpenResponsesFinishReason


def test_tool_calls_when_undefined_and_has_tool_calls():
  assert mapOpenResponsesFinishReason(finishReason=None, hasToolCalls=True) == 'tool-calls'


def test_stop_when_undefined_without_tool_calls():
  assert mapOpenResponsesFinishReason(finishReason=None, hasToolCalls=False) == 'stop'


def test_length_mapping():
  assert (
    mapOpenResponsesFinishReason(
      finishReason='max_output_tokens',
      hasToolCalls=False,
    )
    == 'length'
  )


def test_unknown_reason_other_without_tool_calls():
  assert (
    mapOpenResponsesFinishReason(
      finishReason='completed',
      hasToolCalls=False,
    )
    == 'other'
  )

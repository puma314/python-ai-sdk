"""Tests for Anthropic error parsing helpers."""

from .anthropic_error import AnthropicErrorData, anthropicFailedResponseHandler


def test_anthropic_error_data_parses_overloaded_error():
  payload = {
    'type': 'error',
    'error': {
      'type': 'overloaded_error',
      'message': 'Overloaded',
    },
  }
  parsed = AnthropicErrorData.model_validate(payload)
  assert parsed.error.type == 'overloaded_error'
  assert parsed.error.message == 'Overloaded'


def test_failed_response_handler_returns_error_message():
  payload = {
    'type': 'error',
    'error': {'type': 'invalid_request_error', 'message': 'Bad request'},
  }
  assert anthropicFailedResponseHandler(payload) == 'Bad request'

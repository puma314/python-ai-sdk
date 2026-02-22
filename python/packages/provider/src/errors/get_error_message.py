"""Helpers for deriving a human-readable error message."""

import json


def getErrorMessage(error: object | None) -> str:
  """Return a normalized message string from unknown error values."""

  if error is None:
    return 'unknown error'

  if isinstance(error, str):
    return error

  if isinstance(error, BaseException):
    return str(error)

  try:
    return json.dumps(error)
  except TypeError:
    return str(error)

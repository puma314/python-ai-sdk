from __future__ import annotations

from typing import Any, TypeGuard

from .json_value import JSONArray, JSONObject, JSONValue


def is_json_value(value: Any) -> TypeGuard[JSONValue]:
  if value is None or isinstance(value, (str, int, float, bool)):
    return True

  if isinstance(value, list):
    return all(is_json_value(item) for item in value)

  if isinstance(value, dict):
    return all(
      isinstance(key, str) and (val is None or is_json_value(val))
      for key, val in value.items()
    )

  return False


def is_json_array(value: Any) -> TypeGuard[JSONArray]:
  return isinstance(value, list) and all(is_json_value(item) for item in value)


def is_json_object(value: Any) -> TypeGuard[JSONObject]:
  return isinstance(value, dict) and all(
    isinstance(key, str) and (val is None or is_json_value(val))
    for key, val in value.items()
  )

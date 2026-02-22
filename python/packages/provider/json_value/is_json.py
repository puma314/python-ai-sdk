from __future__ import annotations

"""JSON value type guard functions.

Translated from: packages/provider/src/json-value/is-json.ts
"""

from typing import Any

from .json_value import JSONArray, JSONObject, JSONValue


def is_json_value(value: Any) -> bool:
    """Check if a value is a valid JSON value.

    A JSON value is None, str, int, float, bool, a list of JSON values,
    or a dict with string keys and JSON values.

    Args:
        value: The value to check.

    Returns:
        True if the value is a valid JSON value.
    """
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


def is_json_array(value: Any) -> bool:
    """Check if a value is a valid JSON array.

    Args:
        value: The value to check.

    Returns:
        True if the value is a list where every element is a valid JSON value.
    """
    return isinstance(value, list) and all(is_json_value(item) for item in value)


def is_json_object(value: Any) -> bool:
    """Check if a value is a valid JSON object.

    Args:
        value: The value to check.

    Returns:
        True if the value is a dict with string keys and valid JSON values.
    """
    return (
        value is not None
        and isinstance(value, dict)
        and all(
            isinstance(key, str) and (val is None or is_json_value(val))
            for key, val in value.items()
        )
    )

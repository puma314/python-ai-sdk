from __future__ import annotations

"""JSON value type definitions.

A JSON value can be a string, number, boolean, object, array, or None.
JSON values can be serialized and deserialized by the json.dumps and json.loads methods.

Translated from: packages/provider/src/json-value/json-value.ts
"""

from typing import Union

JSONValue = Union[None, str, int, float, bool, "JSONObject", "JSONArray"]

JSONObject = dict[str, JSONValue | None]

JSONArray = list[JSONValue]

from __future__ import annotations

from typing import TypeAlias

JSONValue: TypeAlias = (
  None | str | int | float | bool | 'JSONObject' | 'JSONArray'
)

# TypeScript includes `undefined` in object values. In Python, absent keys are
# represented by omission, so this alias keeps values JSON-serializable.
JSONObject: TypeAlias = dict[str, JSONValue]
JSONArray: TypeAlias = list[JSONValue]

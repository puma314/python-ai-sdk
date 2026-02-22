from typing import TypeAlias

from ...json_value.json_value import JSONValue

SharedV2ProviderMetadata: TypeAlias = dict[str, dict[str, JSONValue]]

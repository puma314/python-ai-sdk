from typing import Any, Literal, TypedDict

from ...shared.dotted_id import DottedId


class LanguageModelV2ProviderDefinedTool(TypedDict):
  type: Literal['provider-defined']
  id: DottedId
  name: str
  args: dict[str, Any]

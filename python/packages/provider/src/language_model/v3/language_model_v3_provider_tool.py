from typing import Any, Literal, TypedDict

from ...shared.dotted_id import DottedId


class LanguageModelV3ProviderTool(TypedDict):
  type: Literal['provider']
  id: DottedId
  name: str
  args: dict[str, Any]

from typing import Any, Literal, TypedDict


class LanguageModelV3ProviderTool(TypedDict):
  type: Literal['provider']
  id: str
  name: str
  args: dict[str, Any]

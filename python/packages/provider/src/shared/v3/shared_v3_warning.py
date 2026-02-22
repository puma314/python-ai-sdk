from typing import Literal, NotRequired, TypeAlias, TypedDict


class SharedV3UnsupportedWarning(TypedDict):
  type: Literal['unsupported']
  feature: str
  details: NotRequired[str]


class SharedV3CompatibilityWarning(TypedDict):
  type: Literal['compatibility']
  feature: str
  details: NotRequired[str]


class SharedV3OtherWarning(TypedDict):
  type: Literal['other']
  message: str


SharedV3Warning: TypeAlias = (
  SharedV3UnsupportedWarning
  | SharedV3CompatibilityWarning
  | SharedV3OtherWarning
)

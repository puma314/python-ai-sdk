"""Image file definitions for image-model v3 calls."""

from typing import Literal, NotRequired, TypeAlias, TypedDict

from ...shared.v3.shared_v3_provider_metadata import SharedV3ProviderMetadata


class ImageModelV3BinaryFile(TypedDict):
  """Image provided as inline file data."""

  type: Literal['file']
  mediaType: str
  data: str | bytes
  providerOptions: NotRequired[SharedV3ProviderMetadata]


class ImageModelV3URLFile(TypedDict):
  """Image provided as a URL."""

  type: Literal['url']
  url: str
  providerOptions: NotRequired[SharedV3ProviderMetadata]


ImageModelV3File: TypeAlias = ImageModelV3BinaryFile | ImageModelV3URLFile
from typing import Literal, NotRequired, TypeAlias, TypedDict

from ...shared.v3.shared_v3_provider_metadata import SharedV3ProviderMetadata


class ImageModelV3DataFile(TypedDict):
  type: Literal['file']
  mediaType: str
  data: str | bytes
  providerOptions: NotRequired[SharedV3ProviderMetadata]


class ImageModelV3URLFile(TypedDict):
  type: Literal['url']
  url: str
  providerOptions: NotRequired[SharedV3ProviderMetadata]


ImageModelV3File: TypeAlias = ImageModelV3DataFile | ImageModelV3URLFile

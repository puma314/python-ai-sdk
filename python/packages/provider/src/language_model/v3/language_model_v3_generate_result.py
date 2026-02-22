from typing import Any, NotRequired, TypedDict

from ...shared.v3.shared_v3_headers import SharedV3Headers
from ...shared.v3.shared_v3_provider_metadata import SharedV3ProviderMetadata
from ...shared.v3.shared_v3_warning import SharedV3Warning
from .language_model_v3_content import LanguageModelV3Content
from .language_model_v3_finish_reason import LanguageModelV3FinishReason
from .language_model_v3_response_metadata import LanguageModelV3ResponseMetadata
from .language_model_v3_usage import LanguageModelV3Usage


class LanguageModelV3GenerateRequestInfo(TypedDict):
  body: NotRequired[Any]


class LanguageModelV3GenerateResponseInfo(LanguageModelV3ResponseMetadata):
  headers: NotRequired[SharedV3Headers]
  body: NotRequired[Any]


class LanguageModelV3GenerateResult(TypedDict):
  content: list[LanguageModelV3Content]
  finishReason: LanguageModelV3FinishReason
  usage: LanguageModelV3Usage
  providerMetadata: NotRequired[SharedV3ProviderMetadata]
  request: NotRequired[LanguageModelV3GenerateRequestInfo]
  response: NotRequired[LanguageModelV3GenerateResponseInfo]
  warnings: list[SharedV3Warning]

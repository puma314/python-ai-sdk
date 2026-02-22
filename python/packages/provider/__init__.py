from __future__ import annotations

"""Public API for the provider package.

Translated from: packages/provider/src/index.ts
"""

from typing import Any

from .embedding_model import (
    EmbeddingModelV2,
    EmbeddingModelV2DoEmbedResponse,
    EmbeddingModelV2Embedding,
    EmbeddingModelV2ResponseMetadata,
    EmbeddingModelV2TokenUsage,
    EmbeddingModelV3,
    EmbeddingModelV3CallOptions,
    EmbeddingModelV3Embedding,
    EmbeddingModelV3Result,
    EmbeddingModelV3ResultResponse,
    EmbeddingModelV3ResultUsage,
)
from .errors import (
    AISDKError,
    APICallError,
    EmptyResponseBodyError,
    InvalidArgumentError,
    InvalidPromptError,
    InvalidResponseDataError,
    JSONParseError,
    LoadAPIKeyError,
    LoadSettingError,
    NoContentGeneratedError,
    NoSuchModelError,
    TooManyEmbeddingValuesForCallError,
    TypeValidationContext,
    TypeValidationError,
    UnsupportedFunctionalityError,
    get_error_message,
)
from .image_model import (
    ImageModelV2,
    ImageModelV2CallOptions,
    ImageModelV2CallWarning,
    ImageModelV2ProviderMetadata,
    ImageModelV3,
    ImageModelV3CallOptions,
    ImageModelV3File,
    ImageModelV3ProviderMetadata,
    ImageModelV3Usage,
)
from .image_model_middleware import (
    ImageModelV3Middleware,
)
from .json_value import (
    JSONArray,
    JSONObject,
    JSONValue,
    is_json_array,
    is_json_object,
    is_json_value,
)
from .language_model_middleware import (
    LanguageModelV2Middleware,
    LanguageModelV3Middleware,
)
from .embedding_model_middleware import (
    EmbeddingModelV3Middleware,
)
from .language_model import *  # noqa: F401,F403
from .provider import (
    ProviderV2,
    ProviderV3,
)
from .reranking_model import (
    RerankingModelV3,
    RerankingModelV3CallOptions,
)
from .shared import (
    CompatibilityWarning,
    OtherWarning,
    SharedV2Headers,
    SharedV2ProviderMetadata,
    SharedV2ProviderOptions,
    SharedV3Headers,
    SharedV3ProviderMetadata,
    SharedV3ProviderOptions,
    SharedV3Warning,
    UnsupportedWarning,
)
from .speech_model import (
    SpeechModelV2,
    SpeechModelV2CallOptions,
    SpeechModelV2CallWarning,
    SpeechModelV3,
    SpeechModelV3CallOptions,
)
from .transcription_model import (
    TranscriptionModelV2,
    TranscriptionModelV2CallOptions,
    TranscriptionModelV2CallWarning,
    TranscriptionModelV3,
    TranscriptionModelV3CallOptions,
)
from .video_model import (
    Experimental_VideoModelV3,
    Experimental_VideoModelV3CallOptions,
    Experimental_VideoModelV3File,
    Experimental_VideoModelV3VideoData,
)

# JSON Schema types — in Python, JSON Schema is represented as plain dicts.
# These type aliases correspond to the `JSONSchema7` and `JSONSchema7Definition`
# types from the `json-schema` npm package.
JSONSchema7 = dict[str, Any]
JSONSchema7Definition = JSONSchema7 | bool

__all__ = [
    # embedding_model
    "EmbeddingModelV2",
    "EmbeddingModelV2DoEmbedResponse",
    "EmbeddingModelV2Embedding",
    "EmbeddingModelV2ResponseMetadata",
    "EmbeddingModelV2TokenUsage",
    "EmbeddingModelV3",
    "EmbeddingModelV3CallOptions",
    "EmbeddingModelV3Embedding",
    "EmbeddingModelV3Result",
    "EmbeddingModelV3ResultResponse",
    "EmbeddingModelV3ResultUsage",
    # errors
    "AISDKError",
    "APICallError",
    "EmptyResponseBodyError",
    "InvalidArgumentError",
    "InvalidPromptError",
    "InvalidResponseDataError",
    "JSONParseError",
    "LoadAPIKeyError",
    "LoadSettingError",
    "NoContentGeneratedError",
    "NoSuchModelError",
    "TooManyEmbeddingValuesForCallError",
    "TypeValidationContext",
    "TypeValidationError",
    "UnsupportedFunctionalityError",
    "get_error_message",
    # image_model
    "ImageModelV2",
    "ImageModelV2CallOptions",
    "ImageModelV2CallWarning",
    "ImageModelV2ProviderMetadata",
    "ImageModelV3",
    "ImageModelV3CallOptions",
    "ImageModelV3File",
    "ImageModelV3ProviderMetadata",
    "ImageModelV3Usage",
    # image_model_middleware
    "ImageModelV3Middleware",
    # json_value
    "JSONArray",
    "JSONObject",
    "JSONValue",
    "is_json_array",
    "is_json_object",
    "is_json_value",
    # language_model_middleware
    "LanguageModelV2Middleware",
    "LanguageModelV3Middleware",
    # embedding_model_middleware
    "EmbeddingModelV3Middleware",
    # language_model (re-exported via wildcard)
    # provider
    "ProviderV2",
    "ProviderV3",
    # reranking_model
    "RerankingModelV3",
    "RerankingModelV3CallOptions",
    # shared
    "CompatibilityWarning",
    "OtherWarning",
    "SharedV2Headers",
    "SharedV2ProviderMetadata",
    "SharedV2ProviderOptions",
    "SharedV3Headers",
    "SharedV3ProviderMetadata",
    "SharedV3ProviderOptions",
    "SharedV3Warning",
    "UnsupportedWarning",
    # speech_model
    "SpeechModelV2",
    "SpeechModelV2CallOptions",
    "SpeechModelV2CallWarning",
    "SpeechModelV3",
    "SpeechModelV3CallOptions",
    # transcription_model
    "TranscriptionModelV2",
    "TranscriptionModelV2CallOptions",
    "TranscriptionModelV2CallWarning",
    "TranscriptionModelV3",
    "TranscriptionModelV3CallOptions",
    # video_model
    "Experimental_VideoModelV3",
    "Experimental_VideoModelV3CallOptions",
    "Experimental_VideoModelV3File",
    "Experimental_VideoModelV3VideoData",
    # json-schema types
    "JSONSchema7",
    "JSONSchema7Definition",
]

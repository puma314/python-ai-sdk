"""
Auto-translated Python mirror for `src/error/index.ts`.
"""

from __future__ import annotations

from typing import Any, TypeAlias

AISDKError: Any = None
APICallError: Any = None
EmptyResponseBodyError: Any = None
InvalidPromptError: Any = None
InvalidResponseDataError: Any = None
JSONParseError: Any = None
LoadAPIKeyError: Any = None
LoadSettingError: Any = None
NoContentGeneratedError: Any = None
NoSuchModelError: Any = None
TooManyEmbeddingValuesForCallError: Any = None
TypeValidationError: Any = None
UnsupportedFunctionalityError: Any = None

try:
  from .invalid_argument_error import InvalidArgumentError
except Exception:
  InvalidArgumentError: Any = None

try:
  from .invalid_stream_part_error import InvalidStreamPartError
except Exception:
  InvalidStreamPartError: Any = None

try:
  from .invalid_tool_approval_error import InvalidToolApprovalError
except Exception:
  InvalidToolApprovalError: Any = None

try:
  from .invalid_tool_input_error import InvalidToolInputError
except Exception:
  InvalidToolInputError: Any = None

try:
  from .tool_call_not_found_for_approval_error import ToolCallNotFoundForApprovalError
except Exception:
  ToolCallNotFoundForApprovalError: Any = None

try:
  from .missing_tool_result_error import MissingToolResultsError
except Exception:
  MissingToolResultsError: Any = None

try:
  from .no_image_generated_error import NoImageGeneratedError
except Exception:
  NoImageGeneratedError: Any = None

try:
  from .no_object_generated_error import NoObjectGeneratedError
except Exception:
  NoObjectGeneratedError: Any = None

try:
  from .no_output_generated_error import NoOutputGeneratedError
except Exception:
  NoOutputGeneratedError: Any = None

try:
  from .no_speech_generated_error import NoSpeechGeneratedError
except Exception:
  NoSpeechGeneratedError: Any = None

try:
  from .no_transcript_generated_error import NoTranscriptGeneratedError
except Exception:
  NoTranscriptGeneratedError: Any = None

try:
  from .no_video_generated_error import NoVideoGeneratedError
except Exception:
  NoVideoGeneratedError: Any = None

try:
  from .no_such_tool_error import NoSuchToolError
except Exception:
  NoSuchToolError: Any = None

try:
  from .tool_call_repair_error import ToolCallRepairError
except Exception:
  ToolCallRepairError: Any = None

try:
  from .unsupported_model_version_error import UnsupportedModelVersionError
except Exception:
  UnsupportedModelVersionError: Any = None

try:
  from .ui_message_stream_error import UIMessageStreamError
except Exception:
  UIMessageStreamError: Any = None

try:
  from ..prompt.invalid_data_content_error import InvalidDataContentError
except Exception:
  InvalidDataContentError: Any = None

try:
  from ..prompt.invalid_message_role_error import InvalidMessageRoleError
except Exception:
  InvalidMessageRoleError: Any = None

try:
  from ..prompt.message_conversion_error import MessageConversionError
except Exception:
  MessageConversionError: Any = None

DownloadError: Any = None

try:
  from ..util.retry_error import RetryError
except Exception:
  RetryError: Any = None


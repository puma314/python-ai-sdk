"""Open Responses API parameter and response type aliases.

This file mirrors the large TypeScript type declaration surface in a compact
Python TypedDict form for core fields currently consumed by the translated code.
"""

from __future__ import annotations

from typing import Literal, NotRequired, TypeAlias, TypedDict


class OpenResponsesError(TypedDict):
  message: str
  type: str
  param: str
  code: str


class OpenResponsesErrorBody(TypedDict):
  error: OpenResponsesError


FunctionCallStatus: TypeAlias = Literal['in_progress', 'completed', 'incomplete']
ToolChoiceValueEnum: TypeAlias = Literal['none', 'auto', 'required']
VerbosityEnum: TypeAlias = Literal['low', 'medium', 'high']
ReasoningEffortEnum: TypeAlias = Literal['none', 'low', 'medium', 'high', 'xhigh']
ReasoningSummaryEnum: TypeAlias = Literal['concise', 'detailed', 'auto']


class InputTextContentParam(TypedDict):
  type: Literal['input_text']
  text: str


class InputImageContentParam(TypedDict, total=False):
  type: Literal['input_image']
  image_url: str
  detail: Literal['low', 'high', 'auto']


class InputFileContentParam(TypedDict, total=False):
  type: Literal['input_file']
  filename: str
  file_data: str
  file_url: str


class OutputTextContentParam(TypedDict):
  type: Literal['output_text']
  text: str


class RefusalContentParam(TypedDict):
  type: Literal['refusal']
  refusal: str


class FunctionCallItemParam(TypedDict, total=False):
  id: str
  call_id: str
  type: Literal['function_call']
  name: str
  arguments: str
  status: FunctionCallStatus


class FunctionCallOutputItemParam(TypedDict, total=False):
  id: str
  call_id: str
  type: Literal['function_call_output']
  output: (
    str | list[InputTextContentParam | InputImageContentParam | InputFileContentParam]
  )
  status: FunctionCallStatus


class FunctionToolParam(TypedDict, total=False):
  name: str
  description: str
  parameters: dict[str, object]
  strict: bool
  type: Literal['function']


class SpecificFunctionParam(TypedDict):
  type: Literal['function']
  name: str


class AllowedToolsParam(TypedDict, total=False):
  type: Literal['allowed_tools']
  tools: list[SpecificFunctionParam]
  mode: ToolChoiceValueEnum


ToolChoiceParam: TypeAlias = ToolChoiceValueEnum | SpecificFunctionParam | AllowedToolsParam


class OpenResponsesRequestBody(TypedDict, total=False):
  """Body sent to the Open Responses API."""

  model: str
  input: str | list[dict[str, object]]
  instructions: str
  tools: list[FunctionToolParam]
  tool_choice: ToolChoiceParam
  text: dict[str, object]
  max_output_tokens: int
  temperature: float
  top_p: float
  presence_penalty: float
  frequency_penalty: float
  stream: bool


class UsageDetails(TypedDict, total=False):
  cached_tokens: int
  reasoning_tokens: int


class Usage(TypedDict, total=False):
  input_tokens: int
  output_tokens: int
  total_tokens: int
  input_tokens_details: UsageDetails
  output_tokens_details: UsageDetails


class OutputItem(TypedDict, total=False):
  type: str
  id: str
  call_id: str
  name: str
  arguments: str
  content: list[dict[str, object]]


class OpenResponsesResponseBody(TypedDict, total=False):
  id: str
  object: Literal['response']
  created_at: int
  model: str
  status: str
  output: list[OutputItem]
  incomplete_details: dict[str, str]
  usage: Usage
  error: dict[str, str]


class OpenResponsesChunk(TypedDict, total=False):
  type: str
  sequence_number: int
  response: OpenResponsesResponseBody
  item: OutputItem
  item_id: str
  delta: str

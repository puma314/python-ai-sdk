from __future__ import annotations

"""Language model v3 call options.

Translated from: packages/provider/src/language-model/v3/language-model-v3-call-options.ts
"""

import asyncio
from dataclasses import dataclass
from typing import Any, Literal, Union

from ...shared.v3.shared_v3_provider_options import SharedV3ProviderOptions
from .language_model_v3_function_tool import LanguageModelV3FunctionTool
from .language_model_v3_prompt import LanguageModelV3Prompt
from .language_model_v3_provider_tool import LanguageModelV3ProviderTool
from .language_model_v3_tool_choice import LanguageModelV3ToolChoice


@dataclass(frozen=True)
class ResponseFormatText:
    """Text response format."""

    type: Literal['text'] = 'text'


@dataclass(frozen=True)
class ResponseFormatJson:
    """JSON response format."""

    type: Literal['json'] = 'json'

    schema: dict[str, Any] | None = None
    """JSON schema that the generated output should conform to."""

    name: str | None = None
    """Name of output that should be generated. Used by some providers for additional LLM guidance."""

    description: str | None = None
    """Description of the output that should be generated. Used by some providers for additional LLM guidance."""


ResponseFormat = Union[ResponseFormatText, ResponseFormatJson]


@dataclass(frozen=True)
class LanguageModelV3CallOptions:
    """Options for language model v3 calls."""

    prompt: LanguageModelV3Prompt
    """A language mode prompt is a standardized prompt type.

    Note: This is **not** the user-facing prompt. The AI SDK methods will map the
    user-facing prompt types such as chat or instruction prompts to this format.
    That approach allows us to evolve the user facing prompts without breaking
    the language model interface.
    """

    max_output_tokens: int | None = None
    """Maximum number of tokens to generate."""

    temperature: float | None = None
    """Temperature setting. The range depends on the provider and model."""

    stop_sequences: list[str] | None = None
    """Stop sequences.
    If set, the model will stop generating text when one of the stop sequences is generated.
    Providers may have limits on the number of stop sequences.
    """

    top_p: float | None = None
    """Nucleus sampling."""

    top_k: int | None = None
    """Only sample from the top K options for each subsequent token.

    Used to remove "long tail" low probability responses.
    Recommended for advanced use cases only. You usually only need to use temperature.
    """

    presence_penalty: float | None = None
    """Presence penalty setting. It affects the likelihood of the model to
    repeat information that is already in the prompt.
    """

    frequency_penalty: float | None = None
    """Frequency penalty setting. It affects the likelihood of the model
    to repeatedly use the same words or phrases.
    """

    response_format: ResponseFormat | None = None
    """Response format. The output can either be text or JSON. Default is text.

    If JSON is selected, a schema can optionally be provided to guide the LLM.
    """

    seed: int | None = None
    """The seed (integer) to use for random sampling. If set and supported
    by the model, calls will generate deterministic results.
    """

    tools: list[LanguageModelV3FunctionTool | LanguageModelV3ProviderTool] | None = None
    """The tools that are available for the model."""

    tool_choice: LanguageModelV3ToolChoice | None = None
    """Specifies how the tool should be selected. Defaults to 'auto'."""

    include_raw_chunks: bool | None = None
    """Include raw chunks in the stream. Only applicable for streaming calls."""

    abort_signal: asyncio.Event | None = None
    """Abort signal for cancelling the operation."""

    headers: dict[str, str | None] | None = None
    """Additional HTTP headers to be sent with the request.
    Only applicable for HTTP-based providers.
    """

    provider_options: SharedV3ProviderOptions | None = None
    """Additional provider-specific options. They are passed through
    to the provider from the AI SDK and enable provider-specific
    functionality that can be fully encapsulated in the provider.
    """

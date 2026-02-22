from __future__ import annotations

"""Language model v2 call options.

Translated from: packages/provider/src/language-model/v2/language-model-v2-call-options.ts
"""

from dataclasses import dataclass
from typing import Any, Literal, Union

from .language_model_v2_function_tool import (
    LanguageModelV2FunctionTool,
)
from .language_model_v2_prompt import (
    LanguageModelV2Prompt,
)
from .language_model_v2_provider_defined_tool import (
    LanguageModelV2ProviderDefinedTool,
)
from .language_model_v2_tool_choice import (
    LanguageModelV2ToolChoice,
)
from ...shared.v2.shared_v2_provider_options import (
    SharedV2ProviderOptions,
)


@dataclass(frozen=True)
class TextResponseFormat:
    """Text response format."""

    type: Literal['text'] = 'text'


@dataclass(frozen=True)
class JSONResponseFormat:
    """JSON response format."""

    type: Literal['json'] = 'json'

    schema: dict[str, Any] | None = None
    """JSON schema that the generated output should conform to."""

    name: str | None = None
    """Name of output that should be generated. Used by some providers for additional LLM guidance."""

    description: str | None = None
    """Description of the output that should be generated. Used by some providers for additional LLM guidance."""


LanguageModelV2ResponseFormat = Union[TextResponseFormat, JSONResponseFormat]


@dataclass(frozen=True)
class LanguageModelV2CallOptions:
    """Options for calling a language model v2."""

    prompt: LanguageModelV2Prompt
    """A language model prompt is a standardized prompt type.

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

    response_format: LanguageModelV2ResponseFormat | None = None
    """Response format. The output can either be text or JSON. Default is text.

    If JSON is selected, a schema can optionally be provided to guide the LLM.
    """

    seed: int | None = None
    """The seed (integer) to use for random sampling. If set and supported
    by the model, calls will generate deterministic results.
    """

    tools: list[LanguageModelV2FunctionTool | LanguageModelV2ProviderDefinedTool] | None = None
    """The tools that are available for the model."""

    tool_choice: LanguageModelV2ToolChoice | None = None
    """Specifies how the tool should be selected. Defaults to 'auto'."""

    include_raw_chunks: bool | None = None
    """Include raw chunks in the stream. Only applicable for streaming calls."""

    abort_signal: object | None = None
    """Abort signal for cancelling the operation.

    In Python, use an asyncio.Event for cooperative cancellation.
    """

    headers: dict[str, str | None] | None = None
    """Additional HTTP headers to be sent with the request.
    Only applicable for HTTP-based providers.
    """

    provider_options: SharedV2ProviderOptions | None = None
    """Additional provider-specific options. They are passed through
    to the provider from the AI SDK and enable provider-specific
    functionality that can be fully encapsulated in the provider.
    """

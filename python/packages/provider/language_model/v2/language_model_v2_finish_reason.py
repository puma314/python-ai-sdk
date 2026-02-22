from __future__ import annotations

"""Reason why a language model finished generating a response.

Can be one of the following:
- ``stop``: model generated stop sequence
- ``length``: model generated maximum number of tokens
- ``content-filter``: content filter violation stopped the model
- ``tool-calls``: model triggered tool calls
- ``error``: model stopped because of an error
- ``other``: model stopped for other reasons
- ``unknown``: the model has not transmitted a finish reason

Translated from: packages/provider/src/language-model/v2/language-model-v2-finish-reason.ts
"""

from typing import Literal

LanguageModelV2FinishReason = Literal[
    'stop',            # model generated stop sequence
    'length',          # model generated maximum number of tokens
    'content-filter',  # content filter violation stopped the model
    'tool-calls',      # model triggered tool calls
    'error',           # model stopped because of an error
    'other',           # model stopped for other reasons
    'unknown',         # the model has not transmitted a finish reason
]

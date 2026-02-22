"""Translated from: packages/provider/src/errors/get-error-message.ts"""

from __future__ import annotations

import json
from typing import Any


def get_error_message(error: Any | None) -> str:
    if error is None:
        return "unknown error"

    if isinstance(error, str):
        return error

    if isinstance(error, Exception):
        return str(error)

    return json.dumps(error)

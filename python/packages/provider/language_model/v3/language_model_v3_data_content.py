from __future__ import annotations

"""Data content type for language model v3.

Translated from: packages/provider/src/language-model/v3/language-model-v3-data-content.ts
"""

# Data content. Can be bytes, base64 encoded data as a string, or a URL.
#
# In TypeScript this is `Uint8Array | string | URL`. In Python, URL is
# represented as a plain string, so `bytes | str` covers all three cases.
LanguageModelV3DataContent = bytes | str

from typing import TypeAlias

# TypeScript allows Uint8Array | string | URL.
# In Python this maps to bytes (binary) or string (base64/URL).
LanguageModelV3DataContent: TypeAlias = bytes | str

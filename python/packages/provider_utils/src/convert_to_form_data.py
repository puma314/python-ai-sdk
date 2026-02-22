"""
Auto-translated Python mirror for `src/convert-to-form-data.ts`.

Converts an input object to FormData for multipart/form-data requests.
Handles the following cases:
- `null` or `undefined` values are skipped
- Arrays with a single element are appended as a single value
- Arrays with multiple elements are appended with `[]` suffix (e.g., `image[]`)
unless `useArrayBrackets` is set to `false`
- All other values are appended directly
@param input - The input object to convert. Use a generic type for type validation.
@param options - Optional configuration object.
@param options.useArrayBrackets - Whether to add `[]` suffix for multi-element arrays.
Defaults to `true`. Set to `false` for APIs that expect repeated keys without brackets.
@returns A FormData object containing the input values.
@example
```ts
type MyInput = {
model: string;
prompt: string;
images: Blob[];
};
const formData = convertToFormData<MyInput>({
"""

from __future__ import annotations

from typing import Any, TypeAlias


def convertToFormData(*args: Any, **kwargs: Any) -> Any:
  """Auto-translated function placeholder."""
  return None

__all__ = ['convertToFormData']

# TypeScript → Python Translation Rules

This document defines the canonical rules for translating TypeScript source files from the Vercel AI SDK into idiomatic Python. Every translation agent MUST follow these rules. When a rule is ambiguous or a case is not covered, log it to the shared scratchpad at `translation/state/scaffolding-stream.md` with a `[NEEDS HUMAN]` prefix.

---

## 1. File & Module Structure

### File Naming
- **kebab-case → snake_case**: `language-model-v3.ts` → `language_model_v3.py`
- **Test files**: `foo.test.ts` → `test_foo.py` (pytest convention)
- **Type test files**: `*.test-d.ts` → **skip** (no Python equivalent)
- **React files**: `*.tsx` → **skip** (no Python equivalent)
- **Existing underscores**: preserve as-is (e.g. `computer_20251124.ts` → `computer_20251124.py`)

### Directory Mapping
- Strip `src/` from the path: `packages/provider/src/errors/` → `python/packages/provider/errors/`
- Convert directory names: kebab-case → snake_case
- Preserve versioned directories: `v2/`, `v3/` stay as-is

### Barrel Exports (`index.ts` → `__init__.py`)
- Pure re-export barrel: convert to `__init__.py` with Python imports
  ```typescript
  // index.ts
  export { AISDKError } from './ai-sdk-error';
  export type { LanguageModelV3 } from './language-model-v3';
  ```
  ```python
  # __init__.py
  from .ai_sdk_error import AISDKError
  from .language_model_v3 import LanguageModelV3
  ```
- Type-only exports (`export type { ... }`): re-export normally in Python (there is no type-only import distinction). Use `TYPE_CHECKING` guard only when the import would cause a circular dependency at runtime.
- `export *` from: use `from .module import *` but prefer explicit re-exports when the exported names are known.
- If `index.ts` contains logic beyond re-exports, split into `__init__.py` (public API) plus a separate module for the logic.

---

## 2. Type System

### Primitive Types

| TypeScript | Python |
|------------|--------|
| `string` | `str` |
| `number` | `int \| float` (use `float` where fractional values are expected, `int` where only integers apply) |
| `boolean` | `bool` |
| `null` | `None` |
| `undefined` | `None` (see below for nuances) |
| `unknown` | `Any` |
| `void` | `None` |
| `never` | `NoReturn` (from `typing`) |
| `bigint` | `int` |

### `undefined` vs `None` Semantics

TypeScript distinguishes absent (`undefined`) from explicitly null (`null`). Python only has `None`. Rules:

- **Optional parameter** `foo?: string` → `foo: str | None = None`
- **Optional property in interface/type** → `foo: str | None = None` on dataclass/BaseModel
- **TypedDict optional key** (key may be absent) → `foo: NotRequired[str]` (from `typing`)
- **`string | null`** → `str | None`
- **`string | undefined`** → `str | None`
- **`string | null | undefined`** → `str | None`
- When a TS function checks `if (x !== undefined)` vs `if (x !== null)`, collapse both to `if x is not None` in Python. Log a `[NOTE]` if the distinction matters for logic.

### `readonly`

- **On a dataclass**: use `@dataclass(frozen=True)` when ALL fields are readonly
- **Individual readonly field** on a mutable class: use `Final[T]` annotation
- **In a Protocol**: use `@property` for read-only attributes
- **`Readonly<T>`** utility type: use `frozen=True` dataclass
- **`ReadonlyArray<T>`**: use `Sequence[T]` (immutable view) instead of `list[T]`

### Template Literal Types

TypeScript can enforce string patterns at compile time:
```typescript
id: `${string}.${string}`  // e.g. "openai.gpt-4"
```

Python typing **cannot** enforce this statically. Translation:
- Use `str` as the type annotation
- Add a **runtime validator** function:
  ```python
  def validate_provider_tool_id(id: str) -> str:
      """Validate that id matches the pattern 'provider.tool_name'."""
      if '.' not in id or id.startswith('.') or id.endswith('.'):
          raise ValueError(f"Invalid provider tool id format: {id!r}. Expected 'provider.tool_name'.")
      return id
  ```
- Call the validator at construction time (in `__init__` or Pydantic `model_validator`)
- Document the expected format in the docstring

### Literal Types and Enums
- `type Foo = 'a' | 'b' | 'c'` → `Foo = Literal['a', 'b', 'c']`
- TypeScript `enum` → Python `enum.Enum` or `StrEnum`:
  ```python
  class MyEnum(StrEnum):
      VALUE_A = 'a'
      VALUE_B = 'b'
  ```

### Discriminated Unions

The SDK heavily uses `type` field discriminators. Translate as frozen dataclasses with `Literal` type field:

```typescript
type StreamPart =
  | { type: 'text-delta'; delta: string }
  | { type: 'tool-call'; toolName: string; input: unknown };
```
```python
from dataclasses import dataclass
from typing import Any, Literal, Union

@dataclass(frozen=True)
class TextDelta:
    type: Literal['text-delta'] = 'text-delta'
    delta: str = ''

@dataclass(frozen=True)
class ToolCall:
    type: Literal['tool-call'] = 'tool-call'
    tool_name: str = ''
    input: Any = None

StreamPart = Union[TextDelta, ToolCall]
```

For Pydantic models needing runtime discrimination:
```python
from pydantic import BaseModel, Field
from typing import Annotated, Union

StreamPart = Annotated[Union[TextDelta, ToolCall], Field(discriminator='type')]
```

### Intersection Types (`A & B`)
- Python has no intersection types. Use **multiple inheritance**:
  ```python
  class Combined(A, B): ...
  ```
- Or flatten into a single class with all fields from both types.

### Conditional Types (`T extends U ? X : Y`)
- Cannot be directly translated. Use `@overload` for function signatures:
  ```python
  @overload
  async def parse_json(*, text: str) -> JSONValue: ...
  @overload
  async def parse_json(*, text: str, schema: Schema[T]) -> T: ...
  async def parse_json(*, text: str, schema: Schema[T] | None = None) -> T | JSONValue:
      ...
  ```
- For type aliases, collapse to the most general type and document the constraint.

### `NoInfer<T>`
- No Python equivalent. Remove and use the type parameter directly.
- Document in a comment if the inference prevention was important.

### Record / Mapped Types
- `Record<string, T>` → `dict[str, T]`
- `Record<K, V>` where K is a union → `TypedDict` with explicit keys
- `Partial<T>` → make all fields optional (add `| None = None`)
- `Required<T>` → make all fields required (remove defaults)
- `Pick<T, K>` / `Omit<T, K>` → create a new type with only the relevant fields

---

## 3. Zod → Pydantic

The SDK uses Zod for runtime schema validation. Python equivalent is Pydantic.

### Schema Mapping

| Zod | Pydantic / Python |
|-----|-------------------|
| `z.object({ ... })` | `class MyModel(BaseModel): ...` |
| `z.string()` | `str` |
| `z.number()` | `float` (or `int` if `.int()`) |
| `z.boolean()` | `bool` |
| `z.literal('foo')` | `Literal['foo']` |
| `z.enum(['a', 'b'])` | `Literal['a', 'b']` |
| `z.array(z.string())` | `list[str]` |
| `z.optional()` | `T \| None = None` |
| `z.nullable()` | `T \| None` |
| `z.nullish()` | `T \| None = None` |
| `z.union([A, B])` | `Union[A, B]` |
| `z.discriminatedUnion('type', [...])` | `Annotated[Union[...], Field(discriminator='type')]` |
| `z.record(z.string())` | `dict[str, str]` |
| `z.tuple([...])` | `tuple[...]` |
| `z.lazy(() => schema)` | Forward reference + `model_rebuild()` |
| `.default(val)` | `Field(default=val)` |
| `.describe('...')` | `Field(description='...')` |
| `.refine(fn)` | `@field_validator` or `@model_validator` |
| `.transform(fn)` | `@field_validator(mode='before')` |
| `.safeParse(val)` | `MyModel.model_validate(val)` wrapped in try/except |
| `.parse(val)` | `MyModel.model_validate(val)` (raises `ValidationError`) |

### SDK Schema System

The SDK defines its own `Schema<T>` / `FlexibleSchema<T>` / `LazySchema<T>` abstraction in `packages/provider-utils/src/schema.ts`. Translate to Protocol-based equivalents:

```python
from typing import Any, Awaitable, Callable, Generic, Protocol, TypeVar, runtime_checkable

T = TypeVar('T')

@runtime_checkable
class Schema(Protocol[T]):
    """Protocol equivalent of the SDK's Schema type."""

    @property
    def json_schema(self) -> dict[str, Any] | Awaitable[dict[str, Any]]: ...

    def validate(self, value: Any) -> 'ValidationResult[T]' | Awaitable['ValidationResult[T]']: ...

# LazySchema is a callable that returns a Schema, with caching
LazySchema = Callable[[], Schema[T]]

# FlexibleSchema accepts Schema, LazySchema, or Pydantic models
FlexibleSchema = Schema[T] | LazySchema[T] | type[BaseModel]
```

The `_type: OBJECT` phantom field in TypeScript (used only for type inference, never at runtime) has no Python equivalent. Use `Generic[T]` on the Protocol instead.

The Symbol-based `schemaSymbol` marker → use `@runtime_checkable` Protocol or a `_schema_marker: ClassVar[bool] = True` attribute.

---

## 4. Error Hierarchy

### Symbol Marker Pattern → Class Attribute Pattern

TypeScript uses `Symbol.for()` for cross-package type identification:
```typescript
const marker = 'vercel.ai.error';
const symbol = Symbol.for(marker);
class AISDKError extends Error {
  private readonly [symbol] = true;
  static isInstance(error: unknown): error is AISDKError {
    return AISDKError.hasMarker(error, marker);
  }
}
```

Python translation uses class-level string markers:
```python
from typing import ClassVar

class AISDKError(Exception):
    """Base error for AI SDK."""
    _marker: ClassVar[str] = 'vercel.ai.error'

    def __init__(self, *, name: str, message: str, cause: BaseException | None = None) -> None:
        super().__init__(message)
        self.name = name
        self.__cause__ = cause

    @classmethod
    def is_instance(cls, error: object) -> bool:
        """Check if error is an instance of this error class.
        Works across package boundaries via marker checking."""
        return (
            isinstance(error, Exception)
            and hasattr(error, '_marker')
            and isinstance(getattr(error, '_marker', None), str)
            and getattr(error, '_marker', '').startswith(cls._marker)
        )

    @staticmethod
    def has_marker(error: object, marker: str) -> bool:
        return (
            isinstance(error, Exception)
            and hasattr(error, '_marker')
            and getattr(error, '_marker', None) == marker
        )
```

Each subclass sets its own marker:
```python
class APICallError(AISDKError):
    _marker: ClassVar[str] = 'vercel.ai.error.AI_APICallError'

    def __init__(self, *, message: str, url: str, status_code: int | None = None,
                 response_body: str | None = None, cause: BaseException | None = None,
                 is_retryable: bool = False, data: Any = None) -> None:
        super().__init__(name='AI_APICallError', message=message, cause=cause)
        self.url = url
        self.status_code = status_code
        self.response_body = response_body
        self.is_retryable = is_retryable
        self.data = data
```

### Error Hierarchy (preserve completely)
- `AISDKError` (base)
- `APICallError`
- `EmptyResponseBodyError`
- `InvalidArgumentError`
- `InvalidPromptError`
- `InvalidResponseDataError`
- `JSONParseError`
- `LoadAPIKeyError`
- `LoadSettingError`
- `NoContentGeneratedError`
- `NoSuchModelError`
- `TooManyEmbeddingValuesForCallError`
- `TypeValidationError`
- `UnsupportedFunctionalityError`

---

## 5. Async Patterns

### Promise / Async

| TypeScript | Python |
|------------|--------|
| `async function foo(): Promise<T>` | `async def foo() -> T:` |
| `Promise<T>` (as type) | `Coroutine[Any, Any, T]` or just use `async def` |
| `PromiseLike<T>` | `Awaitable[T]` (from `collections.abc`) |
| `MaybePromiseLike<T>` | `T \| Awaitable[T]` |
| `await promise` | `await awaitable` |
| `Promise.all([a, b])` | `asyncio.gather(a, b)` |
| `Promise.race([a, b])` | `asyncio.wait(tasks, return_when=FIRST_COMPLETED)` |

### Streams

| TypeScript | Python |
|------------|--------|
| `ReadableStream<T>` | `AsyncIterator[T]` |
| `AsyncIterable<T>` | `AsyncIterable[T]` (same concept) |
| `for await (const chunk of stream)` | `async for chunk in stream:` |
| `yield` in async generator | `yield` in async generator (same) |
| `TransformStream<I, O>` | Async generator function that takes `AsyncIterable[I]` and yields `O` |

The `convertAsyncIteratorToReadableStream` utility is NOT needed in Python — `AsyncIterator` is already the native streaming abstraction.

For SSE (Server-Sent Events) parsing, use `httpx-sse` library instead of the TS `EventSourceParserStream`.

### Cancellation

| TypeScript | Python |
|------------|--------|
| `AbortSignal` | `asyncio.Event` for cooperative cancellation |
| `AbortController` | Set `asyncio.Event` + check in loops |
| `signal.aborted` | `event.is_set()` |
| `signal.addEventListener('abort', fn)` | `asyncio.create_task` watching the event |

Alternatively, use `anyio.CancelScope` for structured concurrency. Prefer `anyio` over raw `asyncio` for cancellation when possible.

### Delayed / Deferred Values

| TypeScript | Python |
|------------|--------|
| `DelayedPromise<T>` | `asyncio.Future[T]` |
| `resolve(value)` | `future.set_result(value)` |
| `reject(error)` | `future.set_exception(error)` |

---

## 6. JSON Parsing

The SDK mandates `secureJsonParse` instead of raw `JSON.parse` to prevent prototype pollution (a JS-specific attack). In Python, `json.loads` is inherently safe against this. Still, maintain a wrapper for API parity:

```python
import json
from typing import Any

def secure_json_parse(text: str) -> Any:
    """Parse JSON safely. Python's json.loads is inherently safe against
    prototype pollution, but this wrapper maintains API parity with the TS SDK."""
    return json.loads(text)
```

For `parseJSON` and `safeParseJSON`, use `@overload`:
```python
@overload
async def parse_json(*, text: str) -> JSONValue: ...
@overload
async def parse_json(*, text: str, schema: Schema[T]) -> T: ...

def safe_parse_json(*, text: str, schema: Schema[T] | None = None) -> ParseResult[T]:
    """Returns a result object instead of raising."""
    try:
        value = json.loads(text)
        if schema is not None:
            return schema.validate(value)
        return ParseResult(success=True, value=value)
    except (json.JSONDecodeError, ValidationError) as e:
        return ParseResult(success=False, error=e)
```

---

## 7. Naming Conventions

### Properties and Methods
- **camelCase → snake_case**: `modelId` → `model_id`, `toolName` → `tool_name`, `providerMetadata` → `provider_metadata`
- **Boolean prefixes**: `isRetryable` → `is_retryable`, `hasError` → `has_error`
- **Callbacks**: `onStepFinish` → `on_step_finish`

### Classes
- **PascalCase stays PascalCase**: `AISDKError`, `LanguageModelV3`, `ToolLoopAgent`

### Constants
- **UPPER_SNAKE_CASE stays**: `DEFAULT_MAX_RETRIES`
- Module-level constants that were `const` in TS → module-level variables (UPPER_SNAKE_CASE if truly constant)

### String Literal Values
- **Preserve exactly**: `'text-delta'` stays `'text-delta'`, not `'text_delta'`
- These are protocol values, not Python identifiers

### Type Aliases
- PascalCase in both languages: `type StreamPart = ...` → `StreamPart = Union[...]`

---

## 8. Import Mapping

### Package Imports

| TypeScript | Python |
|------------|--------|
| `from '@ai-sdk/provider'` | `from ai_sdk.provider` |
| `from '@ai-sdk/provider-utils'` | `from ai_sdk.provider_utils` |
| `from 'ai'` | `from ai_sdk` |
| `from '@ai-sdk/openai'` | `from ai_sdk.openai` |
| `from '@ai-sdk/anthropic'` | `from ai_sdk.anthropic` |

General rule: `@ai-sdk/<package-name>` → `ai_sdk.<package_name>` (kebab → snake).

### Relative Imports

| TypeScript | Python |
|------------|--------|
| `from './foo'` | `from .foo import ...` |
| `from './foo/bar'` | `from .foo.bar import ...` |
| `from '../bar'` | `from ..bar import ...` |
| `from '../../baz'` | `from ...baz import ...` |

### External Dependencies

| TypeScript | Python |
|------------|--------|
| `zod` (v3 or v4) | `pydantic` |
| `json-schema` types | `dict[str, Any]` (JSON Schema is just a dict) |
| `@standard-schema/spec` | Not needed (Pydantic IS the standard) |
| `eventsource-parser` | `httpx-sse` |
| `secure-json-parse` | `json` (stdlib, already safe) |
| `nanoid` | `uuid` or `secrets.token_urlsafe` |

### Import Style
- Prefer explicit imports: `from ai_sdk.provider.errors import AISDKError`
- Avoid wildcard imports in implementation files (only in `__init__.py`)
- Use `from __future__ import annotations` at the top of every file for forward reference support

---

## 9. Testing (Vitest → pytest)

### Structure

| Vitest | pytest |
|--------|--------|
| `describe('name', () => { ... })` | `class TestName:` |
| `it('should do X', async () => { ... })` | `async def test_should_do_x(self):` |
| `it('should do X', () => { ... })` | `def test_should_do_x(self):` |
| `beforeEach(() => { ... })` | `@pytest.fixture(autouse=True)` |
| `afterEach(() => { ... })` | yield fixture with cleanup |
| `beforeAll(() => { ... })` | `@pytest.fixture(scope='class', autouse=True)` |

### Assertions

| Vitest | pytest |
|--------|--------|
| `expect(x).toBe(y)` | `assert x == y` |
| `expect(x).toEqual(y)` | `assert x == y` (deep equality by default) |
| `expect(x).toBeTruthy()` | `assert x` |
| `expect(x).toBeFalsy()` | `assert not x` |
| `expect(x).toBeNull()` | `assert x is None` |
| `expect(x).toBeUndefined()` | `assert x is None` |
| `expect(x).toContain(y)` | `assert y in x` |
| `expect(x).toHaveLength(n)` | `assert len(x) == n` |
| `expect(fn).toThrow(Error)` | `with pytest.raises(Error):` |
| `expect(fn).toThrowError('msg')` | `with pytest.raises(Error, match='msg'):` |
| `expect(x).toMatchObject(y)` | Custom helper or `assert {**x} >= {**y}` |
| `expect(x).toMatchSnapshot()` | `pytest-snapshot` or inline-snapshot |

### Mocking

| Vitest | pytest |
|--------|--------|
| `vi.fn()` | `unittest.mock.MagicMock()` |
| `vi.fn().mockReturnValue(x)` | `MagicMock(return_value=x)` |
| `vi.fn().mockResolvedValue(x)` | `AsyncMock(return_value=x)` |
| `vi.spyOn(obj, 'method')` | `mocker.patch.object(obj, 'method')` |
| `vi.mock('module')` | `mocker.patch('module')` |
| `expect(fn).toHaveBeenCalledWith(...)` | `fn.assert_called_with(...)` |
| `expect(fn).toHaveBeenCalledTimes(n)` | `assert fn.call_count == n` |

Use `pytest-mock`'s `mocker` fixture for cleaner mock syntax.

### Async Tests
```python
# pytest-asyncio with auto mode (configured in pyproject.toml)
async def test_stream_text():
    result = await generate_text(model=mock_model, prompt="hello")
    assert result.text == "world"
```

---

## 10. Build & Package Tooling

| TypeScript | Python |
|------------|--------|
| `pnpm` / `npm` | `uv` |
| `package.json` | `pyproject.toml` |
| `tsconfig.json` | N/A |
| `tsup.config.ts` | N/A (pure Python) |
| `vitest` | `pytest` |
| `prettier` | `ruff format` |
| `eslint` | `ruff check` |
| `turbo.json` | Makefile or `just` task runner |
| `pnpm build` | N/A (Python doesn't need compilation) |
| `pnpm test` | `uv run pytest` |
| `pnpm lint` | `uv run ruff check` |
| `pnpm type-check` | `uv run pyright` |

---

## 11. Interfaces & Protocols

TypeScript `interface` maps to Python `Protocol` (for structural typing) or `ABC` (for nominal typing):

- **Behavioral contracts** (like `LanguageModelV3`): use `Protocol`
  ```python
  from typing import Protocol

  class LanguageModelV3(Protocol):
      @property
      def specification_version(self) -> Literal['v3']: ...
      @property
      def provider(self) -> str: ...
      @property
      def model_id(self) -> str: ...

      async def do_generate(self, options: CallOptions) -> GenerateResult: ...
      async def do_stream(self, options: CallOptions) -> StreamResult: ...
  ```

- **Data shapes** (like option bags, result types): use `@dataclass(frozen=True)` or `TypedDict`
  ```python
  @dataclass(frozen=True)
  class GenerateResult:
      text: str | None = None
      tool_calls: list[ToolCall] = field(default_factory=list)
      finish_reason: FinishReason = 'unknown'
      usage: Usage = field(default_factory=Usage)
  ```

- **Abstract base classes** (when you need `isinstance` checks): use `ABC`
  ```python
  from abc import ABC, abstractmethod

  class BaseProvider(ABC):
      @abstractmethod
      def language_model(self, model_id: str) -> LanguageModelV3: ...
  ```

Rule of thumb: if the TS code uses `implements`, use `ABC`. If it just uses the type for duck typing, use `Protocol`.

---

## 12. Generics

```typescript
class Foo<T extends Bar> { ... }
```
```python
T = TypeVar('T', bound=Bar)

class Foo(Generic[T]): ...
```

For constrained generics:
```typescript
function foo<T extends string | number>(x: T): T { ... }
```
```python
T = TypeVar('T', str, int)  # constrained TypeVar

def foo(x: T) -> T: ...
```

---

## 13. Utility Patterns

### ID Generation
- `nanoid()` / `generateId()` → `secrets.token_urlsafe(16)` or `uuid.uuid4().hex[:16]`

### API Key Loading
- `loadApiKey({ apiKey, environmentVariableName })` → equivalent Python function using `os.environ.get()`

### HTTP Requests
- `fetch()` / `postJsonToApi()` → `httpx.AsyncClient` with proper headers
- Response handling: `createJsonResponseHandler` → parse `httpx.Response` with Pydantic

### Event Source / SSE
- `EventSourceParserStream` → `httpx_sse.aconnect_sse()` or manual SSE parsing over `httpx` async streams

### Retry Logic
- `withRetries()` → `tenacity` library or manual retry loop with exponential backoff

---

## 14. Comment & Documentation Translation

All comments and documentation from the TypeScript source MUST be translated into idiomatic Python forms. Never silently drop comments.

### JSDoc / TSDoc → Python Docstrings

JSDoc block comments (`/** ... */`) on classes, methods, and functions become Python docstrings using **Google-style** format:

```typescript
/**
 * Load an API key from an explicit argument or environment variable.
 *
 * @param apiKey - Explicit API key. Takes precedence over environment variable.
 * @param environmentVariableName - Name of the environment variable to check.
 * @returns The resolved API key string.
 * @throws {LoadAPIKeyError} If no API key is found in either source.
 */
```
```python
def load_api_key(*, api_key: str | None, environment_variable_name: str) -> str:
    """Load an API key from an explicit argument or environment variable.

    Args:
        api_key: Explicit API key. Takes precedence over environment variable.
        environment_variable_name: Name of the environment variable to check.

    Returns:
        The resolved API key string.

    Raises:
        LoadAPIKeyError: If no API key is found in either source.
    """
```

### Tag Mapping

| JSDoc/TSDoc Tag | Python Docstring |
|-----------------|-----------------|
| `@param name desc` | Entry under `Args:` section |
| `@param {type} name desc` | Entry under `Args:` (drop `{type}`, Python has annotations) |
| `@returns` / `@return` | `Returns:` section |
| `@throws` / `@throws {ErrorType}` | `Raises:` section with error class name |
| `@example` | `Example:` section with indented code block |
| `@see OtherClass` | Inline reference: `See :class:\`OtherClass\`` or plain text |
| `@deprecated` | `.. deprecated::` note in docstring + `warnings.warn()` in body |
| `@internal` / `@private` | Note: `Note: Internal API, may change without notice.` + `_` prefix on name |
| `@default value` | Mention in `Args:` description: `Defaults to value.` |
| `@since version` | Note in docstring body: `Added in version X.` |

### Inline Comments
- `// comment` → `# comment`
- Translate content naturally — fix JS-specific references:
  - `// used in isInstance` → `# used in is_instance`
  - `// default to no references` → `# default to no references`
- References to TS/JS concepts should be reworded for Python context where it makes sense.

### Block Comments
- Non-JSDoc block comments (`/* ... */`) → multi-line `#` comments:
  ```python
  # This is a multi-line comment
  # that spans several lines.
  ```
- Do NOT use triple-quoted strings for non-docstring comments.

### Module-Level Documentation
- File-level JSDoc or leading `/* ... */` at the top of a `.ts` file → module docstring:
  ```python
  from __future__ import annotations
  """Module for handling API call errors.

  Translated from: packages/provider/src/errors/api-call-error.ts
  """
  ```

### Rules
- Every comment in the source MUST have a corresponding comment or docstring in the output
- Do NOT leave JSDoc syntax (`@param`, `@returns`, `{type}`) in Python code
- Do NOT use Sphinx-style `#:` field lists — use Google-style docstrings
- Do NOT add comments that weren't in the source (except the module-level `Translated from:` reference)

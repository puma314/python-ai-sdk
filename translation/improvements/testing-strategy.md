# Testing Strategy for a Zero-Maintenance Python SDK

## Philosophy

The Python SDK is auto-generated. No human maintains it. This means:

1. **Tests must also be auto-generated** from the TypeScript tests
2. **Validation must be fully automated** — no human judgment calls
3. **Failures must be self-healing** — the system should attempt fixes before flagging

The TS repo has 380 test files. These are the ground truth. The Python tests should be derived from them and should pass for the same reasons the TS tests pass.

## Three Layers of Validation

### Layer 1: Static Analysis (Zero Cost, Always Runs)

These run on every sync and every translation:

```bash
# Type checking
uv run pyright python/packages/

# Lint + format
uv run ruff check python/packages/
uv run ruff format --check python/packages/

# Import resolution
PYTHONPATH=python uv run python -c "
from ai_sdk.provider import *
from ai_sdk.provider_utils import *
from ai_sdk.ai import *
# ... all packages
"
```

These catch:
- Missing imports, broken re-exports
- Type errors from TS→Python mismatches
- Unused imports, naming violations
- Circular import issues

### Layer 2: Translated Unit Tests (Medium Cost, Runs on Sync)

#### Translating Tests

The TS test suite IS the spec. Translate `.test.ts` files alongside source files using a dedicated test translation agent.

Test files are currently excluded by the orchestrator:
```python
EXCLUDE_PATTERNS = [
    re.compile(r"\.test\.ts$"),   # <-- currently skipped
    ...
]
```

Add a separate phase that translates tests after the source:

```
Phase 1: Scaffold
Phase 2: Translate source files
Phase 3: Package check (pyright, imports)
Phase 4: Translate test files          ← NEW
Phase 5: Run tests, fix failures       ← NEW
Phase 6: Final validation              ← NEW
```

#### Test Agent Prompt

Test translation needs different rules than source translation:

```markdown
# Test Translation Agent

Translate the TypeScript test file to Python using pytest.

## Key Differences from Source Translation

- Use `pytest` assertions, not `unittest`
- Use `pytest.fixture` for setup/teardown
- Use `pytest.raises` for exception testing
- Use `unittest.mock.MagicMock` / `AsyncMock` for mocks
- Test class names: `describe('Foo', ...)` → `class TestFoo:`
- Test names: `it('should do X', ...)` → `def test_should_do_x(self):`
- Async tests: just use `async def test_...` (pytest-asyncio auto mode)
- Fixtures: import from conftest or create inline

## Important

- The test MUST import from the translated Python module, not fabricated paths
- Mock objects must match the Python API (snake_case methods), not the TS API
- If the test uses a __fixtures__/ JSON file, it should already exist (copied by scaffold)
```

#### Handling Test Failures Automatically

After translating tests, run them. If tests fail:

1. **Parse the pytest output** to identify which tests failed and why
2. **Classify the failure**:
   - Import error → the source translation has a bug (re-run checker on the source file)
   - Assertion error → the test expectation is wrong OR the source translation has a logic bug
   - Attribute error → naming mismatch between test and source (fixable by the test fix agent)
3. **Run a fix agent** with the pytest traceback as feedback
4. **Retry up to 3 times**, then flag as unresolved

```python
async def run_test_fix_loop(test_file: str, max_attempts: int = 3) -> bool:
    for attempt in range(max_attempts):
        result = run_pytest(test_file)
        if result.passed:
            return True

        # Feed failures back to fix agent
        await run_test_fix_agent(
            test_file=test_file,
            pytest_output=result.output,
            attempt=attempt + 1,
        )

    return False  # unfixable after max_attempts
```

### Layer 3: Behavioral Conformance Tests (Higher Cost, Runs Periodically)

These verify the Python SDK behaves identically to the TS SDK at the API level.

#### Approach: Shared Fixture Testing

The TS test suite uses `__fixtures__/` directories with JSON API responses. These fixtures are language-agnostic. Write a conformance test that:

1. Takes a fixture (e.g., `openai-text-response.json`)
2. Feeds it to the Python SDK's response parser
3. Verifies the parsed output matches expected structure

This can be generated once and doesn't change with every sync (fixtures are stable).

#### Approach: Golden Output Testing

For critical functions, generate "golden" expected outputs from the TS side and verify the Python side produces the same result:

```python
# Generated from TS: generateText with mock model returns this structure
GOLDEN_GENERATE_TEXT = {
    "text": "Hello world",
    "finish_reason": "stop",
    "usage": {"prompt_tokens": 10, "completion_tokens": 5},
}

async def test_generate_text_golden():
    result = await generate_text(model=mock_model, prompt="test")
    assert result.text == GOLDEN_GENERATE_TEXT["text"]
    assert result.finish_reason == GOLDEN_GENERATE_TEXT["finish_reason"]
```

## Test Runner Configuration

### `pyproject.toml` Updates

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["python/packages"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
markers = [
    "unit: Unit tests (fast, no external calls)",
    "conformance: Cross-language conformance tests",
    "slow: Tests that take >5s",
]

[tool.coverage.run]
source = ["python/packages"]
omit = ["*/test_*", "*/__pycache__/*"]
```

### Running Tests

```bash
# All unit tests
uv run pytest python/packages/ -m unit

# Just one package
uv run pytest python/packages/provider/ -m unit

# Conformance tests
uv run pytest python/packages/ -m conformance

# With coverage
uv run pytest python/packages/ --cov --cov-report=term-missing
```

## Test Translation Schedule

Tests are translated AFTER the source files for each package:

| Phase | What | When |
|-------|------|------|
| Source translation | All `.ts` files | Initial batch |
| Source validation | pyright + import check | After source translation |
| Test translation | All `.test.ts` files | After source validation passes |
| Test execution | Run translated tests | After test translation |
| Fix loop | Auto-fix failing tests | After first test run |
| Coverage check | Verify coverage thresholds | After tests pass |

## Coverage Expectations

Realistic targets for auto-generated tests:

| Package | TS Test Count | Expected Python Pass Rate | Notes |
|---------|-------------|--------------------------|-------|
| provider | 0 tests | N/A | Provider has no tests (it's all types) |
| provider-utils | ~80 tests | 85%+ | Complex schema tests may need manual help |
| ai | ~200 tests | 70%+ | Streaming tests are hard to translate |
| providers (each) | ~30-50 tests | 80%+ | Fixture-based, translates well |

The pass rate improves over time as the test fix agent learns from failures and the translation rules get refined.

## Metrics to Track (in SQLite DB)

```sql
CREATE TABLE test_runs (
    id              INTEGER PRIMARY KEY,
    package_id      INTEGER REFERENCES packages(id),
    sync_run_id     INTEGER,            -- which sync triggered this
    total_tests     INTEGER,
    passed          INTEGER,
    failed          INTEGER,
    errors          INTEGER,
    skipped         INTEGER,
    coverage_pct    REAL,
    pytest_output   TEXT,               -- or path to output file
    created_at      TEXT
);
```

## What Doesn't Get Tested Automatically

Some things need manual attention (at least initially):

1. **Integration tests with real APIs** — these need API keys and cost money
2. **Streaming behavior under load** — timing-sensitive, hard to mock
3. **Cross-package integration** — importing `ai` + `openai` and making a real call

These should be a small, manually maintained test suite (`python/tests/integration/`) that runs on a schedule (weekly) rather than on every sync.

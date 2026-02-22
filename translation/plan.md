# Translation Execution Plan

## Goal

Translate 9 TypeScript packages from the Vercel AI SDK into idiomatic Python, producing a working `ai-sdk` Python library under `python/packages/`.

## Phase 0: Environment & Validation (this session)

### 0.1 Environment Setup (DONE)
- [x] Move `pyproject.toml` to repo root so `translate.py` and output code share one venv
- [x] Add `claude-agent-sdk` to root dependencies
- [x] Verify `uv run translation/translate.py` works (dry-run)
- [x] Update package-checker prompt paths for root-level execution

### 0.2 Test Run: `provider` Package
- [ ] Run full translation on `provider` (133 files, no cross-package deps)
- [ ] Verify scaffold agent creates correct directory structure
- [ ] Verify file agents produce compilable Python
- [ ] Verify checker agents catch real issues
- [ ] Verify package-checker runs pyright and import smoke test
- [ ] Review output quality manually on a sample of files
- [ ] Document any issues found and fix prompts/orchestrator as needed

### 0.3 Post-Test Adjustments
- [ ] Fix any bugs found in translate.py
- [ ] Tune agent prompts based on test results
- [ ] Adjust concurrency/retry settings if needed

## Phase 1: Foundation Packages

### 1.1 `provider` (133 files)
- Core interfaces and type definitions
- No cross-package dependencies
- Mostly type-only files (interfaces, type aliases, enums)
- Expected difficulty: LOW (types translate cleanly)

### 1.2 `provider-utils` (~90 files)
- Shared utilities: JSON parsing, HTTP helpers, schema validation, ID generation
- Depends on `provider`
- Has significant runtime logic (not just types)
- Key challenge: Zod-to-Pydantic schema conversion subsystem (~50 files)
- Expected difficulty: MEDIUM

## Phase 2: Core SDK

### 2.1 `ai` (~200+ files)
- Main SDK package with `generateText`, `streamText`, `generateObject`, etc.
- Depends on `provider` + `provider-utils`
- Complex streaming logic, tool calling, agent loops
- Has `internal/` and `test/` subpath exports
- Expected difficulty: HIGH (streaming, complex async patterns)

## Phase 3: Provider Implementations

### 3.1 `anthropic`
- Anthropic API provider
- Depends on `provider` + `provider-utils`
- HTTP API calls, SSE streaming, tool use
- Expected difficulty: MEDIUM

### 3.2 `openai`
- OpenAI API provider
- Similar structure to anthropic
- Expected difficulty: MEDIUM

### 3.3 `open-responses`
- OpenAI Responses API (newer API format)
- Depends on `provider` + `provider-utils`
- Expected difficulty: MEDIUM

### 3.4 `google`
- Google Generative AI provider
- Expected difficulty: MEDIUM

### 3.5 `google-vertex`
- Google Vertex AI provider
- Expected difficulty: MEDIUM

### 3.6 `cerebras`
- Cerebras provider (likely smaller/simpler)
- Expected difficulty: LOW

## Risk Mitigation

### Known Risks

1. **Zod-to-Pydantic conversion** (provider-utils): The ~50 Zod conversion files are complex. May need manual review.
2. **Streaming patterns** (ai core): `ReadableStream` -> `AsyncIterator` is non-trivial for complex transform streams.
3. **Agent cost**: 133+ files x opus model = significant API usage. Monitor costs during Phase 1.
4. **Circular imports**: Python is strict about these. May need extensive `TYPE_CHECKING` guards.
5. **Cross-package imports**: Later packages import from earlier ones. If provider types change during translation, downstream breaks.

### Mitigations

- **Translate in strict dependency order** -- never translate a package before its deps are stable
- **Run package-checker after each package** -- catches import/type issues early
- **Use `--resume`** -- if interrupted, don't redo work
- **Manual review after Phase 1** -- before committing to full translation, verify quality
- **Keep original TS code untouched** -- can always re-reference

## Success Criteria

Per package:
- [ ] Pyright passes with no critical errors
- [ ] `import ai_sdk.<package>` works
- [ ] All public TypeScript exports have Python equivalents
- [ ] No stub files remaining
- [ ] Google-style docstrings on all public APIs

Overall:
- [ ] All 9 packages translated
- [ ] Cross-package imports resolve
- [ ] Basic integration test: import core + provider, call a function

## Estimated Timeline

| Phase | Packages | Est. Files | Notes |
|-------|----------|-----------|-------|
| Phase 0 | provider (test) | 133 | Validates tooling |
| Phase 1 | provider + provider-utils | ~220 | Foundation |
| Phase 2 | ai | ~200 | Core SDK |
| Phase 3 | 6 providers | ~400 | Parallel-friendly |

## Post-Translation TODO

- [ ] Write integration tests
- [ ] Add proper `__init__.py` re-exports at `python/packages/ai_sdk/` level
- [ ] Create per-package `pyproject.toml` if publishing separately
- [ ] Documentation pass
- [ ] CI setup (ruff, pyright, pytest)

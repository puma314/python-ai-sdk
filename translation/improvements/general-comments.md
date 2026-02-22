# General Comments: Cross-Cutting Concerns

These are issues that cut across all the improvement docs and should be addressed before scaling beyond the `provider` package.

## Python Version Requirement

The `pyproject.toml` requires `>=3.14`, which isn't even stable yet. Almost nobody runs 3.14 in production. If this SDK is meant to be used by others, it needs to support 3.11+ at minimum.

The main reason for 3.14 is less need for `from __future__ import annotations` and some newer syntax — but that's already handled by the `__future__` import. Dropping to 3.11 means avoiding a few things (PEP 695 `type` statement, some `|` union syntax in runtime positions), but it's manageable and dramatically increases the audience.

This should be a translation rule, not an afterthought.

## Streaming Is the Hardest Translation Problem

The `provider` package is mostly types — easy mode. The `ai` core package has `streamText`, `streamObject`, pipe chains, `TransformStream`, backpressure, and `ReadableStream` controller logic. TS streams and Python async iterators have fundamentally different models. A line-by-line translation will produce code that either doesn't work or has subtle concurrency bugs.

This probably needs a hand-designed streaming foundation (a small `python/packages/ai/streaming.py` module with the right abstractions) that the agents are told to use, rather than letting agents figure out the mapping file-by-file independently.

**Action**: Write a `translation/prompts/streaming-rules.md` before tackling the `ai` package.

## The SDK's Value Proposition in Python

In JavaScript, the AI SDK matters because it:
- Unifies many providers behind one interface
- Handles streaming in a framework-compatible way (React Server Components, Edge runtime)
- Provides `useChat`/`useCompletion` hooks

In Python, the framework integrations (React, Vue, Svelte, Angular, RSC) don't apply at all — those packages should NOT be translated. The streaming benefit is smaller because Python already has a simpler async iteration model.

What DOES translate well:
- Unified provider interface
- Tool calling
- Structured output (`generateObject`)
- Embeddings
- The agent loop (`ToolLoopAgent`)

Make sure the test suite and docs emphasize those, not the things that only matter in JS.

## Some TS Packages Should Never Be Translated

The repo has many more packages than the 9 in scope: `react`, `vue`, `svelte`, `angular`, `rsc`, `codemod`, `langchain`, `azure`, `mistral`, `cohere`, etc. The current plan wisely scopes to 9, but the continuous sync workflow needs a **hard allowlist** so it doesn't try to translate a React hook that got committed to `packages/react/src/`.

A stray `paths: packages/*/src/**` glob in the CI workflow would trigger on those.

## `__init__.py` Re-Exports Are the Python Public API Contract

In TypeScript, the `package.json` `exports` field defines what consumers can import. In Python, it's `__init__.py`. The current system translates `index.ts` → `__init__.py` per-directory, but the package-level public API (what `from ai_sdk.provider import *` gives you) needs careful curation.

If a sync PR adds a new export to a TS `index.ts` and the Python `__init__.py` doesn't update, the new symbol is silently inaccessible. The checker should diff TS exports vs Python `__init__.py` exports as a hard gate.

## The Dataclass Ordering Problem Is a Real Design Flaw

The 210-line escalation file is ~80% "required fields got defaults because of dataclass ordering." This isn't a style nit — it's a semantic divergence.

In TypeScript, `new ToolCall()` without a `toolName` is a type error. In the translated Python, `ToolCall()` silently succeeds with `tool_name=""`. Bugs that TypeScript catches at compile time slip through in Python.

The fix is `@dataclass(frozen=True, kw_only=True)` — then the `type` discriminator can have a default while other fields stay required:

```python
@dataclass(frozen=True, kw_only=True)
class ToolCall:
    type: Literal['tool-call'] = 'tool-call'
    tool_name: str          # required, no default needed with kw_only
    tool_call_id: str       # required
    input: Any              # required
```

**Action**: Update `translation-rules.md` to mandate `kw_only=True` on frozen dataclasses that have discriminator fields. Do this BEFORE translating more packages — don't suppress it as a known-acceptable pattern.

## Cost Projections

Back-of-envelope for full translation:
- 820 source files × (FileAgent + Checker) at current token rates
- Plus 380 test files
- ~1200 agent invocations for the initial batch

Even with token efficiency improvements: **~$50-100 for the initial translation**.

Ongoing sync costs: **~$2-5 per sync run**, adding up to **$100-200/month** if TS changes land daily.

Not huge, but worth setting up cost tracking (the SQLite DB) before scaling past `provider`, so you have real numbers to budget against.

## Source of Truth Policy

The repo has both TypeScript source and Python output. If someone files a bug against the Python SDK, the fix has to happen in the translation rules or prompts, NOT in the Python code — because the next sync will overwrite any hand-edits.

This needs to be:
1. **Documented**: A `python/README.md` that says "DO NOT EDIT — auto-generated from TypeScript source"
2. **Enforced**: A CI check that rejects PRs directly modifying `python/` (only the sync workflow should touch those files)
3. **Clear in error messages**: If someone opens an issue against the Python SDK, the triage should route to translation rules, not Python code fixes

## Priority Actions Before Scaling

| Action | Why | Effort |
|--------|-----|--------|
| Fix `kw_only=True` in translation rules | Prevents semantic bugs in all future translations | 1 hour |
| Drop Python version to 3.11+ | Adoption blocker | 2 hours |
| Write `streaming-rules.md` | `ai` package will fail without it | Half day |
| Add package allowlist to sync workflow | Prevents translating React/Vue/etc | 30 minutes |
| Add "DO NOT EDIT" guards to `python/` | Prevents source-of-truth confusion | 30 minutes |

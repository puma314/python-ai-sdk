# Translation System - Agent Guide

This document explains the TS-to-Python translation system for AI agents working in this codebase.

## Overview

The `translation/` directory contains a multi-agent orchestrator that translates TypeScript packages from the Vercel AI SDK into idiomatic Python. It uses the **Claude Agent SDK** to spawn four types of specialized sub-agents per package.

## Architecture

```
translate.py (orchestrator)
  |
  |-- ScaffoldAgent      Creates directory structure + stub files
  |-- FileAgent (x N)    Translates individual .ts files to .py (parallel)
  |-- CheckerAgent (x N) Validates each translated file (parallel)
  |-- PackageCheckerAgent Holistic validation of entire package
```

### Pipeline per package

1. **Scaffold** -- Creates `python/packages/<name>/` with empty `.py` stubs mirroring the TS `src/` tree
2. **Dependency Graph** -- Builds file-level import graph, topologically sorts files into waves
3. **Translation Loop** -- Processes waves of files in parallel (respecting dependency order):
   - FileAgent translates each file
   - CheckerAgent validates each translation
   - Failed files get retried (up to `max_retries`)
   - Git commits after each batch
4. **Package Check** -- Runs pyright, import smoke tests, cross-file consistency checks

## How to Run

```bash
# From the repo root (pyproject.toml is at root level)

# Dry run - see file discovery and dependency waves
uv run translation/translate.py --packages provider --dry-run

# Translate a single package
uv run translation/translate.py --packages provider

# Translate multiple packages (processed sequentially)
uv run translation/translate.py --packages provider,provider-utils --concurrency 5

# Resume interrupted translation
uv run translation/translate.py --packages provider --resume
```

### CLI flags

| Flag | Default | Description |
|------|---------|-------------|
| `--packages` | (required) | Comma-separated package names |
| `--concurrency` | 5 | Max parallel FileAgents per batch |
| `--max-retries` | 2 | Retry count for failed files |
| `--resume` | false | Skip already-done files from state |
| `--dry-run` | false | Show file plan without translating |

## Key Files

| File | Purpose |
|------|---------|
| `translate.py` | Main orchestrator (~800 lines) |
| `prompts/scaffold-agent.md` | System prompt for ScaffoldAgent |
| `prompts/file-agent.md` | System prompt for FileAgent (has template vars) |
| `prompts/checker-agent.md` | System prompt for CheckerAgent |
| `prompts/package-checker-agent.md` | System prompt for PackageCheckerAgent |
| `prompts/translation-rules.md` | Canonical 700-line translation reference |
| `state/<package>.json` | Per-package file status tracking |
| `state/scaffolding-stream.md` | Shared scratchpad for scaffold decisions |

## Template Variables in Prompts

The FileAgent and CheckerAgent prompts use `{{PLACEHOLDERS}}` that get replaced at runtime:

- `{{SOURCE_PATH}}` -- Original TS file path
- `{{TARGET_PATH}}` -- Destination Python file path
- `{{RULES}}` -- Full content of `translation-rules.md`
- `{{DEPS_CONTEXT}}` -- List of already-translated files
- `{{FEEDBACK}}` -- Checker feedback from previous attempt

## State Management

Translation progress is persisted to `translation/state/<package>.json`:

```json
{
  "package": "provider",
  "files": {
    "packages/provider/src/errors/ai-sdk-error.ts": {
      "target_path": "python/packages/provider/errors/ai_sdk_error.py",
      "status": "done",
      "attempts": 1,
      "last_error": null,
      "dependencies": []
    }
  },
  "summary": { "total": 133, "done": 130, "failed": 3 }
}
```

Use `--resume` to pick up from saved state after interruptions.

## Agent Models

| Agent | Model | Max Turns | Why |
|-------|-------|-----------|-----|
| ScaffoldAgent | sonnet | 40 | Fast structural work |
| FileAgent | opus | 30 | Complex translation needs best model |
| CheckerAgent | sonnet | 15 | Validation is simpler |
| PackageCheckerAgent | opus | 20 | Holistic analysis needs depth |

## Translation Order (respects cross-package dependencies)

1. `provider` -- Core interfaces, no deps
2. `provider-utils` -- Shared utilities, depends on provider
3. `ai` -- Main SDK, depends on provider + provider-utils
4. `anthropic` -- Provider implementation
5. `openai` -- Provider implementation
6. `open-responses` -- OpenAI responses API
7. `google` -- Provider implementation
8. `google-vertex` -- Provider implementation
9. `cerebras` -- Provider implementation

## Key Translation Conventions

- **Python 3.14** -- Use `T | None` not `Optional[T]`, lowercase `dict`/`list`/`tuple`
- **Naming** -- kebab-case files become snake_case, camelCase methods become snake_case
- **Types** -- `interface` -> `Protocol`, data shapes -> `@dataclass(frozen=True)`, Zod -> Pydantic
- **Errors** -- Extend `AISDKError` with class-level `_marker` pattern
- **Docs** -- JSDoc -> Google-style docstrings
- **Imports** -- `@ai-sdk/<name>` -> `ai_sdk.<name>`

## Common Issues

1. **Circular imports**: Use `TYPE_CHECKING` guard for type-only imports
2. **Deadlocks**: If all remaining files have failed dependencies, the queue deadlocks -- check `state/<pkg>.json` for failed files
3. **Checker too strict**: If checker keeps failing on minor issues, file proceeds after max retries (checker failure doesn't block)
4. **Missing `__init__.py`**: Scaffold agent should create these, but verify after scaffold phase

## Project Layout

```
python-ai-sdk/              # Repo root
  pyproject.toml             # Root-level Python project (uv, dependencies)
  .python-version            # Python 3.14
  packages/                  # Original TypeScript source
  python/
    packages/                # Translated Python code (output)
  translation/
    translate.py             # Orchestrator
    prompts/                 # Agent system prompts
    state/                   # Runtime state
```

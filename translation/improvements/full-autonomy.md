# Full Autonomy: Zero-Human-Maintenance Python SDK

## Goal

The Python SDK is a fully auto-generated mirror of the TypeScript AI SDK. No human writes or maintains Python code. The system:

1. Translates the initial codebase (one-time, already in progress)
2. Keeps it in sync with every TS change (continuous)
3. Validates correctness automatically (tests + static analysis)
4. Publishes releases automatically (tied to TS releases)
5. Self-heals when translations break (fix agents + retry loops)

## What "No Humans" Actually Means

| Activity | Human Role | System Role |
|----------|-----------|-------------|
| Writing Python source code | None | Agents translate from TS |
| Writing Python tests | None | Agents translate from TS tests |
| Fixing translation bugs | None | Fix agents retry with feedback |
| Reviewing sync PRs | Approve/reject only | System creates PRs with full validation status |
| Releasing new versions | None (auto-publish) | Triggered by TS releases |
| Updating translation rules | Rare (when patterns fail) | System flags persistent failures |
| Infrastructure maintenance | Rare (CI config, API keys) | N/A |
| Monitoring cost/quality | Periodic dashboard review | System tracks metrics |

The human role shrinks to: (1) approving sync PRs until trust is established, then enabling auto-merge, (2) investigating persistent failures the system can't self-heal, (3) occasional rule updates when new TS patterns emerge.

## System Components

### 1. Translation Engine (Exists)

`translation/translate.py` — the batch orchestrator. Already handles:
- Scaffold → FileAgent → Checker → PackageChecker pipeline
- Dependency-ordered translation
- Retry with checker feedback
- State persistence

**Gaps to fill**: token efficiency, SQLite state, complexity routing (see other docs).

### 2. Continuous Sync (New)

`translation/sync/` — delta translation triggered by TS changes. See `continuous-sync.md`.

**Key property**: Must handle the full lifecycle without human intervention:
- Detect TS diff
- Classify changes (new/modified/deleted)
- Translate delta
- Validate (pyright, tests, imports)
- Open PR with pass/fail status
- Auto-merge if all checks pass (once trust is established)

### 3. Test Mirroring (New)

Translate TS tests alongside source. See `testing-strategy.md`.

**Key property**: Tests are the automated proof that the translation is correct. If tests pass, the sync PR is safe to merge. If tests fail, the system attempts self-healing before flagging.

### 4. Release Pipeline (New)

Mirror TS releases to Python releases automatically.

#### How TS Releases Work

1. Developers add changesets (`.changeset/` files)
2. On merge to main, the release workflow runs `changeset version` → bumps package versions
3. Publishes to npm

#### Python Release Mirror

```yaml
# .github/workflows/python-release.yml
name: Python Release

on:
  # Triggered when the TS release workflow publishes new versions
  workflow_run:
    workflows: ["Release"]
    types: [completed]
    branches: [main]

jobs:
  sync-version:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Detect TS version changes
        id: versions
        run: |
          # Read current TS package versions
          for pkg in provider provider-utils ai openai anthropic; do
            VERSION=$(jq -r .version packages/$pkg/package.json)
            echo "${pkg}_version=$VERSION" >> $GITHUB_OUTPUT
          done

      - name: Update Python pyproject.toml
        run: |
          uv run translation/release/sync_versions.py \
            --provider ${{ steps.versions.outputs.provider_version }} \
            --provider-utils ${{ steps.versions.outputs.provider-utils_version }} \
            --ai ${{ steps.versions.outputs.ai_version }}

      - name: Build and publish
        run: |
          uv build
          uv publish --token ${{ secrets.PYPI_TOKEN }}
```

#### Version Strategy

Option A: **Mirror TS versions exactly**. Python `ai-sdk` version 3.0.8 corresponds to TS `@ai-sdk/provider` 3.0.8.

Option B: **Independent Python versioning** with a mapping table. Python `ai-sdk` version 1.0.0 corresponds to TS versions at a specific commit.

Recommend Option A for simplicity: one fewer thing to maintain.

### 5. Self-Healing Pipeline (New)

When a translation fails validation:

```
Failure detected
    │
    ▼
Classify failure type
    │
    ├─── Import error ──────────▶ Re-translate source file
    ├─── Type error ────────────▶ Re-translate with pyright output as feedback
    ├─── Test assertion error ──▶ Compare TS test behavior, re-translate test
    ├─── Test attribute error ──▶ Fix naming mismatch (lightweight fix agent)
    └─── Unknown ───────────────▶ Flag for investigation
          │
          ▼
    Retry (up to 3x)
          │
          ├─── Success ──▶ Continue pipeline
          └─── Still failing after 3x ──▶ Open GitHub issue
                                          with full diagnostic context
```

The self-healing pipeline is the difference between "auto-generated" and "auto-maintained." Without it, every sync failure becomes a human ticket.

#### Issue Template for Unfixable Failures

```markdown
## Auto-Sync Failure: {{file_path}}

**Sync run**: {{sync_run_id}}
**TS commit**: {{ts_commit_sha}}
**Failure type**: {{failure_type}}

### What happened
The Python translation of `{{ts_file}}` failed validation after 3 auto-fix attempts.

### Pyright output
```
{{pyright_output}}
```

### Last fix agent attempt
```
{{fix_agent_log}}
```

### Suggested action
{{suggested_action}}

### Context
- [Full agent trace]({{trace_url}})
- [Translation DB stats]({{stats_url}})
```

### 6. Observability Dashboard (New)

The SQLite DB (see `state-management.md`) powers a lightweight status dashboard:

```
=== Python SDK Health ===

Packages: 9/9 translated
Total files: 820 translated, 0 pending, 0 failed
Last sync: 2h ago (commit abc1234, 3 files changed, all passed)

Cost (last 30 days):
  Sync runs: 12
  Total tokens: 1.2M
  Est. cost: $4.80

Test health:
  provider:       N/A (no tests)
  provider-utils: 72/80 passing (90%)
  ai:             145/200 passing (72%)
  openai:         38/42 passing (90%)
  anthropic:      35/40 passing (88%)

Open issues: 2
  #142: ai/generate-text.ts sync failed (signature change)
  #139: provider-utils/schema.ts test timeout
```

This can be a CLI command (`uv run translation/translate.py --dashboard`) or a simple HTML page generated by CI and hosted on GitHub Pages.

## Maturity Levels

The system doesn't need to be fully autonomous on day one. Plan for graduated trust:

### Level 0: Batch Translation (Current)

- Human runs `translate.py` manually
- Human reviews output, commits
- No CI, no sync, no tests

### Level 1: Validated Batch (Next)

- SQLite state tracking
- Token efficiency improvements
- Pyright + import checks run automatically
- Human still triggers and reviews

### Level 2: Sync with Human Gate

- CI workflow detects TS changes
- Agents translate delta automatically
- PR opened with validation results
- **Human approves/merges** every sync PR
- Tests translated alongside source

### Level 3: Auto-Merge for Safe Changes

- Implementation-only changes auto-merge if:
  - Pyright passes
  - All translated tests pass
  - No cross-package impact
- Signature changes still require human review
- Self-healing handles minor failures

### Level 4: Full Autonomy

- All sync PRs auto-merge if validation passes
- Releases publish automatically when TS releases
- GitHub issues auto-created for unfixable failures
- Human role: monitor dashboard, update rules when needed
- Cost tracked and budgeted

### Timeline Estimate

| Level | Prerequisite | Effort |
|-------|-------------|--------|
| Level 0 → 1 | State DB + token efficiency | 1 week |
| Level 1 → 2 | Sync workflow + test translation | 2 weeks |
| Level 2 → 3 | Self-healing + confidence in test suite | 2 weeks + 1 month of monitoring |
| Level 3 → 4 | Release pipeline + dashboard | 1 week + confidence period |

## Remaining Gaps Beyond What's Documented

### a. Package Structure for Publishing

The current layout is:
```
python/packages/provider/
python/packages/provider_utils/
python/packages/ai/
```

For PyPI publishing, each package needs its own `pyproject.toml`, or everything ships as one `ai-sdk` package. Decision needed:

- **Monolith** (`pip install ai-sdk`): Simpler. One package, one version. Users get everything.
- **Split** (`pip install ai-sdk-provider`, `pip install ai-sdk-openai`): Mirrors the npm structure. Users install only what they need.

Recommendation: Start with monolith. Split later if size becomes an issue. The TS SDK split exists because npm tree-shaking needs it — Python doesn't have this concern.

### b. Documentation Generation

The TS SDK has documentation at `ai-sdk.dev`. The Python SDK needs docs too, but they should be auto-generated:

1. **Docstrings are already translated** (Google-style) from JSDoc
2. **Generate API reference** from docstrings using `mkdocstrings` or `sphinx-autodoc`
3. **Usage examples** can be translated from `examples/` directory
4. **Host on GitHub Pages** or Read the Docs

This is low priority compared to correctness, but important for adoption.

### c. Dependency Version Pinning

The Python SDK depends on `pydantic>=2.10`, `httpx>=0.27`, etc. These need:
- A policy for when to bump minimum versions
- CI testing against minimum AND latest versions
- Dependabot or Renovate for automated updates

### d. Error Message Parity

When the TS SDK throws `AISDKError("No API key found")`, the Python SDK should throw the same message text. This is tested implicitly if we translate tests, but worth calling out as a design constraint: error messages are part of the public API.

### e. Performance Benchmarking

Once the Python SDK works, it should be benchmarked against raw `httpx` calls to ensure the SDK abstraction layer doesn't add unreasonable overhead. This is a one-time setup, not ongoing maintenance.

### f. Type Stub Publishing

For maximum IDE support, consider publishing `py.typed` marker and ensuring the package plays well with mypy/pyright in user projects. The translated code already has full type annotations, so this is mostly a packaging concern.

## Summary of All Improvement Docs

| Document | Focus | Status |
|----------|-------|--------|
| `token-efficiency.md` | Reduce token waste by 35-45% | Written |
| `state-management.md` | SQLite DB for tracking, hierarchy, analytics | Written |
| `continuous-sync.md` | CI pipeline for mirroring TS changes | Written |
| `testing-strategy.md` | Auto-generated test suite from TS tests | Written |
| `full-autonomy.md` | Vision for zero-maintenance Python SDK | This doc |

Implementation order:
1. State management (measurement infrastructure)
2. Token efficiency (reduce cost of everything that follows)
3. Complete initial batch translation (all 9 packages)
4. Test translation (proves correctness)
5. Continuous sync (keeps it alive)
6. Release pipeline (ships it)
7. Graduate to auto-merge (full autonomy)

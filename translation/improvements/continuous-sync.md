# Continuous Sync: TS → Python Mirror Pipeline

## Vision

After the initial batch translation is complete, the Python SDK should stay in sync with the TypeScript source automatically. When a PR merges to `main` that changes TypeScript source in `packages/`, a CI job detects the diff, re-translates only the affected files, validates the result, and opens a PR with the Python-side changes.

This turns a one-time migration into a living mirror.

## Why This Matters

The TS AI SDK ships releases frequently — the changelog shows patch versions every few days. Without automated sync, the Python port will drift within weeks. Manual re-translation is expensive and error-prone. The whole point of the agent-based approach is that it can be re-run cheaply on deltas.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    GitHub Actions                        │
│                                                         │
│  on: push to main (paths: packages/**/src/**)           │
│                                                         │
│  ┌─────────────┐    ┌──────────────┐    ┌────────────┐ │
│  │ 1. Diff      │───▶│ 2. Classify  │───▶│ 3. Translate│ │
│  │   Detection  │    │   Changes    │    │   Delta     │ │
│  └─────────────┘    └──────────────┘    └────────────┘ │
│                                                │        │
│                                         ┌──────▼──────┐ │
│  ┌─────────────┐    ┌──────────────┐   │ 4. Validate  │ │
│  │ 7. Open PR   │◀──│ 6. Commit    │◀──│   & Test     │ │
│  └─────────────┘    └──────────────┘   └─────────────┘ │
│                                                │        │
│                                         ┌──────▼──────┐ │
│                                         │ 5. Propagate │ │
│                                         │   Downstream │ │
│                                         └─────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Step 1: Diff Detection

### Trigger

```yaml
on:
  push:
    branches: [main]
    paths:
      - 'packages/*/src/**/*.ts'
      - '!packages/*/src/**/*.test.ts'
      - '!packages/*/src/**/*.test-d.ts'
```

### Script: `translation/sync/detect_changes.py`

```python
def detect_changes(base_sha: str, head_sha: str) -> list[Change]:
    """Parse git diff to find changed TS source files."""
    result = subprocess.run(
        ["git", "diff", "--name-status", base_sha, head_sha, "--", "packages/*/src/"],
        capture_output=True, text=True,
    )

    changes = []
    for line in result.stdout.splitlines():
        status, *paths = line.split("\t")
        path = paths[0]

        # Skip non-translatable files
        if any(pat.search(path) for pat in EXCLUDE_PATTERNS):
            continue

        change_type = {
            "A": "added",
            "M": "modified",
            "D": "deleted",
        }.get(status[0], "modified")  # R (rename) → treat as modified

        # For renames, capture both old and new path
        if status.startswith("R"):
            change_type = "renamed"
            old_path = paths[0]
            path = paths[1]
            changes.append(Change(path=path, old_path=old_path, type=change_type))
        else:
            changes.append(Change(path=path, type=change_type))

    return changes
```

### Output

```json
{
  "changes": [
    {"path": "packages/provider/src/errors/ai-sdk-error.ts", "type": "modified"},
    {"path": "packages/ai/src/core/generate-text.ts", "type": "modified"},
    {"path": "packages/openai/src/openai-responses-provider.ts", "type": "added"}
  ],
  "packages_affected": ["provider", "ai", "openai"],
  "commit_range": "abc1234..def5678"
}
```

## Step 2: Classify Changes

Not all changes need the same treatment.

### Change Categories

| Category | Example | Action |
|----------|---------|--------|
| **New file** | New TS file added | Full translation (FileAgent) |
| **Modified file** | Existing file changed | Delta translation (see below) |
| **Deleted file** | TS file removed | Delete Python file + update `__init__.py` |
| **Renamed file** | File moved/renamed | Rename Python file + update imports |
| **New export** | New symbol added to `index.ts` | Update `__init__.py` |
| **Type change** | Interface field type changed | Re-translate file + check dependents |

### Impact Analysis

For modified files, check if the change is:
- **Signature change** (function params, return types, class fields) → re-translate the file AND flag dependents for re-checking
- **Implementation-only change** (body of a function, internal logic) → re-translate just the file
- **Documentation-only change** (JSDoc updates) → re-translate just the file with a lightweight agent
- **Import change** (added/removed imports) → re-translate and verify Python imports

```python
def classify_modification(old_content: str, new_content: str) -> str:
    """Classify a file modification by analyzing the diff."""
    # Parse both versions to extract public API surface
    old_exports = extract_exports(old_content)
    new_exports = extract_exports(new_content)

    if old_exports.signatures != new_exports.signatures:
        return "signature_change"  # breaking: check dependents
    elif old_exports.names != new_exports.names:
        return "export_change"     # new/removed exports
    elif only_jsdoc_changed(old_content, new_content):
        return "docs_only"
    else:
        return "implementation"    # internal logic change
```

### Downstream Impact Graph

When a file's public API changes, find all files that import from it:

```python
def find_dependents(changed_file: str, package: str) -> list[str]:
    """Find all files in the package that import from the changed file."""
    graph = build_dependency_graph(f"packages/{package}")
    dependents = []
    for file_path, info in graph.items():
        if changed_file in info.deps:
            dependents.append(file_path)
    return dependents
```

For cross-package changes (e.g., `provider` type changes affecting `ai`), the sync job flags these for manual review rather than auto-translating, since cross-package changes are higher risk.

## Step 3: Delta Translation

### For Modified Files

Instead of full re-translation, use a diff-aware prompt:

```markdown
# Delta Translation Agent

A TypeScript source file has been updated. The Python translation needs to be updated to match.

## TypeScript Diff
```diff
{{TS_DIFF}}
```

## Current Python Translation
```python
{{CURRENT_PYTHON}}
```

## Instructions
1. Analyze the TypeScript diff to understand what changed
2. Apply the equivalent changes to the Python translation
3. Do NOT rewrite the entire file — make targeted edits
4. If the diff adds new exports, add corresponding Python exports
5. If the diff changes a type signature, update the Python type annotations
6. Write the updated file
```

This is dramatically cheaper than full re-translation:
- The prompt contains only the diff (usually small) and the current Python file
- No need for the full translation rules (the file was already translated correctly once)
- Can use Sonnet instead of Opus for most deltas

### For New Files

Use the existing FileAgent flow, but scoped to just the new file(s). The rest of the package is already translated, so `{{DEPS_CONTEXT}}` is complete.

### For Deleted Files

Handle in the orchestrator directly — no agent needed:

```python
def handle_deletion(change: Change) -> None:
    target = ts_path_to_py_path(change.path)
    target_full = ROOT / target
    if target_full.exists():
        target_full.unlink()
    # Update __init__.py to remove the import
    update_init_py_for_deletion(target)
```

## Step 4: Validate & Test

After translating the delta:

1. **Pyright** on affected files:
   ```bash
   uv run pyright python/packages/<pkg>/<changed_files>
   ```

2. **Import smoke test**:
   ```bash
   PYTHONPATH=python uv run python -c "import ai_sdk.<pkg>"
   ```

3. **Run checker agents** on each changed file (same as batch translation, but only on the delta).

4. **Run affected tests** (once test translation exists — see `testing-strategy.md`):
   ```bash
   uv run pytest python/packages/<pkg>/tests/ -k "<affected_test_pattern>"
   ```

5. **Cross-package import check**: If the changed package is imported by other translated packages, verify those imports still resolve.

## Step 5: Propagate Downstream

If a change in `provider` affects types used by `ai` or `openai`, the sync job needs to:

1. Identify which downstream packages import the changed symbols
2. Re-check (not re-translate) those downstream files to see if they still compile
3. If a downstream file fails pyright due to the upstream change, add it to the translation queue

This is the hardest part. A conservative approach:

```python
def propagate_downstream(changed_package: str, changed_symbols: set[str]) -> list[str]:
    """Find downstream packages that need re-checking."""
    downstream_packages = get_packages_depending_on(changed_package)
    affected_files = []

    for pkg in downstream_packages:
        pkg_files = discover_source_files(f"packages/{pkg}")
        for f in pkg_files:
            target = ts_path_to_py_path(f)
            if (ROOT / target).exists():
                content = (ROOT / target).read_text()
                # Check if this file imports any of the changed symbols
                if any(symbol in content for symbol in changed_symbols):
                    affected_files.append(target)

    return affected_files
```

For the initial version, if downstream files break, the sync PR should flag them for human review rather than attempting auto-fix.

## Step 6 & 7: Commit and Open PR

```yaml
- name: Create sync branch
  run: git checkout -b python-sync/${{ github.sha }}

- name: Run delta translation
  run: |
    uv run translation/sync/run_delta.py \
      --base ${{ github.event.before }} \
      --head ${{ github.sha }}

- name: Commit changes
  run: |
    git add python/packages/
    git commit -m "sync(python): mirror TS changes from ${{ github.sha }}"

- name: Open PR
  run: |
    gh pr create \
      --title "sync(python): mirror TS changes" \
      --body "$(cat <<'EOF'
    ## Auto-generated Python sync

    TypeScript changes in ${{ github.sha }} have been mirrored to the Python SDK.

    ### Changed files
    $(cat /tmp/sync_summary.md)

    ### Validation
    - [ ] Pyright: $(cat /tmp/pyright_result.txt)
    - [ ] Import smoke test: $(cat /tmp/import_result.txt)
    - [ ] Checker agents: $(cat /tmp/checker_result.txt)

    ### Needs manual review
    $(cat /tmp/manual_review.md)
    EOF
    )"
```

## Handling Edge Cases

### Breaking Changes in TS

When the TS side makes a breaking change (major version bump via changesets):
- The sync job detects this from the changeset metadata
- Opens a larger PR flagged as "breaking change sync"
- May require re-translating entire files rather than deltas
- Always requires human review before merge

### New Packages

When a new `packages/<name>` directory appears:
- The sync job runs the full scaffold + translation pipeline for it
- Opens a separate PR: "sync(python): add new package `<name>`"

### Circular Changes

Guard against the sync job creating changes that trigger itself:

```yaml
# In the workflow trigger
paths-ignore:
  - 'python/**'
  - 'translation/**'
```

### Rate Limits / Cost Control

- Set a token budget per sync run (e.g., 500K tokens max)
- If the delta is too large (>20 files changed), skip auto-translation and open an issue instead
- Track cumulative cost in the SQLite DB per sync run

## GitHub Actions Workflow

```yaml
name: Python Sync

on:
  push:
    branches: [main]
    paths:
      - 'packages/*/src/**/*.ts'
      - '!packages/*/src/**/*.test.ts'
      - '!packages/*/src/**/*.test-d.ts'
      - '!packages/*/src/**/*.tsx'

# Don't run on changes to Python output
paths-ignore:
  - 'python/**'

concurrency:
  group: python-sync
  cancel-in-progress: true

jobs:
  sync:
    name: Mirror TS Changes to Python
    runs-on: ubuntu-latest
    timeout-minutes: 30

    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0

      - uses: astral-sh/setup-uv@v4
        with:
          version: "latest"

      - name: Install Python 3.14
        run: uv python install 3.14

      - name: Install dependencies
        run: uv sync

      - name: Detect changes
        id: detect
        run: |
          uv run translation/sync/detect_changes.py \
            --base ${{ github.event.before }} \
            --head ${{ github.sha }} \
            --output /tmp/changes.json

      - name: Check delta size
        id: size-check
        run: |
          FILE_COUNT=$(jq '.changes | length' /tmp/changes.json)
          if [ "$FILE_COUNT" -gt 20 ]; then
            echo "skip=true" >> $GITHUB_OUTPUT
            echo "Delta too large ($FILE_COUNT files). Opening issue instead."
          else
            echo "skip=false" >> $GITHUB_OUTPUT
          fi

      - name: Run delta translation
        if: steps.size-check.outputs.skip != 'true'
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          uv run translation/sync/run_delta.py \
            --changes /tmp/changes.json \
            --max-tokens 500000

      - name: Validate
        if: steps.size-check.outputs.skip != 'true'
        run: |
          uv run pyright python/packages/ 2>&1 | tee /tmp/pyright.txt || true
          PYTHONPATH=python uv run python -c "
          import importlib, json
          changes = json.load(open('/tmp/changes.json'))
          for pkg in changes['packages_affected']:
              mod = f'ai_sdk.{pkg.replace(\"-\", \"_\")}'
              importlib.import_module(mod)
              print(f'OK: {mod}')
          " 2>&1 | tee /tmp/import.txt

      - name: Create PR
        if: steps.size-check.outputs.skip != 'true'
        run: |
          git checkout -b python-sync/${{ github.sha }}
          git add python/packages/
          git commit -m "sync(python): mirror TS changes from ${GITHUB_SHA::8}"
          git push origin python-sync/${{ github.sha }}
          gh pr create \
            --title "sync(python): mirror TS changes from ${GITHUB_SHA::8}" \
            --body "Auto-generated sync PR. See workflow run for details."

      - name: Open issue for large delta
        if: steps.size-check.outputs.skip == 'true'
        run: |
          gh issue create \
            --title "Python sync needed: large TS delta ($(jq '.changes | length' /tmp/changes.json) files)" \
            --body "The TS changes in ${{ github.sha }} affect too many files for auto-sync. Manual translation run needed."
```

## New Files Needed

| File | Purpose |
|------|---------|
| `translation/sync/__init__.py` | Package marker |
| `translation/sync/detect_changes.py` | Git diff parsing, change classification |
| `translation/sync/classify.py` | Signature vs implementation vs docs-only classification |
| `translation/sync/run_delta.py` | Orchestrator for delta translation (subset of translate.py) |
| `translation/sync/propagate.py` | Downstream impact analysis |
| `translation/prompts/delta-agent.md` | Prompt for modifying existing translations |
| `.github/workflows/python-sync.yml` | GitHub Actions workflow |

## Prerequisites

| Dependency | Why |
|-----------|-----|
| Initial translation complete (all 9 packages) | Nothing to sync against if the base doesn't exist |
| SQLite state DB (`state-management.md`) | Need to track sync runs, costs, which files were synced |
| Token efficiency improvements (`token-efficiency.md`) | Delta translation should use the optimized prompts |
| Basic test suite (`testing-strategy.md`) | Need automated validation beyond pyright |

## Open Questions

1. **Where does the Anthropic API key live?** GitHub Actions secrets, but who owns the billing?
2. **Should sync PRs auto-merge if validation passes?** Probably not initially — human review for the first few months, then graduate to auto-merge for implementation-only changes.
3. **What about TS test changes?** If a TS test changes, should the sync job also update the Python test? This depends on whether we translate tests (see `testing-strategy.md`).
4. **Monorepo vs fork?** If the Python SDK eventually lives in its own repo, the sync trigger changes from "push to main" to "watch upstream releases via repository_dispatch" (similar to the existing `ai-provider-api-changes.yml` workflow).

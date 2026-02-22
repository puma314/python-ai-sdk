# Structured State Management with SQLite

## Problem

The current state system uses flat JSON files and append-only markdown, which creates several issues:

1. **No agent lineage.** You can't trace which checker validated which file-agent's output, or which retry followed which failure.
2. **No timing or cost data.** Log files have timestamps in filenames but nothing is queryable. You can't answer "which files cost the most tokens?"
3. **Lost structured output.** The checker returns `{verdict, failures, escalations}` but only `last_error` (a string) persists. Escalations go to an append-only markdown file with no deduplication or querying.
4. **Resume is binary.** `--resume` only checks if a file is "done." It can't distinguish "file-agent succeeded but checker hasn't run" from "checker failed and needs retry."
5. **No cross-run analysis.** After translating 3 packages, you can't compare cost-per-file across packages or identify systematic patterns.

## Current State Files

| File | Format | Contents | Limitations |
|------|--------|----------|------------|
| `state/<pkg>.json` | JSON | File statuses, attempt counts, last error | No timing, no agent run history, no checker details |
| `state/escalation.md` | Markdown | Append-only checker notes | No dedup, no querying, not linked to specific runs |
| `state/scaffolding-stream.md` | Markdown | Scaffold agent notes | Append-only scratchpad |
| `logs/<agent-type>/<label>_<ts>.log` | Text | Full agent conversation | Not linked to state, not queryable |

## Proposed Architecture

### SQLite Database

Single file at `translation/state/translation.db`. Python's `sqlite3` is stdlib — no new dependency.

### Schema

```sql
-- ============================================================
-- Packages
-- ============================================================
CREATE TABLE packages (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL UNIQUE,        -- 'provider', 'provider-utils', etc.
    status          TEXT NOT NULL DEFAULT 'pending',  -- pending | scaffolding | translating | checking | done | failed
    total_files     INTEGER,
    started_at      TEXT,                        -- ISO 8601
    finished_at     TEXT,
    scaffold_run_id INTEGER REFERENCES agent_runs(id)
);

-- ============================================================
-- Files
-- ============================================================
CREATE TABLE files (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id      INTEGER NOT NULL REFERENCES packages(id),
    source_path     TEXT NOT NULL UNIQUE,
    target_path     TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'pending',  -- pending | translating | checking | done | failed | skipped
    complexity      TEXT,                        -- trivial | simple | complex
    source_lines    INTEGER,                     -- for routing/analytics
    topo_depth      INTEGER,                     -- topological sort depth
    current_attempt INTEGER DEFAULT 0,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_files_package ON files(package_id);
CREATE INDEX idx_files_status ON files(status);

-- ============================================================
-- File Dependencies
-- ============================================================
CREATE TABLE file_deps (
    file_id         INTEGER NOT NULL REFERENCES files(id),
    depends_on_id   INTEGER NOT NULL REFERENCES files(id),
    PRIMARY KEY (file_id, depends_on_id)
);

CREATE INDEX idx_file_deps_dep ON file_deps(depends_on_id);

-- ============================================================
-- Agent Runs (the core table)
-- ============================================================
CREATE TABLE agent_runs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    -- Hierarchy
    package_id      INTEGER NOT NULL REFERENCES packages(id),
    file_id         INTEGER REFERENCES files(id),           -- NULL for scaffold, package-checker
    parent_run_id   INTEGER REFERENCES agent_runs(id),      -- who spawned this agent

    -- Identity
    agent_type      TEXT NOT NULL,               -- scaffold | file | checker | fix | package-checker
    model           TEXT NOT NULL,               -- opus | sonnet | haiku | none (for inline)
    attempt         INTEGER DEFAULT 1,           -- which attempt for this file+agent_type

    -- Lifecycle
    status          TEXT NOT NULL DEFAULT 'running',  -- running | success | failed | error | skipped
    started_at      TEXT NOT NULL DEFAULT (datetime('now')),
    finished_at     TEXT,
    duration_sec    REAL,                         -- computed on completion

    -- Cost tracking
    prompt_tokens   INTEGER,
    output_tokens   INTEGER,
    total_tokens    INTEGER,
    turns           INTEGER,                     -- number of API round trips
    tools_used      TEXT,                        -- JSON array of tool names used

    -- Diagnostics
    log_path        TEXT,                        -- path to full conversation log
    error_message   TEXT,                        -- if status = failed | error
    result_summary  TEXT                         -- brief text summary of what happened
);

CREATE INDEX idx_runs_file ON agent_runs(file_id);
CREATE INDEX idx_runs_package ON agent_runs(package_id);
CREATE INDEX idx_runs_parent ON agent_runs(parent_run_id);
CREATE INDEX idx_runs_type ON agent_runs(agent_type);

-- ============================================================
-- Checker Verdicts
-- ============================================================
CREATE TABLE checker_verdicts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id          INTEGER NOT NULL REFERENCES agent_runs(id),
    file_id         INTEGER NOT NULL REFERENCES files(id),
    verdict         TEXT NOT NULL,               -- PASSED | FAILED
    failures        TEXT,                        -- JSON array of failure strings
    escalations     TEXT,                        -- JSON array of escalation strings
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_verdicts_file ON checker_verdicts(file_id);
CREATE INDEX idx_verdicts_run ON checker_verdicts(run_id);

-- ============================================================
-- Escalations (normalized, deduplicated)
-- ============================================================
CREATE TABLE escalations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id         INTEGER NOT NULL REFERENCES files(id),
    run_id          INTEGER NOT NULL REFERENCES agent_runs(id),
    pattern         TEXT NOT NULL,               -- normalized short key for grouping
    message         TEXT NOT NULL,               -- full escalation text
    suppressed      INTEGER DEFAULT 0,           -- 1 if this pattern is now suppressed
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_escalations_pattern ON escalations(pattern);
CREATE INDEX idx_escalations_file ON escalations(file_id);

-- ============================================================
-- Views for common queries
-- ============================================================

-- Cost per file (all agent types combined)
CREATE VIEW v_file_cost AS
SELECT
    f.id,
    f.source_path,
    f.target_path,
    f.complexity,
    f.source_lines,
    f.status,
    COUNT(r.id) AS total_runs,
    SUM(r.total_tokens) AS total_tokens,
    SUM(r.prompt_tokens) AS total_prompt_tokens,
    SUM(r.output_tokens) AS total_output_tokens,
    SUM(r.duration_sec) AS total_duration_sec,
    MAX(r.attempt) AS max_attempts
FROM files f
LEFT JOIN agent_runs r ON r.file_id = f.id
GROUP BY f.id;

-- Cost breakdown by agent type and model
CREATE VIEW v_cost_by_agent AS
SELECT
    agent_type,
    model,
    COUNT(*) AS run_count,
    SUM(total_tokens) AS total_tokens,
    AVG(total_tokens) AS avg_tokens,
    SUM(duration_sec) AS total_duration_sec,
    AVG(turns) AS avg_turns
FROM agent_runs
WHERE status IN ('success', 'failed')
GROUP BY agent_type, model;

-- Top escalation patterns
CREATE VIEW v_escalation_patterns AS
SELECT
    pattern,
    COUNT(*) AS occurrences,
    COUNT(DISTINCT file_id) AS files_affected,
    MAX(suppressed) AS is_suppressed
FROM escalations
GROUP BY pattern
ORDER BY occurrences DESC;

-- Files that are ready to translate (deps met)
CREATE VIEW v_ready_files AS
SELECT f.*
FROM files f
WHERE f.status = 'pending'
  AND NOT EXISTS (
    SELECT 1 FROM file_deps fd
    JOIN files dep ON dep.id = fd.depends_on_id
    WHERE fd.file_id = f.id AND dep.status != 'done'
  );
```

## Agent Hierarchy Design

### Concept

Every agent run has a `parent_run_id` that creates a tree:

```
Package: provider
├── scaffold_run (id=1, parent=NULL)
│
├── file_run (id=2, parent=NULL, file=ai-sdk-error.ts, attempt=1)
│   └── checker_run (id=10, parent=2, verdict=PASSED)
│
├── file_run (id=3, parent=NULL, file=json-value.ts, attempt=1)
│   └── checker_run (id=11, parent=3, verdict=FAILED)
│       └── fix_run (id=20, parent=11, file=json-value.ts, attempt=2)
│           └── checker_run (id=21, parent=20, verdict=PASSED)
│
└── package_checker_run (id=100, parent=NULL)
```

### Parent Assignment Rules

| Agent Type | parent_run_id |
|-----------|--------------|
| scaffold | NULL (top-level for the package) |
| file (attempt 1) | NULL (top-level, spawned by orchestrator) |
| checker | The file_run or fix_run it's validating |
| fix (retry) | The checker_run that triggered the retry |
| package-checker | NULL (top-level for the package) |

### Implementation in Orchestrator

The orchestrator passes parent IDs through the existing flow:

```python
# In the translation loop:
file_run_id = db.insert_agent_run(
    package_id=pkg_id,
    file_id=f.id,
    parent_run_id=None,
    agent_type="file",
    model=model_for_complexity(f.complexity),
    attempt=f.current_attempt,
)

# After file agent completes, spawn checker with parent:
checker_run_id = db.insert_agent_run(
    package_id=pkg_id,
    file_id=f.id,
    parent_run_id=file_run_id,
    agent_type="checker",
    model="sonnet",
    attempt=f.current_attempt,
)

# If checker fails and retry needed:
fix_run_id = db.insert_agent_run(
    package_id=pkg_id,
    file_id=f.id,
    parent_run_id=checker_run_id,  # linked to the failing checker
    agent_type="fix",
    model="sonnet",
    attempt=f.current_attempt + 1,
)
```

### Trace Query

To see the full history of a problematic file:

```sql
-- All runs for json-value.ts, in order
SELECT
    r.id,
    r.agent_type,
    r.attempt,
    r.status,
    r.parent_run_id,
    r.model,
    r.turns,
    r.total_tokens,
    r.duration_sec,
    r.error_message,
    cv.verdict,
    cv.failures
FROM agent_runs r
LEFT JOIN checker_verdicts cv ON cv.run_id = r.id
WHERE r.file_id = (SELECT id FROM files WHERE source_path LIKE '%json-value.ts')
ORDER BY r.started_at;
```

## Database Access Layer

### Class Design

```python
class TranslationDB:
    """SQLite-backed state management for the translation orchestrator."""

    def __init__(self, db_path: Path):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")  # concurrent reads
        self.conn.execute("PRAGMA foreign_keys=ON")
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        """Create tables if they don't exist. Idempotent."""
        self.conn.executescript(SCHEMA_SQL)

    # -- Package operations --

    def get_or_create_package(self, name: str) -> int:
        """Returns package ID, creating if needed."""
        ...

    def update_package_status(self, pkg_id: int, status: str) -> None:
        ...

    # -- File operations --

    def insert_files(self, pkg_id: int, file_infos: list[FileInfo]) -> None:
        """Bulk insert files with complexity, line count, depth."""
        ...

    def get_ready_files(self, pkg_id: int, limit: int) -> list[FileRow]:
        """Files whose deps are all done. Uses v_ready_files view."""
        ...

    def update_file_status(self, file_id: int, status: str) -> None:
        ...

    def get_file_deps(self, file_id: int) -> list[FileRow]:
        """Return only the direct dependencies of a file (for scoped deps_context)."""
        ...

    # -- Agent run operations --

    def start_run(self, *, package_id: int, file_id: int | None,
                  parent_run_id: int | None, agent_type: str,
                  model: str, attempt: int) -> int:
        """Insert a new agent run, return its ID."""
        ...

    def finish_run(self, run_id: int, *, status: str,
                   prompt_tokens: int | None = None,
                   output_tokens: int | None = None,
                   turns: int | None = None,
                   tools_used: list[str] | None = None,
                   log_path: str | None = None,
                   error_message: str | None = None,
                   result_summary: str | None = None) -> None:
        """Mark a run as complete. Computes duration_sec automatically."""
        ...

    # -- Checker operations --

    def insert_verdict(self, run_id: int, file_id: int, verdict: str,
                       failures: list[str], escalations: list[str]) -> None:
        """Store checker verdict. Auto-inserts escalations with pattern extraction."""
        ...

    def get_suppressed_patterns(self) -> list[str]:
        """Patterns seen 3+ times. Used to add to checker prompt dynamically."""
        ...

    # -- Resume support --

    def get_resume_state(self, pkg_id: int) -> dict:
        """Rich resume: returns files with their last run status, checker verdicts, etc."""
        ...

    # -- Analytics --

    def print_stats(self, pkg_id: int | None = None) -> None:
        """Print cost/timing/retry stats. Used by --stats flag."""
        ...
```

### Context Manager for Runs

```python
@contextmanager
def tracked_run(self, **kwargs) -> Generator[int, None, None]:
    """Context manager that auto-finishes a run on exit."""
    run_id = self.start_run(**kwargs)
    try:
        yield run_id
        # Caller sets status via finish_run
    except Exception as e:
        self.finish_run(run_id, status="error", error_message=str(e))
        raise
```

Usage in the orchestrator:

```python
with db.tracked_run(
    package_id=pkg_id,
    file_id=f.db_id,
    parent_run_id=None,
    agent_type="file",
    model=model,
    attempt=f.current_attempt,
) as run_id:
    result, is_error, _ = await collect_result(query(...), log_file=log_file)
    db.finish_run(
        run_id,
        status="failed" if is_error else "success",
        log_path=str(log_file),
        error_message=result if is_error else None,
        result_summary=result[:500] if not is_error else None,
    )
```

## Token Counting

### From Claude Agent SDK

The agent SDK likely provides token usage in the response metadata. Check for:
- `ResultMessage.usage.input_tokens`
- `ResultMessage.usage.output_tokens`

If available, capture in `collect_result` and return alongside the result text.

### Fallback: Approximate from Logs

If the SDK doesn't expose token counts, approximate:
- Count message objects in the log (each `[AssistantMessage]` or `[UserMessage]` is a turn)
- Estimate tokens from character count (roughly 4 chars per token for English/code)

### Updated `collect_result`

```python
async def collect_result(
    query_iter: Any,
    log_file: Path | None = None,
) -> tuple[str, bool, Any, dict]:    # added: metrics dict
    """Returns (result_text, is_error, structured_output, metrics)."""
    metrics = {"turns": 0, "prompt_tokens": 0, "output_tokens": 0, "tools_used": set()}

    async for message in query_iter:
        if message is None:
            continue

        if hasattr(message, "role") and message.role == "assistant":
            metrics["turns"] += 1

        # Capture tool usage
        if hasattr(message, "tool_name"):
            metrics["tools_used"].add(message.tool_name)

        # Capture token usage if available
        if hasattr(message, "usage"):
            metrics["prompt_tokens"] += getattr(message.usage, "input_tokens", 0)
            metrics["output_tokens"] += getattr(message.usage, "output_tokens", 0)

        ...

    metrics["tools_used"] = list(metrics["tools_used"])
    return last_result, is_error, structured_output, metrics
```

## Escalation Pattern Extraction

### Auto-Categorization

When inserting escalations, normalize to a pattern key:

```python
ESCALATION_PATTERNS = {
    r"Module docstring appears after.*__future__": "docstring-after-future",
    r"Required .* fields? .* default": "required-field-has-default",
    r"Unused import.*field": "unused-field-import",
    r"absolute.*import.*rather than relative": "absolute-vs-relative-import",
    r"Unused import.*Any": "unused-any-import",
    r"PEP 257": "pep257-docstring-order",
}

def extract_pattern(message: str) -> str:
    for regex, pattern in ESCALATION_PATTERNS.items():
        if re.search(regex, message, re.IGNORECASE):
            return pattern
    return "other"
```

### Dynamic Suppression

After N occurrences of the same pattern, auto-add to checker prompt:

```python
def build_checker_known_patterns(db: TranslationDB) -> str:
    suppressed = db.get_suppressed_patterns()  # patterns with 3+ occurrences
    if not suppressed:
        return ""
    lines = ["## Known Project Conventions (do NOT escalate these)\n"]
    for pattern, count, example in suppressed:
        lines.append(f"- {example} (seen {count} times, accepted)")
    return "\n".join(lines)
```

## Migration from Current State

### One-Time Import Script

```python
def migrate_json_to_db(db: TranslationDB) -> None:
    """Import existing provider.json and escalation.md into the DB."""

    # 1. Import provider.json
    state = json.loads((STATE_DIR / "provider.json").read_text())
    pkg_id = db.get_or_create_package("provider")

    for source_path, info in state["files"].items():
        file_id = db.insert_file(
            pkg_id, source_path, info["target_path"],
            status=info["status"],
        )
        # Create synthetic agent_run records for completed files
        if info["status"] == "done":
            for attempt in range(1, info["attempts"] + 1):
                run_id = db.start_run(
                    package_id=pkg_id, file_id=file_id,
                    parent_run_id=None, agent_type="file",
                    model="opus", attempt=attempt,
                )
                db.finish_run(run_id, status="success")

    # 2. Import escalation.md
    for line in (STATE_DIR / "escalation.md").read_text().splitlines():
        m = re.match(r"\[(.+?)\]\s*(.+)", line)
        if m:
            file_path, message = m.group(1), m.group(2)
            pattern = extract_pattern(message)
            # Find file_id by target_path
            ...
```

### Coexistence Period

During migration, keep both JSON and DB active:
- Read from DB for all new operations
- Write to both DB and JSON for backward compatibility
- Remove JSON writes once DB is validated

## CLI Additions

### `--stats` Flag

```bash
uv run translation/translate.py --stats
uv run translation/translate.py --stats --packages provider
```

Output:

```
=== Translation Stats: provider ===

Files: 133 total, 112 done, 0 failed, 21 pending
Tokens: 3.2M total (2.4M prompt, 0.8M output)
Duration: 47 min

By agent type:
  file-agent:    112 runs, 2.1M tokens, avg 18.7K/file, avg 4.2 turns
  checker:       112 runs, 0.9M tokens, avg 8.0K/file, avg 2.1 turns
  fix:            18 runs, 0.1M tokens, avg 5.6K/file
  scaffold:        1 run,  0.05M tokens
  pkg-checker:     1 run,  0.04M tokens

By complexity:
  trivial (36 files): 0 tokens (handled inline)
  simple  (63 files): 1.2M tokens, avg 19.0K/file
  complex (34 files): 2.0M tokens, avg 58.8K/file

Top 5 most expensive files:
  1. language-model-v3-prompt.ts       — 142K tokens (422 lines, 3 attempts)
  2. language-model-v2-prompt.ts       — 98K tokens  (218 lines, 2 attempts)
  3. image-model-v3.ts                 — 87K tokens  (110 lines, 2 attempts)
  ...

Top escalation patterns:
  docstring-after-future:    98 occurrences (SUPPRESSED)
  required-field-has-default: 34 occurrences (SUPPRESSED)
  unused-field-import:       12 occurrences (SUPPRESSED)
```

### `--trace <file>` Flag

```bash
uv run translation/translate.py --trace packages/provider/src/errors/ai-sdk-error.ts
```

Output:

```
=== Trace: ai-sdk-error.ts ===

File: packages/provider/src/errors/ai-sdk-error.ts → python/packages/provider/errors/ai_sdk_error.py
Status: done | Complexity: simple | Lines: 62 | Depth: 0

Run History:
  #1  file-agent (sonnet)  attempt=1  success  14.2K tokens  3 turns  22s
  #2  checker   (sonnet)   attempt=1  PASSED   8.1K tokens   2 turns  11s
      Escalations: (none)

Total: 22.3K tokens, 33s
```

## Implementation Order

| Step | What | Effort | Blocked By |
|------|------|--------|-----------|
| 1 | Create schema + `TranslationDB` class | Half day | Nothing |
| 2 | Wire `start_run`/`finish_run` into orchestrator | Half day | Step 1 |
| 3 | Replace `FileQueue` with DB-backed queries | Half day | Step 2 |
| 4 | Add checker verdict + escalation storage | 2 hours | Step 2 |
| 5 | Migration script for existing state | 2 hours | Step 1 |
| 6 | `--stats` and `--trace` CLI | 2 hours | Step 3 |
| 7 | Dynamic escalation suppression | 1 hour | Step 4 |
| 8 | Token counting from SDK or approximation | 2 hours | Step 2 |

Total: ~2.5 days of focused work.

The DB should be implemented **before** the token efficiency improvements from `token-efficiency.md`, because the DB gives you the measurement infrastructure to validate that the optimizations actually work.

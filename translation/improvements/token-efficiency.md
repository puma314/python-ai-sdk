# Token Efficiency Improvements

## Problem

The translation system burns tokens at a rate that scales poorly. For the `provider` package (133 files), conservative estimates put total token usage at ~5M+ tokens — roughly 35-45% of which is waste from repeated content, wrong-sized models, and unnecessary agent calls.

Across all 9 packages (~820 files), the inefficiencies compound to an estimated **10-15M wasted tokens**.

## Current Token Budget Per File (Approximate)

| Component | Size | Notes |
|-----------|------|-------|
| `translation-rules.md` | ~7K tokens | Injected into every FileAgent + CheckerAgent |
| `file-agent.md` template | ~1.5K tokens | Has its own comment rules section too |
| `checker-agent.md` template | ~1K tokens | |
| `{{DEPS_CONTEXT}}` | 0.5K–4K tokens | Grows linearly with done files |
| Source file read (tool call) | ~0.1–1K tokens | Agent reads via Read tool |
| Stub file read (tool call) | ~0.1K tokens | Agent reads existing stub |
| Agent output | ~1–3K tokens | Translation + summary |
| **Total per FileAgent call** | **~11–17K tokens** | |
| **Total per CheckerAgent call** | **~9–13K tokens** | |

Multiply by 133 files (each getting both agents): **~2.7M–4M tokens** for `provider` alone.

---

## Improvement 1: Tiered Rules

### What

Split `translation-rules.md` (24,792 bytes, ~7K tokens) into two files:

- `rules-essential.md` (~3K tokens): Naming conventions, import mapping, primitive type mapping, error pattern, basic async patterns, dataclass/Protocol choice, docstring format.
- `rules-reference.md` (full file): Everything, including conditional types, template literal validators, Zod-to-Pydantic details, stream patterns, testing/mocking, etc.

### How

1. Create `prompts/rules-essential.md` with sections 1 (file structure), 2 (primitive types + undefined/None only), 4 (error hierarchy), 7 (naming), 8 (imports), 11 (interfaces — just the decision rule), 14 (comments — condensed to 10 lines).
2. Create `prompts/rules-reference.md` as the current full file (renamed).
3. In `translate.py`, classify files by complexity (see Improvement 3) and select the appropriate rules file.

### Savings

~60% of files are simple enough for essential rules only. Saves ~4K tokens × ~80 files = **~320K input tokens** per package.

### Prerequisite

Improvement 3 (file complexity classification).

---

## Improvement 2: Scoped Dependency Context

### What

Replace the full done-files list in `{{DEPS_CONTEXT}}` with only the files that the current file actually imports.

### Current Behavior

```python
def get_dependency_context(f: FileState, queue: FileQueue) -> str:
    done = queue.done_files()  # ALL done files
    if not done:
        return "No files have been translated yet."
    return "\n".join(f"- {d.source_path} → {d.target_path}" for d in done)
```

By file #100 this is 13,421 chars (~3.5K tokens) of lines the agent doesn't need.

### New Behavior

```python
def get_dependency_context(f: FileState, queue: FileQueue) -> str:
    # Only include files this file actually imports
    relevant = []
    for dep_path in f.dependencies:
        dep_file = queue._files.get(dep_path)
        if dep_file and dep_file.status == "done":
            relevant.append(dep_file)

    if not relevant:
        return "No dependencies have been translated yet. This file has no intra-package imports."

    total_done = len(queue.done_files())
    total = len(queue._files)
    lines = [f"Progress: {total_done}/{total} files translated."]
    lines.append("Direct dependencies (already translated):")
    for d in relevant:
        lines.append(f"- {d.source_path} → {d.target_path}")
    return "\n".join(lines)
```

### Savings

Average file has 2-3 deps. Reduces deps_context from ~3.5K tokens (late in the run) to ~200 tokens. Over 133 files: **~300K input tokens saved**.

### Risk

Low. The agent only needs to know import paths for files it references. If it needs the full picture, it can use Glob.

---

## Improvement 3: File Complexity Classification + Model Routing

### What

Classify each file before spawning an agent. Route trivial files to no agent at all, simple files to Sonnet, and complex files to Opus.

### Classification Rules

```python
def classify_file(source_path: str) -> str:
    """Returns 'trivial', 'simple', or 'complex'."""
    content = (ROOT / source_path).read_text()
    lines = [l for l in content.strip().splitlines() if l.strip()]
    non_blank = len(lines)

    # Trivial: barrel files (only re-exports), single type alias, empty index
    is_barrel = all(
        l.strip().startswith(("export ", "export{", "//", "/*", "*/", "*"))
        for l in lines
    )
    if is_barrel or non_blank <= 5:
        return "trivial"

    # Complex: large files, files with class bodies, async functions, generics
    has_class = any("class " in l for l in lines)
    has_async = any("async " in l for l in lines)
    has_generic = any(("<" in l and ">" in l and "extends" in l) for l in lines)

    if non_blank > 80 or (has_class and has_async) or has_generic:
        return "complex"

    return "simple"
```

### Routing

| Complexity | Agent | Model | Rules | Max Turns |
|-----------|-------|-------|-------|-----------|
| trivial | None — generate inline | N/A | N/A | 0 |
| simple | FileAgent | sonnet | rules-essential | 15 |
| complex | FileAgent | opus | rules-reference (full) | 30 |

### Trivial File Handling (No Agent)

For barrel files (`index.ts` with only re-exports), generate `__init__.py` directly in the orchestrator:

```python
def translate_barrel_file(f: FileState) -> None:
    """Translate a trivial barrel file without spawning an agent."""
    content = (ROOT / f.source_path).read_text()

    imports = []
    for line in content.splitlines():
        # Match: export { Foo } from './bar'
        m = re.match(r"export\s+(?:type\s+)?\{\s*(.+?)\s*\}\s+from\s+'(\./[^']+)'", line)
        if m:
            names = [n.strip().split(" as ")[-1] for n in m.group(1).split(",")]
            module = kebab_to_snake(m.group(2).removeprefix("./").removesuffix("/index"))
            for name in names:
                imports.append(f"from .{module} import {name}")

        # Match: export * from './bar'
        m2 = re.match(r"export\s+\*\s+from\s+'(\./[^']+)'", line)
        if m2:
            module = kebab_to_snake(m2.group(1).removeprefix("./").removesuffix("/index"))
            imports.append(f"from .{module} import *")

    py_content = "from __future__ import annotations\n\n"
    py_content += "\n".join(sorted(set(imports))) + "\n"
    (ROOT / f.target_path).parent.mkdir(parents=True, exist_ok=True)
    (ROOT / f.target_path).write_text(py_content)
```

### Savings

- 36 trivial files skip agents entirely: **~500K tokens saved**
- ~60 simple files use Sonnet instead of Opus: Sonnet is ~5x cheaper per token, and the prompts are smaller. Effective savings: **~400K tokens equivalent cost**.

---

## Improvement 4: Pre-Inject Source Content

### What

Read the source file and (optionally) the stub file in the orchestrator and inject their contents directly into the prompt, eliminating the agent's first 1-2 tool-call round trips.

### Current Flow

```
Orchestrator → spawns FileAgent
  FileAgent turn 1: thinks "let me read the source"
  FileAgent turn 1: calls Read(source_path) → gets content
  FileAgent turn 2: calls Read(target_path) → gets stub
  FileAgent turn 3: calls Write(target_path) → writes translation
  FileAgent turn 4: summary text
```

### New Flow

Add `{{SOURCE_CONTENT}}` and `{{STUB_CONTENT}}` to the file-agent prompt template:

```markdown
## Source File Content

```typescript
{{SOURCE_CONTENT}}
```

## Current Target File

```python
{{STUB_CONTENT}}
```
```

The agent can now translate immediately on turn 1 (Write call), turn 2 (summary). Saves 2 round trips.

### Template Change in `run_file_agent`

```python
source_content = (ROOT / f.source_path).read_text(encoding="utf-8")
stub_content = (ROOT / f.target_path).read_text(encoding="utf-8") if (ROOT / f.target_path).exists() else ""

system_prompt = (
    agent_template
    .replace("{{RULES}}", rules)
    .replace("{{SOURCE_PATH}}", f.source_path)
    .replace("{{TARGET_PATH}}", f.target_path)
    .replace("{{DEPS_CONTEXT}}", deps_context)
    .replace("{{FEEDBACK}}", feedback)
    .replace("{{SOURCE_CONTENT}}", source_content)
    .replace("{{STUB_CONTENT}}", stub_content)
)
```

### Savings

Eliminates 2 tool-call turns per file. Each turn involves a request/response round trip with the full context window. Estimated **~200K tokens saved** across 133 files (from reduced context re-sending on subsequent turns).

Also apply to the checker: inject both source and target content so the checker doesn't need Read tool calls either. This lets you also drop `Read` from the checker's `allowed_tools`, reducing tool-description token overhead.

---

## Improvement 5: Deduplicate Comment Rules in File Agent Prompt

### What

Remove the "Comment Translation Rules" section (~60 lines) from `file-agent.md`. It duplicates Section 14 of `translation-rules.md` which is already injected via `{{RULES}}`.

### Current Duplication

`file-agent.md` lines 61-131 cover:
- JSDoc → docstrings
- Inline comments
- Block comments
- Module-level documentation
- What NOT to do

`translation-rules.md` Section 14 (lines 623-700) covers the exact same content with the same examples.

### Change

Delete lines 61-131 from `file-agent.md`. Add a one-line reference: "See Translation Rules Section 14 for comment translation guidelines."

### Savings

~1K tokens removed from every FileAgent system prompt. Over 133 files: **~133K input tokens**.

---

## Improvement 6: Known-Acceptable Patterns for Checker

### What

Add a "Known Project Conventions" section to `checker-agent.md` that lists patterns the checker should accept without escalating.

### Motivation

The `escalation.md` file has 210 lines. Roughly 80% are the same complaint repeated per file:
- "Module docstring appears after `from __future__ import annotations`" (100+ instances)
- "Required fields have defaults due to dataclass ordering" (30+ instances)
- "Unused `field` import" (10+ instances)

Each escalation costs output tokens. Worse, some of these get miscategorized as FAILED verdicts, triggering unnecessary retries.

### Change

Add to `checker-agent.md`:

```markdown
## Known Project Conventions (do NOT escalate these)

The following patterns are intentional project-wide decisions. Do not report them as escalations or failures:

1. Module docstring after `from __future__ import annotations` — this is the project standard. PEP 257 tension is known and accepted.
2. Required TS fields getting default values in Python dataclasses when a discriminator `type` field has a default — this is a necessary Python dataclass ordering workaround.
3. Unused `field` import from `dataclasses` — will be cleaned up in a later pass.
4. Absolute `ai_sdk.provider.*` imports where relative imports could be used — accepted for now.
```

### Savings

Reduces escalation output by ~80%. Prevents false FAILED verdicts that trigger retries. Estimated **~50K output tokens** + avoided retry costs.

---

## Improvement 7: Lighter Retry Prompts

### What

When retrying a file after checker failure, use a focused "fix" prompt instead of the full translation prompt.

### Current Behavior

Retries call `run_file_agent` with the same full system prompt (~10K+ tokens). The only change is `{{FEEDBACK}}` gets the checker's error. The agent re-reads the source file, re-reads the translation rules, and retranslates from scratch.

### New Behavior

Create a `prompts/fix-agent.md` (~2K tokens) that says:

```markdown
# Translation Fix Agent

You previously translated a TypeScript file to Python, but the checker found issues.

## File
**Target file**: `{{TARGET_PATH}}`

## Current Translation
```python
{{CURRENT_TRANSLATION}}
```

## Checker Feedback
{{FEEDBACK}}

## Rules Reference (relevant sections only)
{{RELEVANT_RULES}}

## Instructions
1. Read the checker feedback carefully
2. Fix ONLY the issues identified — do not rewrite the entire file
3. Write the corrected file to `{{TARGET_PATH}}`
```

### Implementation

```python
async def run_fix_agent(f: FileState, pkg: str) -> tuple[FileState, bool, str | None]:
    current = (ROOT / f.target_path).read_text()
    feedback = f.last_error or "No specific feedback."

    fix_template = load_prompt("fix-agent.md")
    system_prompt = (
        fix_template
        .replace("{{TARGET_PATH}}", f.target_path)
        .replace("{{CURRENT_TRANSLATION}}", current)
        .replace("{{FEEDBACK}}", feedback)
        .replace("{{RELEVANT_RULES}}", extract_relevant_rules(feedback))
    )
    # Use sonnet for fixes — they're targeted edits, not full translations
    ...
```

### Savings

Retry prompts go from ~12K tokens to ~4K tokens. Uses Sonnet instead of Opus. With ~18 retries in the provider package: **~100K tokens saved**.

---

## Implementation Order

| Priority | Improvement | Effort | Tokens Saved | Dependencies |
|----------|------------|--------|-------------|-------------|
| 1 | Scoped deps_context (#2) | Low | ~300K | None |
| 2 | Deduplicate comment rules (#5) | Trivial | ~133K | None |
| 3 | Known patterns for checker (#6) | Low | ~50K + retries | None |
| 4 | Pre-inject source content (#4) | Low | ~200K | None |
| 5 | File complexity + model routing (#3) | Medium | ~900K | None |
| 6 | Tiered rules (#1) | Medium | ~320K | #3 |
| 7 | Lighter retry prompts (#7) | Medium | ~100K | None |

Items 1-4 can be done in an hour. Items 5-7 are a half-day of work.

Total estimated savings: **~2M tokens per package** (~35-45% reduction).

---

## Measuring Impact

After implementing, compare:
- Total tokens per file (requires Improvement from `state-management.md` — token tracking in the DB)
- Retry rate (should drop with #6)
- Time per file (fewer round trips from #4)
- Cost per package (aggregate from DB)

The state management DB (see `state-management.md`) is the best way to measure these improvements rigorously. Without it, you're comparing log file sizes manually.

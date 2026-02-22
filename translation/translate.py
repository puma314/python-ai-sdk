"""TypeScript → Python Translation Orchestrator.

Uses the Claude Agent SDK to translate TypeScript packages from the Vercel AI SDK
into idiomatic Python. Processes packages sequentially, running four agent types
per package: ScaffoldAgent → FileAgents (parallel) → CheckerAgents (parallel) → PackageCheckerAgent.

Usage:
    uv run translation/translate.py --packages provider,provider-utils --concurrency 5
    uv run translation/translate.py --packages provider --resume
    uv run translation/translate.py --packages provider --dry-run
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from claude_agent_sdk import ClaudeAgentOptions, query

# ---------------------------------------------------------------------------
# Monkey-patch: handle unknown message types (e.g. rate_limit_event) gracefully
# ---------------------------------------------------------------------------

import claude_agent_sdk._internal.message_parser as _mp
import claude_agent_sdk._internal.client as _client

_original_parse_message = _mp.parse_message


def _patched_parse_message(data: dict) -> Any:
    """Wrap parse_message to return None for unknown message types instead of raising."""
    try:
        return _original_parse_message(data)
    except Exception as e:
        if "Unknown message type" in str(e):
            return None  # skip unknown messages
        raise


_mp.parse_message = _patched_parse_message  # type: ignore[assignment]
# Also patch the import in client.py which may have already imported it
_client.parse_message = _patched_parse_message  # type: ignore[assignment]


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT / "translation" / "prompts"
STATE_DIR = ROOT / "translation" / "state"
LOGS_DIR = ROOT / "translation" / "logs"

EXCLUDE_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\.test\.ts$"),
    re.compile(r"\.test-d\.ts$"),
    re.compile(r"\.tsx$"),
    re.compile(r"tsup\.config\.ts$"),
    re.compile(r"tsconfig.*\.json$"),
    re.compile(r"vitest\..+\.config\.(js|ts)$"),
    re.compile(r"package\.json$"),
    re.compile(r"package-lock\.json$"),
    re.compile(r"\.eslintrc"),
    re.compile(r"\.prettierrc"),
    re.compile(r"turbo\.json$"),
    re.compile(r"README\.md$"),
    re.compile(r"CHANGELOG\.md$"),
    re.compile(r"AGENTS\.md$"),
    re.compile(r"\.d\.ts$"),
    re.compile(r"__snapshots__/"),
    re.compile(r"node_modules/"),
    re.compile(r"dist/"),
    re.compile(r"\.turbo/"),
]


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------


@dataclass
class Config:
    packages: list[str] = field(default_factory=list)
    concurrency: int = 5
    max_retries: int = 2
    resume: bool = False
    dry_run: bool = False


def parse_args() -> Config:
    parser = argparse.ArgumentParser(description="TS→Python Translation Orchestrator")
    parser.add_argument(
        "--packages",
        required=True,
        help="Comma-separated list of packages to translate (e.g. provider,provider-utils)",
    )
    parser.add_argument("--concurrency", type=int, default=5, help="Parallel FileAgents (default: 5)")
    parser.add_argument("--max-retries", type=int, default=2, help="Max retries per file (default: 2)")
    parser.add_argument("--resume", action="store_true", help="Resume from saved state")
    parser.add_argument("--dry-run", action="store_true", help="Show file discovery without translating")

    args = parser.parse_args()
    return Config(
        packages=[p.strip() for p in args.packages.split(",")],
        concurrency=args.concurrency,
        max_retries=args.max_retries,
        resume=args.resume,
        dry_run=args.dry_run,
    )


# ---------------------------------------------------------------------------
# Path Utilities
# ---------------------------------------------------------------------------


def kebab_to_snake(name: str) -> str:
    return name.replace("-", "_")


def ts_path_to_py_path(ts_path: str) -> str:
    """Convert a TS source path to its Python target path.

    Example:
        packages/provider/src/errors/ai-sdk-error.ts
        → python/packages/provider/errors/ai_sdk_error.py
    """
    parts = ts_path.split("/")

    # Replace packages/ prefix with python/packages/
    if parts[0] == "packages":
        parts[0] = "python/packages"

    # Remove 'src' segment
    if "src" in parts:
        parts.remove("src")

    # Convert kebab-case segments to snake_case
    parts = [kebab_to_snake(p) for p in parts]

    # Convert extension
    last = parts[-1]
    if last == "index.ts":
        parts[-1] = "__init__.py"
    elif last.endswith(".ts"):
        parts[-1] = last.removesuffix(".ts") + ".py"

    return "/".join(parts)


def python_package_name(pkg: str) -> str:
    return kebab_to_snake(pkg)


def python_package_dot_path(pkg: str) -> str:
    return kebab_to_snake(pkg)


# ---------------------------------------------------------------------------
# File State
# ---------------------------------------------------------------------------


@dataclass
class FileState:
    source_path: str
    target_path: str
    status: str = "pending"  # pending | in-progress | done | failed | skipped
    attempts: int = 0
    last_error: str | None = None
    dependencies: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# File Discovery & Dependency Graph
# ---------------------------------------------------------------------------


def discover_source_files(package_path: str) -> list[str]:
    """Walk the package's src/ directory and return all translatable .ts files."""
    src_dir = ROOT / package_path / "src"
    if not src_dir.exists():
        print(f"  ERROR: Source directory not found: {src_dir}", file=sys.stderr)
        return []

    files: list[str] = []

    def walk(directory: Path) -> None:
        for entry in sorted(directory.iterdir()):
            rel = str(entry.relative_to(ROOT))
            if entry.is_dir():
                if entry.name in ("node_modules", "dist", ".turbo", "__snapshots__"):
                    continue
                walk(entry)
            elif entry.suffix in (".ts", ".tsx"):
                if not any(pat.search(rel) for pat in EXCLUDE_PATTERNS):
                    files.append(rel)

    walk(src_dir)

    # Also check internal/ and test/ at package root
    for subdir in ("internal", "test"):
        subdir_path = ROOT / package_path / subdir
        if subdir_path.exists():
            walk(subdir_path)

    return files


def extract_imports(file_path: str) -> list[str]:
    """Extract relative import paths from a TypeScript file."""
    full_path = ROOT / file_path
    if not full_path.exists():
        return []

    content = full_path.read_text(encoding="utf-8")
    imports: list[str] = []

    # Match: import ... from './relative-path' or export ... from '../relative-path'
    import_re = re.compile(r"""(?:import|export)\s+.*?\s+from\s+['"](\.\./?\S*?|\.\/\S*?)['"]""")

    for match in import_re.finditer(content):
        import_path = match.group(1)
        file_dir = str(Path(file_path).parent)
        resolved = os.path.normpath(os.path.join(file_dir, import_path))

        # Try to resolve to an actual file
        if not resolved.endswith((".ts", ".tsx")):
            index_path = os.path.join(resolved, "index.ts")
            ts_path = resolved + ".ts"
            tsx_path = resolved + ".tsx"
            if (ROOT / index_path).exists():
                resolved = index_path
            elif (ROOT / ts_path).exists():
                resolved = ts_path
            elif (ROOT / tsx_path).exists():
                resolved = tsx_path

        imports.append(resolved)

    return imports


@dataclass
class DepInfo:
    deps: list[str]
    depth: int


def build_dependency_graph(package_path: str) -> dict[str, DepInfo]:
    """Build a file-level dependency graph with topological depth."""
    source_files = discover_source_files(package_path)
    source_set = set(source_files)

    # Build adjacency list
    deps_map: dict[str, list[str]] = {}
    for f in source_files:
        file_imports = [imp for imp in extract_imports(f) if imp in source_set]
        deps_map[f] = file_imports

    # Compute depth via Kahn's algorithm
    in_degree: dict[str, int] = {f: 0 for f in source_files}
    reverse_deps: dict[str, list[str]] = {f: [] for f in source_files}

    for f, f_deps in deps_map.items():
        for dep in f_deps:
            if dep in in_degree:
                in_degree[f] = in_degree.get(f, 0) + 1
                reverse_deps[dep].append(f)

    depth: dict[str, int] = {}
    queue: list[str] = []

    for f, deg in in_degree.items():
        if deg == 0:
            queue.append(f)
            depth[f] = 0

    head = 0
    while head < len(queue):
        current = queue[head]
        head += 1
        current_depth = depth.get(current, 0)

        for dependent in reverse_deps.get(current, []):
            new_in = in_degree.get(dependent, 1) - 1
            in_degree[dependent] = new_in
            depth[dependent] = max(depth.get(dependent, 0), current_depth + 1)
            if new_in == 0:
                queue.append(dependent)

    # Handle cycles: assign max depth
    max_depth = max(depth.values(), default=0) + 1
    for f in source_files:
        if f not in depth:
            depth[f] = max_depth

    return {
        f: DepInfo(deps=deps_map.get(f, []), depth=depth.get(f, 0))
        for f in source_files
    }


# ---------------------------------------------------------------------------
# File Queue
# ---------------------------------------------------------------------------


class FileQueue:
    def __init__(self, graph: dict[str, DepInfo]) -> None:
        self._files: dict[str, FileState] = {}

        # Sort by depth for initial ordering
        sorted_files = sorted(graph.items(), key=lambda item: item[1].depth)

        for source_path, info in sorted_files:
            self._files[source_path] = FileState(
                source_path=source_path,
                target_path=ts_path_to_py_path(source_path),
                dependencies=info.deps,
            )

    def has_work(self) -> bool:
        return any(f.status in ("pending", "in-progress") for f in self._files.values())

    def is_deadlocked(self) -> bool:
        for f in self._files.values():
            if f.status != "pending":
                continue
            has_blocking_failure = any(
                self._files.get(dep) is not None and self._files[dep].status == "failed"
                for dep in f.dependencies
            )
            if not has_blocking_failure:
                return False
        return True

    def get_ready_batch(self, max_size: int) -> list[FileState]:
        batch: list[FileState] = []
        for f in self._files.values():
            if len(batch) >= max_size:
                break
            if f.status != "pending":
                continue
            all_deps_done = all(
                (dep not in self._files) or self._files[dep].status == "done"
                for dep in f.dependencies
            )
            if all_deps_done:
                batch.append(f)
        return batch

    def mark_in_progress(self, f: FileState) -> None:
        f.status = "in-progress"
        f.attempts += 1

    def mark_done(self, f: FileState) -> None:
        f.status = "done"

    def mark_failed(self, f: FileState, error: str | None = None) -> None:
        f.status = "failed"
        f.last_error = error

    def mark_pending(self, f: FileState) -> None:
        f.status = "pending"

    def get_summary(self) -> str:
        total = done = failed = pending = in_progress = 0
        for f in self._files.values():
            total += 1
            match f.status:
                case "done":
                    done += 1
                case "failed":
                    failed += 1
                case "pending":
                    pending += 1
                case "in-progress":
                    in_progress += 1
        return f"  Progress: {done}/{total} done, {failed} failed, {pending} pending, {in_progress} in-progress"

    def done_files(self) -> list[FileState]:
        return [f for f in self._files.values() if f.status == "done"]

    def failed_files(self) -> list[FileState]:
        return [f for f in self._files.values() if f.status == "failed"]

    def save_state(self, pkg: str) -> None:
        state = {
            "package": pkg,
            "files": {
                key: {
                    "target_path": f.target_path,
                    "status": f.status,
                    "attempts": f.attempts,
                    "last_error": f.last_error,
                    "dependencies": f.dependencies,
                }
                for key, f in self._files.items()
            },
            "summary": {
                "total": len(self._files),
                "done": sum(1 for f in self._files.values() if f.status == "done"),
                "failed": sum(1 for f in self._files.values() if f.status == "failed"),
            },
        }
        state_path = STATE_DIR / f"{python_package_name(pkg)}.json"
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps(state, indent=2))

    def load_state(self, pkg: str) -> bool:
        state_path = STATE_DIR / f"{python_package_name(pkg)}.json"
        if not state_path.exists():
            return False
        try:
            state = json.loads(state_path.read_text())
            restored = 0
            for key, saved in state.get("files", {}).items():
                existing = self._files.get(key)
                if existing and saved.get("status") == "done":
                    existing.status = "done"
                    existing.attempts = saved.get("attempts", 1)
                    restored += 1
            print(f"  Resumed state: {restored} files already done")
            return True
        except (json.JSONDecodeError, KeyError) as e:
            print(f"  Warning: could not parse state file: {e}", file=sys.stderr)
            return False


# ---------------------------------------------------------------------------
# Prompt Loading
# ---------------------------------------------------------------------------


def load_prompt(name: str) -> str:
    prompt_path = PROMPTS_DIR / name
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    return prompt_path.read_text(encoding="utf-8")


def get_dependency_context(f: FileState, queue: FileQueue) -> str:
    done = queue.done_files()
    if not done:
        return "No files have been translated yet."
    return "\n".join(f"- {d.source_path} → {d.target_path}" for d in done)


# ---------------------------------------------------------------------------
# Logging Helpers
# ---------------------------------------------------------------------------

# Main orchestrator logger
logger = logging.getLogger("translate")


def setup_logging() -> None:
    """Set up logging for the orchestrator and create log directories."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    log_file = LOGS_DIR / f"orchestrator_{timestamp}.log"

    # File handler for detailed logs
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
    )

    # Console handler for summary output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter("%(message)s"))

    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info(f"Logs: {log_file}")


def agent_log_path(agent_type: str, label: str) -> Path:
    """Create a log file path for a sub-agent run.

    Creates: translation/logs/<agent_type>/<label>_<timestamp>.log
    """
    agent_dir = LOGS_DIR / agent_type
    agent_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    # Sanitize label for filesystem
    safe_label = re.sub(r"[^\w\-.]", "_", label)[:80]
    return agent_dir / f"{safe_label}_{timestamp}.log"


# ---------------------------------------------------------------------------
# Agent Helpers
# ---------------------------------------------------------------------------


async def collect_result(
    query_iter: Any,
    log_file: Path | None = None,
) -> tuple[str, bool, Any]:
    """Drain an agent query iterator and return (result_text, is_error, structured_output).

    If log_file is provided, writes all agent messages to it.
    Handles unknown message types gracefully (e.g. rate_limit_event).
    """
    from claude_agent_sdk import ResultMessage

    fh = None
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        fh = open(log_file, "w", encoding="utf-8")  # noqa: SIM115
        fh.write(f"=== Agent log started at {datetime.now(timezone.utc).isoformat()} ===\n\n")

    last_result = ""
    is_error = False
    structured_output = None
    try:
        async for message in query_iter:
            # Skip None messages (from patched parser handling unknown types)
            if message is None:
                continue

            if fh:
                msg_type = type(message).__name__
                fh.write(f"[{msg_type}] ")
                if hasattr(message, "result"):
                    fh.write(f"{message.result}\n")
                elif hasattr(message, "content"):
                    fh.write(f"{message.content}\n")
                else:
                    fh.write(f"{message}\n")
                fh.flush()

            if isinstance(message, ResultMessage):
                last_result = message.result or ""
                is_error = message.is_error
                if hasattr(message, "structured_output"):
                    structured_output = message.structured_output
    finally:
        if fh:
            fh.write(f"\n=== Agent log ended at {datetime.now(timezone.utc).isoformat()} ===\n")
            fh.write(f"Result: {'ERROR' if is_error else 'OK'}\n")
            if structured_output is not None:
                fh.write(f"Structured output: {json.dumps(structured_output)}\n")
            fh.close()

    return last_result, is_error, structured_output


def git_commit(message: str, paths: list[str]) -> bool:
    """Stage the given paths and create a git commit. Returns True on success."""
    try:
        # Stage specific paths
        subprocess.run(
            ["git", "add", *paths],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )

        # Check if there's anything staged to commit
        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=ROOT,
            capture_output=True,
        )
        if result.returncode == 0:
            # Nothing staged — skip
            logger.debug("  [Git] Nothing to commit, skipping.")
            return True

        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )
        logger.info(f"  [Git] Committed: {message}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"  [Git] Commit failed: {e.stderr.decode().strip()}")
        return False


# ---------------------------------------------------------------------------
# Agent Runners
# ---------------------------------------------------------------------------


async def run_scaffold_agent(pkg: str) -> None:
    log_file = agent_log_path("scaffold", pkg)
    logger.info(f"  [Scaffold] Starting for packages/{pkg}... (log: {log_file})")

    scaffold_prompt = load_prompt("scaffold-agent.md")

    result, is_error, _ = await collect_result(
        query(
            prompt=f"Scaffold the package: packages/{pkg}",
            options=ClaudeAgentOptions(
                system_prompt=scaffold_prompt,
                allowed_tools=["Read", "Write", "Glob", "Bash", "Grep"],
                model="sonnet",
                permission_mode="bypassPermissions",
                cwd=str(ROOT),
                max_turns=40,
            ),
        ),
        log_file=log_file,
    )

    if is_error:
        logger.error(f"  [Scaffold] Failed: {result}")
        raise RuntimeError(f"Scaffold agent failed for {pkg}: {result}")

    logger.info("  [Scaffold] Complete.")


async def run_file_agent(f: FileState, pkg: str, queue: FileQueue) -> tuple[FileState, bool, str | None]:
    """Translate a single file. Returns (file, success, error_or_none)."""
    # Use the source filename (without extension) as log label
    src_name = Path(f.source_path).stem
    log_file = agent_log_path("file-agent", f"{pkg}__{src_name}")
    logger.info(f"  [FileAgent] Translating {f.source_path}... (log: {log_file})")

    rules = load_prompt("translation-rules.md")
    agent_template = load_prompt("file-agent.md")
    deps_context = get_dependency_context(f, queue)
    feedback = f.last_error or "None — this is the first attempt."

    system_prompt = (
        agent_template
        .replace("{{RULES}}", rules)
        .replace("{{SOURCE_PATH}}", f.source_path)
        .replace("{{TARGET_PATH}}", f.target_path)
        .replace("{{DEPS_CONTEXT}}", deps_context)
        .replace("{{FEEDBACK}}", feedback)
    )

    try:
        result, is_error, _ = await collect_result(
            query(
                prompt=f"Translate {f.source_path} to Python at {f.target_path}",
                options=ClaudeAgentOptions(
                    system_prompt=system_prompt,
                    allowed_tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep"],
                    model="opus",
                    permission_mode="bypassPermissions",
                    cwd=str(ROOT),
                    max_turns=30,
                ),
            ),
            log_file=log_file,
        )
        if is_error:
            return f, False, result
        return f, True, None
    except Exception as e:
        logger.error(f"  [FileAgent] Exception translating {f.source_path}: {e}")
        return f, False, str(e)


CHECKER_OUTPUT_SCHEMA = {
    "type": "json_schema",
    "schema": {
        "type": "object",
        "properties": {
            "verdict": {
                "type": "string",
                "enum": ["PASSED", "FAILED"],
                "description": "Whether the translation passed or failed validation.",
            },
            "failures": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of blocking issues (empty if verdict is PASSED).",
            },
            "escalations": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Non-blocking style notes for escalation.md (may be empty).",
            },
        },
        "required": ["verdict", "failures", "escalations"],
        "additionalProperties": False,
    },
}


async def run_checker_agent(f: FileState, pkg: str) -> tuple[FileState, bool, str | None]:
    """Validate a translated file. Returns (file, passed, feedback_or_none)."""
    src_name = Path(f.source_path).stem
    log_file = agent_log_path("checker", f"{pkg}__{src_name}")
    logger.info(f"  [Checker] Validating {f.target_path}... (log: {log_file})")

    rules = load_prompt("translation-rules.md")
    checker_template = load_prompt("checker-agent.md")

    system_prompt = (
        checker_template
        .replace("{{RULES}}", rules)
        .replace("{{SOURCE_PATH}}", f.source_path)
        .replace("{{TARGET_PATH}}", f.target_path)
    )

    try:
        result, is_error, structured = await collect_result(
            query(
                prompt=f"Check the translated Python file at {f.target_path} against source {f.source_path}",
                options=ClaudeAgentOptions(
                    system_prompt=system_prompt,
                    allowed_tools=["Read", "Glob", "Grep", "Bash"],
                    model="sonnet",
                    permission_mode="bypassPermissions",
                    cwd=str(ROOT),
                    max_turns=15,
                    output_format=CHECKER_OUTPUT_SCHEMA,
                ),
            ),
            log_file=log_file,
        )
        if is_error:
            logger.warning(f"  [Checker] Agent error for {f.target_path}, treating as pass")
            return f, True, None

        # Use structured output if available
        if structured and isinstance(structured, dict):
            verdict = structured.get("verdict", "")
            passed = verdict == "PASSED"
            # Write escalation notes if any
            escalations = structured.get("escalations", [])
            if escalations:
                esc_path = STATE_DIR / "escalation.md"
                with open(esc_path, "a", encoding="utf-8") as ef:
                    for note in escalations:
                        ef.write(f"[{f.target_path}] {note}\n")
            if passed:
                return f, True, None
            failures = structured.get("failures", [])
            feedback = "\n".join(failures) if failures else result
            return f, False, feedback

        # Fallback: parse text result if structured output unavailable
        clean = result.replace("```", "").strip()
        has_passed = "\nPASSED" in f"\n{clean}" or clean.startswith("PASSED")
        has_failed = "\nFAILED" in f"\n{clean}" or clean.startswith("FAILED")
        if has_passed and has_failed:
            passed = clean.rfind("PASSED") > clean.rfind("FAILED")
        elif has_passed:
            passed = True
        else:
            passed = False
        return f, passed, None if passed else result
    except Exception as e:
        logger.warning(f"  [Checker] Exception for {f.target_path}: {e}")
        return f, True, None  # checker failure shouldn't block translation


async def run_package_checker_agent(pkg: str) -> None:
    log_file = agent_log_path("package-checker", pkg)
    logger.info(f"  [PackageChecker] Running holistic check on {pkg}... (log: {log_file})")

    checker_template = load_prompt("package-checker-agent.md")
    py_pkg = python_package_name(pkg)
    py_pkg_dot = python_package_dot_path(pkg)

    system_prompt = (
        checker_template
        .replace("{{PACKAGE}}", pkg)
        .replace("{{PYTHON_PACKAGE}}", py_pkg)
        .replace("{{PYTHON_PACKAGE_DOT}}", py_pkg_dot)
    )

    try:
        result, is_error, _ = await collect_result(
            query(
                prompt=f"Run holistic package check on python/packages/{py_pkg} (translated from packages/{pkg})",
                options=ClaudeAgentOptions(
                    system_prompt=system_prompt,
                    allowed_tools=["Read", "Glob", "Grep", "Bash"],
                    model="opus",
                    permission_mode="bypassPermissions",
                    cwd=str(ROOT),
                    max_turns=20,
                ),
            ),
            log_file=log_file,
        )
        if is_error:
            logger.error(f"  [PackageChecker] Agent error: {result}")
        else:
            logger.info(f"  [PackageChecker] Result:\n{result}")
    except Exception as e:
        logger.error(f"  [PackageChecker] Exception: {e}")


# ---------------------------------------------------------------------------
# Dry Run
# ---------------------------------------------------------------------------


def dry_run(package_path: str) -> None:
    print(f"\n=== Dry Run: {package_path} ===\n")

    graph = build_dependency_graph(package_path)
    print(f"Files discovered: {len(graph)}")
    print("\nDependency-ordered file list:\n")

    sorted_files = sorted(graph.items(), key=lambda item: item[1].depth)
    for source_path, info in sorted_files:
        target = ts_path_to_py_path(source_path)
        dep_str = ""
        if info.deps:
            dep_names = [os.path.basename(d) for d in info.deps]
            dep_str = f" (depends on: {', '.join(dep_names)})"
        print(f"  [depth={info.depth}] {source_path} → {target}{dep_str}")

    # Wave breakdown
    waves: dict[int, list[str]] = {}
    for source_path, info in sorted_files:
        waves.setdefault(info.depth, []).append(source_path)

    print("\nTranslation waves:")
    for depth in sorted(waves):
        print(f"  Wave {depth}: {len(waves[depth])} files")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


async def main() -> None:
    config = parse_args()

    # Skip logging setup for dry-run (just uses print)
    if not config.dry_run:
        setup_logging()

    logger.info("Translation Orchestrator")
    logger.info(f"  Packages: {', '.join(config.packages)}")
    logger.info(f"  Concurrency: {config.concurrency}")
    logger.info(f"  Max retries: {config.max_retries}")
    logger.info(f"  Resume: {config.resume}")
    logger.info(f"  Dry run: {config.dry_run}")

    STATE_DIR.mkdir(parents=True, exist_ok=True)

    for pkg in config.packages:
        logger.info(f"\n{'=' * 60}")
        logger.info(f"  Package: {pkg}")
        logger.info(f"{'=' * 60}")

        src_dir = ROOT / "packages" / pkg / "src"
        if not src_dir.exists():
            logger.error(f"  ERROR: Source directory not found: {src_dir}")
            continue

        # Dry run mode
        if config.dry_run:
            dry_run(f"packages/{pkg}")
            continue

        # Phase 1: Scaffold
        logger.info("\n  Phase 1: Scaffolding...")
        await run_scaffold_agent(pkg)

        # Phase 2: Build dependency graph
        logger.info("\n  Phase 2: Building dependency graph...")
        graph = build_dependency_graph(f"packages/{pkg}")
        queue = FileQueue(graph)

        if config.resume:
            queue.load_state(pkg)

        logger.info(f"  Files to translate: {len(graph)}")

        # Phase 3: Translation loop
        logger.info("\n  Phase 3: Translating files...")
        iteration = 0

        while queue.has_work():
            iteration += 1
            batch = queue.get_ready_batch(config.concurrency)

            if not batch:
                if queue.is_deadlocked():
                    logger.error("  DEADLOCK: Remaining files have failed dependencies.")
                    for f in queue.failed_files():
                        logger.error(f"    {f.source_path}: {f.last_error or 'unknown error'}")
                    break
                await asyncio.sleep(1)
                continue

            logger.info(f"\n  --- Iteration {iteration}: {len(batch)} files ---")

            # Mark batch as in-progress
            for f in batch:
                queue.mark_in_progress(f)

            # Run FileAgents in parallel
            file_results = await asyncio.gather(
                *(run_file_agent(f, pkg, queue) for f in batch)
            )

            # Update queue
            for f, success, error in file_results:
                if success:
                    queue.mark_done(f)
                    logger.info(f"    done  {f.source_path}")
                elif f.attempts < config.max_retries:
                    f.last_error = error
                    queue.mark_pending(f)
                    logger.info(f"    retry {f.source_path} (attempt {f.attempts}/{config.max_retries})")
                else:
                    queue.mark_failed(f, error)
                    logger.error(f"    FAIL  {f.source_path}: {error}")

            # Run CheckerAgents on successful translations
            newly_done = [f for f, success, _ in file_results if success]
            if newly_done:
                logger.info(f"\n  Running checkers on {len(newly_done)} files...")
                check_results = await asyncio.gather(
                    *(run_checker_agent(f, pkg) for f in newly_done)
                )
                for f, passed, feedback in check_results:
                    if not passed:
                        if f.attempts < config.max_retries:
                            f.last_error = feedback
                            queue.mark_pending(f)
                            logger.info(f"    retry {f.target_path} (checker failed)")
                        else:
                            logger.warning(f"    WARN  {f.target_path} (checker failed, max retries reached)")
                    else:
                        logger.info(f"    ok    {f.target_path}")

            # Commit translated files from this batch
            committed_files = [
                f.target_path
                for f, success, _ in file_results
                if success and queue._files[f.source_path].status == "done"
            ]
            if committed_files:
                file_names = ", ".join(os.path.basename(p) for p in committed_files[:5])
                suffix = f" +{len(committed_files) - 5} more" if len(committed_files) > 5 else ""
                git_commit(
                    f"translate({pkg}): batch {iteration} — {len(committed_files)} files ({file_names}{suffix})",
                    committed_files,
                )

            queue.save_state(pkg)
            logger.info(queue.get_summary())

        # Phase 4: Package-level holistic check
        logger.info("\n  Phase 4: Package-level validation...")
        await run_package_checker_agent(pkg)

        # Final summary
        logger.info(f"\n  === Package {pkg} Summary ===")
        logger.info(queue.get_summary())

        failed = queue.failed_files()
        if failed:
            logger.info("\n  Failed files:")
            for f in failed:
                logger.info(f"    - {f.source_path}: {f.last_error or 'unknown error'}")

    logger.info("\nTranslation complete.")


if __name__ == "__main__":
    asyncio.run(main())

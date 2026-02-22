"""Test each sub-agent individually to verify they work.

Usage:
    uv run translation/test_agents.py scaffold
    uv run translation/test_agents.py file
    uv run translation/test_agents.py checker
    uv run translation/test_agents.py package-checker
"""

from __future__ import annotations

import asyncio
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Monkey-patch SDK to handle unknown message types (e.g. rate_limit_event)
# ---------------------------------------------------------------------------

import claude_agent_sdk._internal.message_parser as _mp
import claude_agent_sdk._internal.client as _client

_original_parse_message = _mp.parse_message


def _patched_parse_message(data: dict) -> Any:
    try:
        return _original_parse_message(data)
    except Exception as e:
        if "Unknown message type" in str(e):
            print(f"  [SDK] Skipping unknown message type: {data.get('type', '?')}")
            return None
        raise


_mp.parse_message = _patched_parse_message  # type: ignore[assignment]
_client.parse_message = _patched_parse_message  # type: ignore[assignment]

# ---------------------------------------------------------------------------

from claude_agent_sdk import ClaudeAgentOptions, query, ResultMessage

ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT / "translation" / "prompts"
LOGS_DIR = ROOT / "translation" / "logs" / "test"
LOGS_DIR.mkdir(parents=True, exist_ok=True)


def load_prompt(name: str) -> str:
    return (PROMPTS_DIR / name).read_text(encoding="utf-8")


async def drain(query_iter: Any, label: str) -> tuple[str, bool]:
    """Drain agent messages, printing them live and returning the final result."""
    log_file = LOGS_DIR / f"{label}_{datetime.now(timezone.utc).strftime('%H%M%S')}.log"
    fh = open(log_file, "w", encoding="utf-8")  # noqa: SIM115
    fh.write(f"=== {label} started at {datetime.now(timezone.utc).isoformat()} ===\n\n")

    last_result = ""
    is_error = False
    msg_count = 0

    try:
        async for message in query_iter:
            if message is None:
                continue
            msg_count += 1
            msg_type = type(message).__name__

            # Log to file
            if hasattr(message, "result"):
                fh.write(f"[{msg_type}] {message.result}\n")
            elif hasattr(message, "content"):
                content = message.content
                # Summarize content blocks
                if isinstance(content, list):
                    for block in content:
                        if hasattr(block, "text"):
                            fh.write(f"[{msg_type}:text] {block.text[:200]}\n")
                        elif hasattr(block, "name"):
                            fh.write(f"[{msg_type}:tool_use] {block.name}({str(block.input)[:100]})\n")
                        elif hasattr(block, "tool_use_id"):
                            content_str = str(block.content)[:200] if block.content else ""
                            fh.write(f"[{msg_type}:tool_result] {content_str}\n")
                        elif hasattr(block, "thinking"):
                            fh.write(f"[{msg_type}:thinking] {block.thinking[:100]}...\n")
                else:
                    fh.write(f"[{msg_type}] {str(content)[:200]}\n")
            else:
                fh.write(f"[{msg_type}] {str(message)[:200]}\n")
            fh.flush()

            # Print progress to console
            if isinstance(message, ResultMessage):
                last_result = message.result or ""
                is_error = message.is_error
                print(f"\n  Result (is_error={is_error}): {last_result[:500]}")
            elif msg_count % 5 == 0:
                print(f"  ... {msg_count} messages received", end="\r")

    finally:
        fh.write(f"\n=== ended at {datetime.now(timezone.utc).isoformat()} | messages: {msg_count} ===\n")
        fh.close()

    print(f"\n  Total messages: {msg_count}")
    print(f"  Log: {log_file}")
    return last_result, is_error


# ---------------------------------------------------------------------------
# Test: Scaffold Agent
# ---------------------------------------------------------------------------

async def test_scaffold():
    """Test the scaffold agent on a tiny subset — just the errors/ directory."""
    print("=" * 60)
    print("TEST: Scaffold Agent")
    print("  Target: packages/provider (full scaffold)")
    print("=" * 60)

    prompt = load_prompt("scaffold-agent.md")

    result, is_error = await drain(
        query(
            prompt="Scaffold the package: packages/provider",
            options=ClaudeAgentOptions(
                system_prompt=prompt,
                allowed_tools=["Read", "Write", "Glob", "Bash", "Grep"],
                model="sonnet",
                permission_mode="bypassPermissions",
                cwd=str(ROOT),
                max_turns=40,
            ),
        ),
        label="scaffold_provider",
    )

    if is_error:
        print(f"\n  FAILED: {result}")
    else:
        print("\n  PASSED")
        # Verify some files were created
        provider_dir = ROOT / "python" / "packages" / "provider"
        if provider_dir.exists():
            py_files = list(provider_dir.rglob("*.py"))
            print(f"  Created {len(py_files)} .py files under {provider_dir}")
        else:
            print(f"  WARNING: {provider_dir} does not exist!")

    return not is_error


# ---------------------------------------------------------------------------
# Test: File Agent (single file)
# ---------------------------------------------------------------------------

async def test_file():
    """Test the file agent on a single simple file."""
    print("=" * 60)
    print("TEST: File Agent")
    print("  Source: packages/provider/src/errors/ai-sdk-error.ts")
    print("  Target: python/packages/provider/errors/ai_sdk_error.py")
    print("=" * 60)

    source = "packages/provider/src/errors/ai-sdk-error.ts"
    target = "python/packages/provider/errors/ai_sdk_error.py"

    # Ensure target directory exists
    (ROOT / target).parent.mkdir(parents=True, exist_ok=True)

    rules = load_prompt("translation-rules.md")
    template = load_prompt("file-agent.md")

    system_prompt = (
        template
        .replace("{{RULES}}", rules)
        .replace("{{SOURCE_PATH}}", source)
        .replace("{{TARGET_PATH}}", target)
        .replace("{{DEPS_CONTEXT}}", "No files have been translated yet.")
        .replace("{{FEEDBACK}}", "None — this is the first attempt.")
    )

    result, is_error = await drain(
        query(
            prompt=f"Translate {source} to Python at {target}",
            options=ClaudeAgentOptions(
                system_prompt=system_prompt,
                allowed_tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep"],
                model="opus",
                permission_mode="bypassPermissions",
                cwd=str(ROOT),
                max_turns=30,
            ),
        ),
        label="file_agent_ai_sdk_error",
    )

    if is_error:
        print(f"\n  FAILED: {result}")
    else:
        print("\n  PASSED")
        target_path = ROOT / target
        if target_path.exists():
            content = target_path.read_text()
            lines = content.splitlines()
            print(f"  Output: {len(lines)} lines")
            print(f"  First 5 lines:\n    " + "\n    ".join(lines[:5]))
        else:
            print(f"  WARNING: {target_path} was not created!")

    return not is_error


# ---------------------------------------------------------------------------
# Test: Checker Agent
# ---------------------------------------------------------------------------

async def test_checker():
    """Test the checker agent on a translated file."""
    print("=" * 60)
    print("TEST: Checker Agent")
    print("  Source: packages/provider/src/errors/ai-sdk-error.ts")
    print("  Target: python/packages/provider/errors/ai_sdk_error.py")
    print("=" * 60)

    source = "packages/provider/src/errors/ai-sdk-error.ts"
    target = "python/packages/provider/errors/ai_sdk_error.py"

    # Check target exists
    if not (ROOT / target).exists():
        print("  SKIP: Target file doesn't exist. Run 'file' test first.")
        return False

    rules = load_prompt("translation-rules.md")
    template = load_prompt("checker-agent.md")

    system_prompt = (
        template
        .replace("{{RULES}}", rules)
        .replace("{{SOURCE_PATH}}", source)
        .replace("{{TARGET_PATH}}", target)
    )

    result, is_error = await drain(
        query(
            prompt=f"Check the translated Python file at {target} against source {source}",
            options=ClaudeAgentOptions(
                system_prompt=system_prompt,
                allowed_tools=["Read", "Glob", "Grep", "Bash"],
                model="sonnet",
                permission_mode="bypassPermissions",
                cwd=str(ROOT),
                max_turns=15,
            ),
        ),
        label="checker_ai_sdk_error",
    )

    if is_error:
        print(f"\n  AGENT ERROR: {result}")
    else:
        passed = result.strip().startswith("PASSED")
        print(f"\n  Checker verdict: {'PASSED' if passed else 'FAILED'}")
        if not passed:
            print(f"  Feedback:\n{result[:1000]}")

    return not is_error


# ---------------------------------------------------------------------------
# Test: Package Checker Agent
# ---------------------------------------------------------------------------

async def test_package_checker():
    """Test the package checker on whatever has been translated so far."""
    print("=" * 60)
    print("TEST: Package Checker Agent")
    print("  Package: provider")
    print("=" * 60)

    pkg = "provider"
    py_pkg = "provider"

    # Check target dir exists
    if not (ROOT / "python" / "packages" / py_pkg).exists():
        print("  SKIP: python/packages/provider doesn't exist. Run scaffold first.")
        return False

    template = load_prompt("package-checker-agent.md")

    system_prompt = (
        template
        .replace("{{PACKAGE}}", pkg)
        .replace("{{PYTHON_PACKAGE}}", py_pkg)
        .replace("{{PYTHON_PACKAGE_DOT}}", py_pkg)
    )

    result, is_error = await drain(
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
        label="package_checker_provider",
    )

    if is_error:
        print(f"\n  AGENT ERROR: {result}")
    else:
        print(f"\n  Package checker result:\n{result[:2000]}")

    return not is_error


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

TESTS = {
    "scaffold": test_scaffold,
    "file": test_file,
    "checker": test_checker,
    "package-checker": test_package_checker,
}


async def main():
    if len(sys.argv) < 2 or sys.argv[1] not in TESTS:
        print(f"Usage: uv run translation/test_agents.py <{'|'.join(TESTS.keys())}>")
        sys.exit(1)

    test_name = sys.argv[1]
    print(f"\nRunning test: {test_name}\n")

    success = await TESTS[test_name]()

    print(f"\n{'=' * 60}")
    print(f"  {test_name}: {'PASSED' if success else 'FAILED'}")
    print(f"{'=' * 60}")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())

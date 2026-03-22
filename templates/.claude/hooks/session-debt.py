#!/usr/bin/env python3
"""Session debt tracker: maintains a per-session ledger of errors/warnings.

Hook: PostToolUse on Bash
Behavior: Detects failures and warnings from Bash output, writes to
.flow/session-debt.jsonl. Unlike learnings.jsonl (persistent across sessions),
session-debt.jsonl is cleared at session start and must be resolved before shipping.

The /flow-ship skill checks this ledger and blocks if unresolved items exist.
"""

import fcntl
import json
import os
import re
import sys
from datetime import datetime, timezone


FAILURE_PATTERNS = [
    (r"(?i)\berror\b", "error"),
    (r"FAILED", "error"),
    (r"Traceback", "error"),
    (r"exit code [1-9]", "error"),
    (r"exit status [1-9]", "error"),
    (r"Command failed", "error"),
    (r"CalledProcessError", "error"),
    (r"(?i)\bwarning\b", "warning"),
    (r"(?i)\bdeprecated\b", "warning"),
    (r"(?i)TODO\b", "warning"),
    (r"(?i)FIXME\b", "warning"),
]

# Commands that are informational -- don't track failures from these
IGNORE_COMMANDS = [
    "git status",
    "git diff",
    "git log",
    "git branch",
    "gh issue",
    "gh pr",
    "cat ",
    "ls ",
    "echo ",
    "find ",
    "grep ",
]


def find_main_worktree():
    """Resolve main worktree so all worktrees share one .flow/ directory."""
    import subprocess

    try:
        result = subprocess.run(
            ["git", "worktree", "list", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if line.startswith("worktree "):
                    return line[len("worktree "):]
    except (subprocess.SubprocessError, OSError):
        pass
    hook_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(hook_dir))


def is_ignorable(command):
    """Check if command is informational (not worth tracking failures)."""
    return any(command.strip().startswith(prefix) for prefix in IGNORE_COMMANDS)


def detect_issues(text):
    """Detect errors and warnings in command output. Returns list of (severity, excerpt)."""
    if not text:
        return []
    issues = []
    seen = set()
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped or len(stripped) < 5:
            continue
        for pattern, severity in FAILURE_PATTERNS:
            if re.search(pattern, stripped):
                key = (severity, stripped[:100])
                if key not in seen:
                    seen.add(key)
                    issues.append({"severity": severity, "excerpt": stripped[:200]})
                break
    return issues


def get_session_id():
    """Get or create a session identifier."""
    return os.environ.get("CLAUDE_SESSION_ID", "unknown")


def main():
    try:
        hook_input = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, ValueError):
        return

    tool_name = hook_input.get("tool_name", "")
    if tool_name != "Bash":
        return

    tool_input = hook_input.get("tool_input", {})
    tool_result = hook_input.get("tool_result", {})

    command = tool_input.get("command", "")

    # Skip informational commands
    if is_ignorable(command):
        return

    # Extract result text
    result_text = ""
    if isinstance(tool_result, dict):
        result_text = tool_result.get("stdout", "") + tool_result.get("stderr", "")
        if not result_text:
            result_text = tool_result.get("output", "")
    elif isinstance(tool_result, str):
        result_text = tool_result

    # Detect issues
    issues = detect_issues(result_text)
    if not issues:
        return

    # Write to session-debt.jsonl
    project_root = find_main_worktree()
    flow_dir = os.path.join(project_root, ".flow")
    os.makedirs(flow_dir, exist_ok=True)
    debt_path = os.path.join(flow_dir, "session-debt.jsonl")

    for issue in issues:
        entry = {
            "ts": datetime.now(timezone.utc).astimezone().isoformat(),
            "session_id": get_session_id(),
            "severity": issue["severity"],
            "excerpt": issue["excerpt"],
            "command": command[:300],
            "resolved": False,
            "resolution": None,
        }
        try:
            with open(debt_path, "a") as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                try:
                    f.write(json.dumps(entry) + "\n")
                finally:
                    fcntl.flock(f, fcntl.LOCK_UN)
        except OSError:
            pass


if __name__ == "__main__":
    main()

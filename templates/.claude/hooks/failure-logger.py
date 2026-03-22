#!/usr/bin/env python3
"""Failure logger: captures Bash failures to learnings.jsonl.

Hook: PostToolUse on Bash
Behavior: Checks tool_result for failure indicators. If the command looks
relevant and failed, appends to .flow/learnings.jsonl.
"""

import fcntl
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone


FAILURE_PATTERNS = [
    r"non-zero",
    r"(?i)\berror\b",
    r"FAILED",
    r"Traceback",
    r"exit code [1-9]",
    r"exit status [1-9]",
    r"Command failed",
    r"CalledProcessError",
]


def load_config():
    """Load failure_logger config from patterns.json."""
    patterns_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "patterns.json")
    try:
        with open(patterns_path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


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
    # Fallback: assume hook is in .claude/hooks/ of the project root
    hook_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(hook_dir))


def is_relevant_command(command, relevant_keywords):
    """Check if the command matches any relevant keyword."""
    return any(kw in command for kw in relevant_keywords)


def detect_failure(tool_result):
    """Check if tool_result indicates a failure."""
    if not tool_result:
        return False
    text = tool_result if isinstance(tool_result, str) else str(tool_result)
    return any(re.search(p, text) for p in FAILURE_PATTERNS)


def categorize_command(command, categories):
    """Determine the failure category based on command content."""
    for category, keywords in categories.items():
        if any(kw in command for kw in keywords):
            return category
    return "other"


def extract_module(command):
    """Try to extract a module or package name from the command.

    Customize the regex below to match your project's module naming pattern.
    Examples:
      - Python packages: r"\\b(myapp_\\w+)\\b"
      - Node packages: r"@myorg/(\\w+)"
      - Go packages: r"\\b(cmd|pkg)/(\\w+)"
    """
    # Generic pattern: look for common project path segments
    match = re.search(r"\b(src|lib|packages?|modules?|apps?)/(\w+)", command)
    return match.group(2) if match else None


def extract_error_excerpt(tool_result, max_len=500):
    """Extract the most relevant error lines from output."""
    if not tool_result:
        return ""
    text = tool_result if isinstance(tool_result, str) else str(tool_result)
    # Find lines with error indicators
    error_lines = []
    for line in text.split("\n"):
        if any(re.search(p, line) for p in FAILURE_PATTERNS):
            error_lines.append(line.strip())
    excerpt = "\n".join(error_lines) if error_lines else text[-max_len:]
    return excerpt[:max_len]


def get_session_id():
    """Get or create a session identifier."""
    return os.environ.get("CLAUDE_SESSION_ID", uuid.uuid4().hex[:8])


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
    result_text = ""
    if isinstance(tool_result, dict):
        result_text = tool_result.get("stdout", "") + tool_result.get("stderr", "")
        if not result_text:
            result_text = tool_result.get("output", "")
    elif isinstance(tool_result, str):
        result_text = tool_result

    # Load config
    config = load_config()
    if not config:
        return

    fl_config = config.get("failure_logger", {})
    relevant_keywords = fl_config.get("relevant_commands", [])
    categories = fl_config.get("categories", {})

    # Check relevance
    if not is_relevant_command(command, relevant_keywords):
        return

    # Check for failure
    if not detect_failure(result_text):
        return

    # Build log entry
    entry = {
        "ts": datetime.now(timezone.utc).astimezone().isoformat(),
        "session_id": get_session_id(),
        "type": "bash_failure",
        "category": categorize_command(command, categories),
        "command": command[:500],
        "error_excerpt": extract_error_excerpt(result_text),
        "module": extract_module(command),
        "reflected": False,
    }

    # Write to learnings.jsonl with file locking
    project_root = find_main_worktree()
    flow_dir = os.path.join(project_root, ".flow")
    os.makedirs(flow_dir, exist_ok=True)
    learnings_path = os.path.join(flow_dir, "learnings.jsonl")

    try:
        with open(learnings_path, "a") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                f.write(json.dumps(entry) + "\n")
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)
    except OSError:
        pass  # Don't crash the hook on write failure


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Clear session debt ledger. Called at session start or after manual review."""

import os
import sys


def find_main_worktree():
    """Resolve main worktree."""
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


def main():
    project_root = find_main_worktree()
    debt_path = os.path.join(project_root, ".flow", "session-debt.jsonl")

    if os.path.exists(debt_path):
        os.remove(debt_path)
        print("Session debt ledger cleared.")
    else:
        print("No session debt ledger found.")


if __name__ == "__main__":
    main()

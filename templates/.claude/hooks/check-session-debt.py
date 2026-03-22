#!/usr/bin/env python3
"""Check session debt: reports unresolved errors/warnings before shipping.

Called by /flow-ship to enforce the completion gate.
Exit code 0 = clean, exit code 1 = unresolved debt exists.
Outputs a human-readable summary to stdout.
"""

import json
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

    if not os.path.exists(debt_path):
        print("Session debt: clean (no ledger file)")
        sys.exit(0)

    errors = []
    warnings = []

    with open(debt_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if entry.get("resolved"):
                    continue
                if entry.get("severity") == "error":
                    errors.append(entry)
                else:
                    warnings.append(entry)
            except json.JSONDecodeError:
                continue

    if not errors and not warnings:
        print("Session debt: clean (all items resolved)")
        sys.exit(0)

    print("SESSION DEBT — unresolved items:")
    print()

    if errors:
        print(f"  ERRORS ({len(errors)}):")
        for e in errors[:10]:
            print(f"    - {e['excerpt'][:120]}")
            print(f"      from: {e['command'][:80]}")
        if len(errors) > 10:
            print(f"    ... and {len(errors) - 10} more")
        print()

    if warnings:
        print(f"  WARNINGS ({len(warnings)}):")
        for w in warnings[:10]:
            print(f"    - {w['excerpt'][:120]}")
        if len(warnings) > 10:
            print(f"    ... and {len(warnings) - 10} more")
        print()

    print("Fix these issues or mark them resolved before shipping.")
    print("To clear the ledger: python3 .claude/hooks/clear-session-debt.py")
    sys.exit(1)


if __name__ == "__main__":
    main()

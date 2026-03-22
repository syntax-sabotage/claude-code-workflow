#!/usr/bin/env python3
"""Session context injector: surfaces recent failures on session start.

Hook: SessionStart (matcher: startup|resume)
Behavior: Reads learnings.jsonl, filters unreflected entries, outputs summary.
Also clears the session debt ledger from the previous session.
"""

import json
import os
import sys
from collections import defaultdict


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


def load_unreflected_entries(learnings_path, max_lines=50):
    """Read last N lines and return unreflected entries."""
    try:
        with open(learnings_path) as f:
            lines = f.readlines()
    except FileNotFoundError:
        return []

    entries = []
    for line in lines[-max_lines:]:
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
            if not entry.get("reflected", False):
                entries.append(entry)
        except json.JSONDecodeError:
            continue
    return entries


def clear_session_debt(project_root):
    """Clear session debt ledger at session start -- fresh slate each session."""
    debt_path = os.path.join(project_root, ".flow", "session-debt.jsonl")
    if os.path.exists(debt_path):
        os.remove(debt_path)


def main():
    project_root = find_main_worktree()

    # Clear session debt from previous session
    clear_session_debt(project_root)

    learnings_path = os.path.join(project_root, ".flow", "learnings.jsonl")

    entries = load_unreflected_entries(learnings_path)
    if not entries:
        return  # Silent exit -- no noise

    # Group by category
    by_category = defaultdict(list)
    for entry in entries:
        cat = entry.get("category", "other")
        by_category[cat].append(entry)

    # Build summary
    total = len(entries)
    lines = [f"LEARNINGS CONTEXT: {total} unprocessed failure(s) from recent sessions:"]

    for cat, cat_entries in sorted(by_category.items()):
        modules = set()
        for e in cat_entries:
            m = e.get("module")
            if m:
                modules.add(m)
        count = len(cat_entries)
        mod_str = f" ({', '.join(sorted(modules))})" if modules else ""
        lines.append(f"  - {count} {cat} failure(s){mod_str}")

    lines.append("Consider running /flow-reflect to capture learnings.")

    # Output as system message
    print("\n".join(lines))


if __name__ == "__main__":
    main()

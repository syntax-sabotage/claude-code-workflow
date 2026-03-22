#!/usr/bin/env python3
"""Pre-edit guard: regex anti-pattern detection on Edit/Write operations.

Hook: PreToolUse on Edit|Write
Behavior: Warns but never blocks. Loads patterns from patterns.json.
Output: hookSpecificOutput format (Claude Code 2025+ hook spec).

Customize patterns.json for your project's framework and anti-patterns.
"""

import json
import os
import re
import sys

HOOKS_DIR = os.path.dirname(os.path.abspath(__file__))

# Protected paths that agents should not modify directly.
# Customize this list for your project.
PROTECTED_PATHS = [
    # Example: "package-lock.json",
    # Example: "yarn.lock",
    # Example: "migrations/",
]


def _respond(decision="allow", reason=None):
    """Output hook response in hookSpecificOutput format and exit."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
        }
    }
    if reason:
        output["hookSpecificOutput"]["permissionDecisionReason"] = reason
    json.dump(output, sys.stdout)
    sys.stdout.flush()
    sys.exit(0)


def load_patterns():
    """Load pattern rules from patterns.json in the same directory."""
    try:
        with open(os.path.join(HOOKS_DIR, "patterns.json")) as f:
            return json.load(f)
    except Exception:
        return None


def get_file_type(file_path):
    """Map file extension to pattern key.

    Extend this mapping for your project's file types.
    """
    if not file_path:
        return None
    ext = os.path.splitext(file_path)[1].lstrip(".")
    mapping = {
        "py": "py",
        "xml": "xml",
        "ts": "ts",
        "tsx": "tsx",
        "js": "js",
        "jsx": "jsx",
        "go": "go",
        "rs": "rs",
        "rb": "rb",
    }
    return mapping.get(ext)


def check_protected_path(file_path):
    """Check if the file is in a protected path."""
    if not file_path or not PROTECTED_PATHS:
        return None
    for protected in PROTECTED_PATHS:
        if protected in file_path:
            return {
                "id": "PROTECTED_PATH",
                "severity": "warn",
                "message": f"Editing protected path: {protected}. Ensure this is intentional.",
            }
    return None


def main():
    raw = sys.stdin.read()
    hook_input = json.loads(raw)
    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    # Determine what content to scan
    if tool_name == "Edit":
        content = tool_input.get("new_string", "")
        file_path = tool_input.get("file_path", "")
    elif tool_name == "Write":
        content = tool_input.get("content", "")
        file_path = tool_input.get("file_path", "")
    else:
        _respond()

    if not content:
        _respond()

    warnings = []

    # Check protected paths
    protected = check_protected_path(file_path)
    if protected:
        sev = protected["severity"].upper()
        warnings.append(f"[{sev}] {protected['id']}: {protected['message']}")

    # Only run pattern checks on known file types
    file_type = get_file_type(file_path)
    if file_type:
        config = load_patterns()
        if config:
            # Run regex pattern checks
            patterns = config.get("patterns", {}).get(file_type, [])
            for pattern in patterns:
                try:
                    if re.search(pattern["regex"], content):
                        sev = pattern["severity"].upper()
                        warnings.append(f"[{sev}] {pattern['id']}: {pattern['message']}")
                except re.error:
                    continue

    if warnings:
        msg = "PATTERN GUARD -- anti-patterns detected in edit:\n" + "\n".join(
            f"  - {w}" for w in warnings
        )
        _respond("allow", msg)
    else:
        _respond()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Absolute failsafe: never crash, never block
        try:
            json.dump(
                {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow"}},
                sys.stdout,
            )
            sys.stdout.flush()
        except Exception:
            pass

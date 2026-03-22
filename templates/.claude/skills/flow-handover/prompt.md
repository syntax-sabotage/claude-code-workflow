---
description: FLOW Handover - End session and capture state
---

<!--
  PROCEDURAL SKILL - Session summarization workflow.
  Captures current work state so the next session can resume seamlessly.
-->

**MODEL:** sonnet
**EXECUTION:** foreground
End the current session and capture state for next session:

## 1. Gather Current State

```bash
git status                 # Uncommitted changes
git branch --show-current  # Current branch
```

Check for active issues:
```bash
# My assigned issues
gh issue list --assignee @me --state open --json number,title,labels --limit 5
```

Check for open PRs:
```bash
# PRs from current branch
gh pr list --head "$(git branch --show-current)" --json number,title,state --limit 5
```

## 2. Read Current Handover File

```bash
cat .context/handover/session.md 2>/dev/null || echo "No previous handover file"
```

Also read shared project state if it exists:
```bash
cat .context/handover/project.md 2>/dev/null || echo "No project handover file"
```

## 3. Update Session Handover File

Write to `.context/handover/session.md` with:
- **Last Updated:** current timestamp and session number
- **Current Focus:** what we were working on
- **What Was Done This Session:** bullet list of changes (current session only -- full detail)
- **Deferred / Not Completed:** MANDATORY section -- list anything from the task that was not completed, with reason for each. Valid reasons: blocked (missing access, dependency), user decision needed, out of scope (explain why). "Can do later" is NOT a valid reason. If nothing was deferred, write "Nothing deferred -- all task items completed."
- **Notes for Next Session:** context that would be lost
- **Previous Sessions:** one-liner summaries

**SESSION HISTORY DISCIPLINE (critical -- do this every handover):**
The previous session's full detail section must be compressed to a single one-liner and moved into the "Previous Sessions (summary)" list. The handover file should only ever contain full detail for the current session. All older sessions are one-liners.

This keeps the handover file under ~120 lines.

## 4. Update Project State (if needed)

Only update `.context/handover/project.md` if:
- Blockers changed (new blocker, blocker resolved)
- Priorities shifted (new critical issue, issue closed)
- Milestones reached (feature shipped, sprint complete)

Do NOT update project.md just because a session ended with no project-level changes.

## Template: Session Handover File

```markdown
# Session Handover

**Last Updated:** <date> (session <N>)

---

## Current Focus

**Session <N> -- <one-line summary>.**
**Branch:** `<branch>` (<status note if relevant>)
**Active issue:** <#number or None>

---

## What Was Done This Session

### Session <N> -- <Title>

- <bullet points>

---

## Deferred / Not Completed

<For each deferred item: what, why, and what unblocks it. "Nothing deferred" if complete.>

---

## Notes for Next Session

<context that would be lost>

---

## Previous Sessions (summary)

- **Session <N-1>** -- <20-word summary>
- **Session <N-2>** -- <20-word summary>
...
```

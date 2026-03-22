---
description: FLOW Resume - Start a new session with full context
---

<!--
  PROCEDURAL SKILL - Context restoration.
  Reads handover file + project state to restore session context.
-->

**MODEL:** sonnet
**EXECUTION:** foreground
Resume work on the project:

## 1. Read Context Files

Read these in order (skip any that don't exist):
1. `.context/substrate.md` -- project overview
2. `.context/handover/session.md` -- last session's handover
3. `.context/handover/project.md` -- shared blockers, priorities
4. `.context/ai-rules.md` -- coding standards
5. `CLAUDE.md` -- project conventions

## 2. Gather Live State

```bash
git branch --show-current
git status
```

```bash
# My assigned issues
gh issue list --assignee @me --state open --json number,title,labels --limit 5
```

```bash
# My open PRs
gh pr list --author @me --state open --json number,title,state --limit 5
```

```bash
# High priority issues
gh issue list --label "priority/critical,priority/high" --state open --json number,title --limit 5 2>/dev/null || \
gh issue list --label "severity::critical,severity::high" --state open --json number,title --limit 5 2>/dev/null || \
echo "No priority labels found"
```

## 3. Present Session Briefing

```
SESSION RESUME
===============================
Last session: <date> (session <N>)
Focus was:    <what was being worked on>

CURRENT STATE
  Branch: <current branch>
  Uncommitted: <yes/no -- count if yes>
  Active issue: <from handover or None>

PENDING WORK
  Open PRs: <list, if any>
  Assigned: <list, if any>

PROJECT STATE
  Blockers: <from project.md>
  Priorities: <top 1-3 from project.md>

SUGGESTED NEXT STEP
  <recommendation based on state>
```

Focus the suggestion on the current state -- recommend the most impactful next action based on what's in progress, what's blocked, and what's ready to pick up.

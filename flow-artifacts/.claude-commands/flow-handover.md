# /flow-handover - End Session

Generate session summary and update handover document.

## Steps

1. **Summarize Session Work**
   - What was worked on
   - What was completed
   - What's still in progress
   - Any blockers discovered

2. **Query Final State**
```bash
gh issue list --state open --label "active" --json number,title,labels
gh issue list --state closed --limit 5 --json number,title,closedAt
```

3. **Update SESSION_HANDOVER.md**
```markdown
# Session Handover

> Current state for resuming work. Updated at session end.

## Last Updated
<date> - <brief description>

## Current State

### Active Work
- #47 [Invoice Pro] Add date validation - 70% complete
  - Completed: model changes, form view
  - Remaining: validation tests

### Blockers
- None / List any

### Recent Completions
- #45 Fixed validation bug
- #44 Updated access rules

## Quick Context

### Module Status
| Module | Status | Notes |
|--------|--------|-------|
| invoice_pro | Active | Working on #47 |
| mcp_security | Stable | No active work |

### Environment
| Env | Status | Notes |
|-----|--------|-------|
| Docker | Running | Synced with latest |
| Production | Running | Last deploy: <date> |

## Next Session

### Suggested First Actions
1. Run /flow-resume
2. Continue #47 - remaining validation work
3. ...

### Known Issues
- ...

## GitHub Status
- Active: 2 issues
- Blocked: 0
- Pool: 3 needs triage
```

4. **Commit Handover If Changed**
```bash
git add .context/SESSION_HANDOVER.md
git commit -m "chore: update session handover"
```

## Output Format

```
## Session Handover Complete

### This Session
- Worked on: #47 invoice date validation
- Completed: #45 validation bug fix
- Blocked: None

### Updated Files
- .context/SESSION_HANDOVER.md

### For Next Session
Run /flow-resume to continue work.

Goodbye!
```

## When to Run

- End of work session
- Before switching to different project
- When context getting too large (/clear)

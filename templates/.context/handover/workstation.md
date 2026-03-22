# [WORKSTATION_NAME] -- Session Handover

> Per-workstation state file. Updated at session end by `/flow-handover`.
> Read at session start by `/flow-resume`.

**Last Updated:** [YYYY-MM-DD HH:MM]
**Role:** [Architect/Developer/Reviewer/Data Engineer/Content Engineer]

## Current Focus

- **Issue:** #[NUMBER] -- [Title]
- **Branch:** `[branch-name]`
- **Status:** [In progress / Blocked / Ready for review]

## What Was Done (This Session)

- [Completed item 1]
- [Completed item 2]
- [Completed item 3]

## Deferred Items

Items that could not be completed this session.

| Item | Reason | Blocked By |
|------|--------|------------|
| [Deferred task] | [Genuine blocker reason] | [Issue #/dependency/decision needed] |

> **Anti-deferral rule:** "Too much work" is not a valid deferral reason.
> If scope is larger than expected, flag it BEFORE starting, not after.

## Notes for Next Session

- [Important context that won't be obvious from code alone]
- [Configuration state, environment notes]
- [Cross-workstation coordination notes]

## Session Debt

Check `.flow/session-debt.jsonl` for unresolved errors/warnings from this session.

```bash
python3 .claude/hooks/check-session-debt.py
```

## Previous Sessions

### [YYYY-MM-DD] -- [Brief summary]
- [What was accomplished]
- [Key decisions made]

### [YYYY-MM-DD] -- [Brief summary]
- [What was accomplished]

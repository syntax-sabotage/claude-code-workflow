---
description: FLOW Triage - Categorize and prioritize open issues
---

<!--
  PROCEDURAL SKILL - Issue categorization.
  Can run in BACKGROUND for large triage jobs.
-->

**MODEL:** sonnet
**EXECUTION:** background (for large pools)
Triage open issues:

1. Run `gh issue list --state open --json number,title,body,labels --limit 50`
2. Identify issues missing required labels (e.g., `type::*`, `severity::*`, `size::*`)

For each issue:
- Assign severity label (critical/high/medium/low)
- Assign type label (feature/task/bug)
- Assign size label (S/M/L)
- Assign autonomy label (0/1/2/3) based on size defaults
- Flag if blocked with appropriate `blocked::*` label (see below)

Apply labels:
```bash
gh issue edit <number> \
  --add-label "severity::<level>" \
  --add-label "type::<type>" \
  --add-label "size::<size>"
```

Present triage summary table.

## Blocking Labels

Dependencies are managed dynamically, not pre-wired. Use these labels when blocks are discovered:

| Label | Meaning |
|-------|---------|
| `blocked::technical-dependency` | Waiting on another issue/PR |
| `blocked::vendor` | Waiting on external party |
| `blocked::information` | Needs requirements clarification |
| `blocked::customer-decision` | Waiting on customer input |
| `blocked::internal-approval` | Waiting on internal sign-off |
| `blocked::environment` | Infra/environment issue |

When adding a blocked label, add a comment explaining what's blocking. Remove the label when unblocked.

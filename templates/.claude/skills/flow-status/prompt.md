---
description: FLOW Status - Show current work state
---

**MODEL:** sonnet
**EXECUTION:** foreground
Show current work state across git, issues, and PRs:

## Gather State

```bash
# Current branch and uncommitted changes
echo "=== Git Status ==="
git branch --show-current
git status --short

echo ""
echo "=== My Assigned Issues ==="
gh issue list --assignee @me --state open --json number,title,labels --limit 10

echo ""
echo "=== My Open PRs ==="
gh pr list --author @me --state open --json number,title,state,reviewDecision --limit 10

echo ""
echo "=== Recent Closed ==="
gh issue list --assignee @me --state closed --limit 5 --json number,title
```

## Render

Present a compact status dashboard:

```
PROJECT STATUS
==========================================

GIT
  Branch: <current branch>
  Status: <clean / N uncommitted changes>

ACTIVE ISSUES
  #<num>  <title>  [<labels>]
  ...

OPEN PRs
  #<num>  <title>  <review status>
  ...

RECENTLY CLOSED
  #<num>  <title>
  ...
```

Keep the output concise. Do NOT make additional API calls beyond those listed above.

---
description: Start Work on GitHub Issue
---

Start work on issue #$ARGUMENTS:

1. Run `gh issue view $ARGUMENTS --json title,body,labels,assignees` to see issue details
2. Run `gh issue edit $ARGUMENTS --add-assignee @me` to assign yourself
3. Create branch:
   ```bash
   DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name')
   git fetch origin
   git checkout -b $ARGUMENTS-<short-slug-from-title> origin/$DEFAULT_BRANCH
   ```
4. Report back with issue summary and branch name

**Branch naming:** `<issue-number>-<short-slug>` (e.g., `42-fix-auth-timeout`)

Generate the slug from the issue title: lowercase, spaces to hyphens, strip special chars, max 50 chars.

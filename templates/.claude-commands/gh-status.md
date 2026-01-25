---
description: GitHub Status Overview
---

Show me the current state of work:

1. Run `gh issue list --state open --label "priority/critical,priority/high" --limit 10` - Critical/high priority issues
2. Run `gh issue list --state open --assignee @me` - My assigned issues
3. Run `git branch --show-current` and check if branch name contains issue number
4. Run `gh pr list --state open --limit 5` - Open PRs

Present a summary:
- What needs urgent attention
- What I'm currently working on
- What's ready for review

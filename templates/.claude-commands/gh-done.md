---
description: Finish Work and Create PR
---

Finish current work and create a PR:

1. Run `git branch --show-current` to get branch name
2. Extract issue number from branch name (e.g., "6-fix-bug" -> 6)
3. Run `git status` - if uncommitted changes, ask what to do
4. Run `git log origin/main..HEAD` - if unpushed commits, push them
5. Create PR: `gh pr create --title "<descriptive title>" --body "Fixes #<issue-number>"`
6. Report back with PR URL

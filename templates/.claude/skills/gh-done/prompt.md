---
description: Finish Work and Create PR
---

Finish current work and create a PR:

1. Run `git branch --show-current` to get branch name
2. Extract issue number from branch name (e.g., "42-fix-bug" -> 42)
3. Run `git status` -- if uncommitted changes, ask what to do
4. Run `git log origin/main..HEAD` -- if unpushed commits, push them:
   ```bash
   git push -u origin $(git branch --show-current)
   ```
5. Create PR:
   ```bash
   gh pr create \
     --title "<descriptive title>" \
     --body "$(cat <<'EOF'
   ## Summary
   <bullet points of changes>

   ## Test plan
   - [ ] <relevant test items>

   Fixes #<issue-number>

   Generated with [Claude Code](https://claude.com/claude-code)
   EOF
   )"
   ```
6. Report back with PR URL

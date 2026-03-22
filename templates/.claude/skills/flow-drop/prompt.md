---
description: FLOW Drop - Release a ticket back to the pool
---

**MODEL:** sonnet
**EXECUTION:** foreground
Release the current (or specified) ticket back to the pool so another developer can pick it up.

## 1. Identify Issue

Determine the issue number:

- If `$ARGUMENTS` is provided, use it (strip `#` prefix if present).
- Otherwise, extract from current branch name:
  ```bash
  BRANCH=$(git branch --show-current)
  IID=$(echo "$BRANCH" | grep -oE '^[0-9]+')
  ```
- If no issue number can be determined, ask the user.

Verify the issue exists and is assigned:
```bash
gh issue view $IID --json title,assignees,labels
```

## 2. Confirm with User

```
Drop issue #<IID>: <title>?

   Currently assigned to: @<assignee>
   Branch: <current branch>
   Uncommitted changes: <yes/no>

   This will:
   - Unassign you from the issue
   - Set status back to ready
   - Post a context comment for the next developer

   [y] Yes, drop it    [n] No, keep working
```

If user declines, stop here.

## 3. Capture Context

Ask user for handover context (or auto-generate):

```
Context for the next developer? (Leave blank to auto-generate from git log)

> _
```

If user provides input, use that as the context.

If blank, auto-generate from recent work:
```bash
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name')
LOG=$(git log origin/$DEFAULT_BRANCH..HEAD --oneline 2>/dev/null)
DIFF_STAT=$(git diff --stat origin/$DEFAULT_BRANCH 2>/dev/null)
```

Build context summary:
```
## Handover Context

**Dropped by:** @<current user> on <date>
**Branch:** <branch name>
**Commits:** <count> commits on branch

### Progress
<user-provided context OR auto-generated summary>

### Files Changed
<diff stat summary>

### Notes
<any warnings about partial work, known issues, etc.>
```

## 4. Update GitHub

```bash
# Unassign and reset status to ready
gh issue edit $IID \
  --remove-assignee @me \
  --remove-label "status::active" \
  --add-label "status::ready"

# Post handover context as comment
gh issue comment $IID \
  --body "$(cat <<'EOF'
## Dropped -- Handover Context

<context from step 3>
EOF
)"
```

## 5. Check for Existing PR

```bash
PR_CHECK=$(gh pr list --head "$BRANCH" --json number,title 2>/dev/null)
```

If a PR exists:
```
PR exists for this branch: #<pr_number>

   Consider marking it as draft:
   gh pr ready <pr_number> --undo

   [d] Mark as draft    [s] Skip (leave PR as-is)
```

If user chooses draft:
```bash
gh pr ready <pr_number> --undo
```

## 6. Local Cleanup

Handle local branch state:

```bash
# Check for uncommitted changes
DIRTY=$(git status --porcelain)
```

If uncommitted changes:
```
Uncommitted changes on branch. What to do?

   [c] Commit WIP (recommended -- preserves work on remote)
   [s] Stash (local only -- may be lost)
   [d] Discard changes
```

**If commit WIP:**
```bash
git add -A
git commit -m "wip: partial work on #$IID

Dropped for reassignment. See issue comment for context.

Co-Authored-By: Claude <noreply@anthropic.com>"
git push -u origin "$BRANCH"
```

**If stash:**
```bash
git stash push -m "WIP for #$IID (dropped)"
```

**If discard:**
```bash
git checkout -- .
```

Then switch back to default branch:
```bash
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name')
git checkout $DEFAULT_BRANCH
```

## 7. Output

```
## Dropped: #<IID> <title>

**Status:** ready (back in pool)
**Assignee:** unassigned
**Context:** Posted as comment on issue
**Branch:** <branch> (on default branch now)

Issue is available for anyone to pick up.
```

## Notes

- Always post a context comment -- the next developer (human or bot) needs to know what was done and what's left.
- WIP commits are preferred over stash -- stashes are local and easy to lose.
- The `status::ready` label makes the issue visible on the board and eligible for automated processing.

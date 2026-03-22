---
description: FLOW Worktree - Manage git worktrees for multi-instance work
---

**MODEL:** sonnet
**EXECUTION:** foreground
Manage git worktrees for parallel CLI instances. Subcommand from `$ARGUMENTS`:

## Usage

```
/flow-worktree list
/flow-worktree create <issue#>
/flow-worktree clean [issue#]
```

## Subcommands

### `list` (default if no arguments)

Show all active worktrees with branch, issue, and status:

```bash
git worktree list
```

For each worktree, also check for uncommitted changes:
```bash
git -C <worktree_path> status --porcelain
```

Present as:
```
WORKTREES
  * project/           main                              (clean)
    project-109/       109-add-auth-middleware            (3 uncommitted)
    project-108/       108-fix-data-export                (clean)

* = current worktree
```

### `create <issue#>`

Create a new worktree for the given issue:

1. **Fetch latest:**
   ```bash
   git fetch origin
   ```

2. **Get issue title for branch slug:**
   ```bash
   gh issue view <issue#> --json title -q '.title'
   ```

3. **Create branch slug** from title (lowercase, spaces to hyphens, max 50 chars, no special chars)

4. **Check if branch already exists:**
   ```bash
   git branch --list "<issue#>-*"
   ```
   If branch exists, use it. If not, create from `origin/main`.

5. **Create worktree:**
   ```bash
   # New branch
   DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name')
   git worktree add ../<project>-<issue#> -b <issue#>-<slug> origin/$DEFAULT_BRANCH

   # Existing branch
   git worktree add ../<project>-<issue#> <existing-branch>
   ```

6. **Report:**
   ```
   Worktree created: ../<project>-<issue#>/
   Branch: <issue#>-<slug>

   To work in it, open a new Claude Code CLI:
     cd ../<project>-<issue#> && claude
   ```

### `clean [issue#]`

Remove worktrees whose branches are merged, or a specific one:

**If `issue#` provided:**
```bash
git worktree remove ../<project>-<issue#>
git branch -d <branch>  # Only if merged into main
```

**If no `issue#`:**
1. List all worktrees
2. For each non-main worktree, check if branch is merged:
   ```bash
   DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name')
   git branch --merged $DEFAULT_BRANCH | grep <branch>
   ```
3. Offer to remove merged ones:
   ```
   Merged worktrees (safe to remove):
     project-108/  108-fix-data-export

   Unmerged worktrees (keep):
     project-109/  109-add-auth-middleware

   Remove merged worktrees? [y/n]
   ```
4. Remove confirmed worktrees:
   ```bash
   git worktree remove ../<project>-<issue#>
   git branch -d <branch>
   ```

## Notes

- Worktrees share the same `.git` object store -- pushes from any worktree work normally
- Convention: worktrees go in sibling directories `../<project>-<issue#>/`
- Each worktree has its own independent working directory and git index
- Useful for working on multiple issues in parallel with separate Claude Code instances

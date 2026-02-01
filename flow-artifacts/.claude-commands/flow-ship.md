# /flow-ship - Complete and Deploy

Ship completed work: PR, merge, close issue, deploy.

## Prerequisites
- Work completed on feature branch
- Tests passing (if applicable)
- Code reviewed (for significant changes)

## Steps

1. **Verify Current State**
```bash
git status
git log main..HEAD --oneline
```

2. **Identify Active Issue**
```bash
gh issue list --state open --label "active" --json number,title
```

3. **Create/Update PR**
```bash
# If PR doesn't exist
gh pr create --title "<issue#> <title>" --body "Closes #<issue#>\n\n## Changes\n- ..."

# If PR exists
gh pr view --json number,title
```

4. **Merge PR**
```bash
gh pr merge --squash --delete-branch
```

5. **Close Issue with Learnings**
```bash
gh issue close <issue#> --comment "## Completed

### Changes
- ...

### Learnings
- ..."

gh issue edit <issue#> --remove-label "active"
```

6. **Deploy (Project-Specific)**

Adapt these steps to your deployment pipeline:

```bash
# Example: Run pre-deploy checks
# ./deploy.sh --dry-run

# Example: Deploy to staging
# ./deploy.sh staging

# Example: Deploy to production
# ./deploy.sh production

# Example: Verify deployment
# ssh $PROD_HOST "systemctl status $SERVICE && journalctl -u $SERVICE -n 20 --no-pager"
```

> **Note:** Replace the above with your project's actual deployment commands.
> See `templates/.claude-commands-examples/vps-upgrade.md` for a concrete example.

9. **Check for Reflection Trigger**
```bash
# Count unreflected closed issues in stream
gh issue list --state closed --milestone "<stream>" --json labels | \
  jq '[.[] | select(.labels | map(.name) | contains(["reflected"]) | not)] | length'
```

If 3+ unreflected: Suggest `/flow-reflect <stream>`

10. **Update State Cache**
```bash
.flow/update-state.sh --clear-active
```

## Output Format

```
## Shipped Issue #47

### PR
- #52 merged to main

### Deployment
- [x] Pre-deploy checks passed
- [x] Staging verified
- [x] Production deployed
- [x] Production service healthy

### Issue Closed
- Added learnings comment
- Removed 'active' label

### Reflection Check
3 unreflected issues in "Invoice Pro" stream.
Consider running: /flow-reflect "Invoice Pro"
```

## After Shipping

- Run `/flow-status` to see next work
- Or `/flow-reflect <stream>` if prompted

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

6. **Verify Modules (Pre-Deploy Check)**
```bash
# Fetch latest sources
./deploy.py

# Verify all required modules available
./deploy.py verify
```

7. **Deploy to Docker (Test)**
```bash
# Preview what will be deployed
./deploy.py --dry-run docker

# Deploy and restart Odoo
./deploy.py docker

# Verify: Check Odoo logs for module errors
docker-compose -f /Users/larsweiler/Dev-Odoo19/docker/docker-compose.yml logs --tail=50 odoo19
```

8. **Deploy to Production (If Ready)**
```bash
# Preview production deployment
./deploy.py --dry-run vps

# Deploy to production and restart
./deploy.py vps

# Verify: Check Odoo service status
ssh root@185.163.117.155 "systemctl status odoo19 && journalctl -u odoo19 -n 20 --no-pager"
```

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
- [x] Modules verified (./deploy.py verify)
- [x] Docker dev environment updated
- [x] Docker logs checked - no errors
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

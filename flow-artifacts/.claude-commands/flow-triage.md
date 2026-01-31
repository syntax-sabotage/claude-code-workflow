# /flow-triage - Assign Pool Items

Triage issues in the pool (needs-triage label) to streams.

## Steps

1. **List Pool Items**
```bash
gh issue list --state open --label "needs-triage" --json number,title,body,labels
```

2. **For Each Issue, Determine:**
   - Which stream (milestone) it belongs to
   - Size estimate (S/M/L)
   - Type (bug/feature/debt/security/odoo)
   - Autonomy level (if not default)

3. **Update Issue**
```bash
gh issue edit <number> \
  --milestone "<stream>" \
  --add-label "size/<size>" \
  --add-label "type/<type>" \
  --remove-label "needs-triage"
```

4. **Add Default Autonomy**
```bash
# Based on size and type
gh issue edit <number> --add-label "autonomy/<level>"
```

## Triage Decision Matrix

| Type | Size | Default Autonomy |
|------|------|-----------------|
| bug | S | 2 |
| bug | M | 2 |
| bug | L | 1 |
| feature | S | 2 |
| feature | M | 2 |
| feature | L | 1 |
| security | any | 1 |
| debt | any | 2 |

## Output Format

```
## Triage Complete

### Processed Issues

| # | Title | Stream | Size | Type | Autonomy |
|---|-------|--------|------|------|----------|
| 50 | PDF export issue | Invoice Pro | M | bug | 2 |
| 51 | Batch processing | Invoice Pro | L | feature | 1 |
| 52 | Update dependencies | Maintenance | S | debt | 2 |

### Remaining in Pool
None - all triaged!

### Summary
- 3 issues triaged
- 2 -> Invoice Pro
- 1 -> Maintenance
```

## Quick Triage Commands

```bash
# Quick assign to stream
gh issue edit 50 --milestone "Invoice Pro" --remove-label "needs-triage"

# Set size
gh issue edit 50 --add-label "size/M"

# Set type
gh issue edit 50 --add-label "type/bug"

# Full triage in one command
gh issue edit 50 \
  --milestone "Invoice Pro" \
  --add-label "size/M" \
  --add-label "type/bug" \
  --add-label "autonomy/2" \
  --remove-label "needs-triage"
```

## When Items Stay in Pool

Some items should stay with `needs-triage`:
- Unclear requirements (needs clarification)
- Duplicate of existing issue
- Out of scope for current streams
- Needs user input

Add a comment explaining why it wasn't triaged.

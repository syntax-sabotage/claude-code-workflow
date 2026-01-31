# /flow-status - View FLOW State

Query GitHub for current workflow state and update statusline cache.

## Steps

0. **Update State Cache**
```bash
.flow/update-state.sh
```

1. **List All Open Milestones**
```bash
gh api repos/{owner}/{repo}/milestones --jq '.[] | {title, open_issues, due_on, description}'
```

2. **List Active Issues (Being Worked On)**
```bash
gh issue list --state open --label "active" --json number,title,labels,milestone,assignees
```

3. **List Blocked Issues**
```bash
gh issue list --state open --label "blocked" --json number,title,labels,milestone
```

4. **List Pool (Untriaged)**
```bash
gh issue list --state open --label "needs-triage" --json number,title,labels
```

5. **Issues by Stream**
```bash
gh issue list --state open --milestone "<stream>" --json number,title,labels
```

6. **Recent Completions**
```bash
gh issue list --state closed --limit 10 --json number,title,closedAt,milestone
```

7. **Module Status (from modules.lock)**
```bash
# Show what modules are configured and their versions
./deploy.py --dry-run docker 2>/dev/null || cat modules.lock | grep -E "^name|^version"
```

## Output Format

```
## FLOW Status - IT-Beratung Odoo

### Streams (Milestones)
| Stream | Open | Description |
|--------|------|-------------|
| Invoice Pro | 5 | AI invoice processing features |
| Security | 2 | MCP security, access control |
| Infrastructure | 1 | Docker, VPS, deployment |

### Active Work
- #47 [Invoice Pro] Add date validation (size/M, @user)
- #32 [Security] Fix permission check (size/S)

### Blocked
- #28 [Infrastructure] VPS upgrade - waiting on provider

### Pool (Needs Triage)
- #50 User reported PDF export issue
- #51 Feature request: batch processing

### Recent Completions (Last 7 Days)
- #45 [Invoice Pro] Fixed validation bug
- #44 [Security] Updated access rules

### Module Versions (modules.lock)
| Module | Source | Version | Required |
|--------|--------|---------|----------|
| foundation | praetorx | 19.0.1.3.18 | yes |
| praetorx_base | praetorx | 19.0.1.1.2 | yes |
| invoice_pro | praetorx | 19.0.1.0.16 | yes |
| mcp_security | praetorx | 19.0.1.0.8 | yes |
| praetorx_vault | praetorx | 19.0.3.0.11 | no |
| scribe | praetorx | 19.0.1.1.12 | no |
| social_media_management | local | 19.0.1.0.0 | yes |

### Summary
- 3 active objectives
- 1 blocked
- 2 in pool awaiting triage
- 8 total open issues

### Suggested Actions
1. Triage pool items: /flow-triage
2. Unblock #28 if possible
3. Continue active work
```

## Filtering Options

```bash
# By milestone
gh issue list --milestone "Invoice Pro" --state open

# By label
gh issue list --label "type/bug" --state open

# By size
gh issue list --label "size/L" --state open
```

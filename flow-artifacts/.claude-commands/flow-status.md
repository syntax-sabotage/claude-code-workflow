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

7. **Project-Specific Status (Optional)**
```bash
# Add project-specific status checks here, e.g.:
# npm run build --dry-run
# ./deploy.sh status
# cat package.json | jq '.version'
```

## Output Format

```
## FLOW Status - {{PROJECT_NAME}}

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

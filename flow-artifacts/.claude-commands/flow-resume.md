# /flow-resume - Start Session

Resume work by querying current GitHub state and refreshing statusline cache.

## Steps

0. **Update State Cache**
```bash
.flow/update-state.sh
```

1. **Query Active Work**
```bash
gh issue list --state open --label "active" --json number,title,labels,milestone
```

2. **Query Blocked Issues**
```bash
gh issue list --state open --label "blocked" --json number,title,labels
```

3. **Check Recent Completions**
```bash
gh issue list --state closed --limit 5 --json number,title,closedAt
```

4. **List Open Milestones**
```bash
gh api repos/{owner}/{repo}/milestones --jq '.[] | {title, open_issues, due_on}'
```

5. **Read Session Handover**
```
Read .context/SESSION_HANDOVER.md for previous session context
```

## Output Format

```
## Session Resume - IT-Beratung Odoo

### Active Work
- #47 [Invoice Pro] Feature X (size/M, autonomy/2)

### Blocked
- #32 Waiting on API access

### Recent Completions
- #45 Fixed validation bug (closed 2 hours ago)

### Streams (Milestones)
- Invoice Pro: 3 open issues
- Security: 1 open issue

### Previous Session Notes
[Summary from SESSION_HANDOVER.md]

### Suggested Next Action
[Based on priority and state]
```

## After Running

- Pick an issue to work on with `/flow-start <issue#>`
- Or triage pool items with `/flow-triage`
- Or check specific stream with `/flow-stream <name>`

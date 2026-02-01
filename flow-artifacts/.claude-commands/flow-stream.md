# /flow-stream <name> - Manage Stream

Query or create a stream (GitHub milestone).

## Arguments
- `name` - Stream name to query or create

## Query Mode (Stream Exists)

1. **Get Milestone Details**
```bash
gh api repos/{owner}/{repo}/milestones --jq '.[] | select(.title == "<name>")'
```

2. **List Stream Issues**
```bash
gh issue list --milestone "<name>" --state open --json number,title,labels
gh issue list --milestone "<name>" --state closed --json number,title,closedAt
```

3. **Calculate Progress**
```
Open: X issues
Closed: Y issues
Progress: Y/(X+Y) %
```

## Output Format (Query)

```
## Stream: Invoice Pro

### Description
AI-powered invoice processing features

### Progress
- Open: 5 issues
- Closed: 12 issues
- Progress: 70%

### Open Issues
| # | Title | Size | Status |
|---|-------|------|--------|
| 47 | Add date validation | M | active |
| 48 | PDF export | M | - |
| 50 | Batch processing | L | - |

### Recent Completions
- #45 Fixed validation bug (2 days ago)
- #44 Updated access rules (5 days ago)

### Unreflected Issues
3 closed issues ready for /flow-reflect
```

## Create Mode (Stream Doesn't Exist)

1. **Prompt for Details**
   - Description
   - Due date (optional)

2. **Create Milestone**
```bash
gh api repos/{owner}/{repo}/milestones -f title="<name>" -f description="<desc>" -f due_on="<date>"
```

3. **Suggest Initial Objectives**

## Output Format (Create)

```
## Created Stream: Infrastructure

### Details
- Description: Docker, VPS, deployment infrastructure
- Due: 2026-03-01

### URL
https://github.com/{{owner}}/{{repo}}/milestone/4

### Next Steps
Add objectives with: /flow-objective "<title>"
```

## Common Streams for This Project

| Stream | Focus |
|--------|-------|
| Invoice Pro | AI invoice processing features |
| Security | MCP security, access control |
| Infrastructure | Docker, VPS, deployment |
| Maintenance | Bug fixes, updates, tech debt |
| Social Media | Social media management features |

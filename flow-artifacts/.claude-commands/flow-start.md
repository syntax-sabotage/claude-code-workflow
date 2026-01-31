# /flow-start <issue#> - Claim and Start Work

Claim a GitHub issue and begin implementation.

## Arguments
- `issue#` - GitHub issue number to work on

## Steps

1. **Fetch Issue Details**
```bash
gh issue view <issue#> --json title,body,labels,milestone
```

2. **Check Autonomy Level**
- Look for `autonomy/0`, `autonomy/1`, `autonomy/2`, or `autonomy/3` label
- If missing, infer from size: S/M -> autonomy/2, L -> autonomy/1

3. **Claim the Issue**
```bash
gh issue edit <issue#> --add-label "active"
```

4. **Create Feature Branch**
```bash
git checkout main
git pull origin main
git checkout -b <issue#>-<slug>
```

5. **Execute Based on Autonomy**

| Autonomy | Execution Mode |
|----------|----------------|
| 0-1 | Interactive - work in foreground, coordinate with user |
| 2-3 | Background - spawn subagent, user stays available |

### For Autonomy 2-3 (Background):
```javascript
Task({
  prompt: "Implement issue #<issue#>: <title>\n\nDescription:\n<body>\n\nFollow .context/ai-rules.md for Odoo patterns.",
  subagent_type: "coder",
  run_in_background: true
})
```

### For Autonomy 0-1 (Interactive):
Work directly, asking questions as needed.

## Output Format

```
## Starting Issue #47

**Title:** Add invoice date validation
**Stream:** Invoice Pro
**Size:** M
**Autonomy:** 2 (background)

**Branch:** 47-invoice-date-validation

[For autonomy 2-3]
Spawned background agent to implement. Will report when complete.

[For autonomy 0-1]
Working interactively. Here's my plan:
1. ...
2. ...
```

6. **Update State Cache**
```bash
.flow/update-state.sh
```

## After Starting

- For background: Wait for agent completion
- For interactive: Begin implementation
- When done: Use `/flow-ship` to complete

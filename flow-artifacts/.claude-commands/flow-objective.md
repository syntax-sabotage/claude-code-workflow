# /flow-objective <title> - Create New Objective

Create a new GitHub issue with proper FLOW labels.

## Arguments
- `title` - Short descriptive title for the objective

## Interactive Prompts

1. **Stream Selection**
   - List existing milestones
   - Or create new milestone

2. **Size Estimation**
   - S (hours)
   - M (days)
   - L (week+)

3. **Type Selection**
   - bug
   - feature
   - debt
   - security
   - odoo

4. **Description**
   - What needs to be done
   - Acceptance criteria
   - Any technical notes

## Steps

1. **Get Stream (Milestone)**
```bash
gh api repos/{owner}/{repo}/milestones --jq '.[].title'
```

2. **Create Issue**
```bash
gh issue create \
  --title "<title>" \
  --body "## Objective
<description>

## Acceptance Criteria
- [ ] ...

## Technical Notes
..." \
  --milestone "<stream>" \
  --label "size/<size>" \
  --label "type/<type>"
```

3. **Set Default Autonomy**
- size/S -> autonomy/2
- size/M -> autonomy/2
- size/L -> autonomy/1
- security type -> autonomy/1

```bash
gh issue edit <number> --add-label "autonomy/<level>"
```

## Output Format

```
## Created Objective #48

**Title:** Add PDF export for invoices
**Stream:** Invoice Pro
**Size:** M
**Type:** feature
**Autonomy:** 2

**URL:** https://github.com/lweiler-lab/it-beratung/issues/48

Start work with: /flow-start 48
```

## Templates by Type

### Bug
```markdown
## Bug Description
What's happening vs what should happen.

## Steps to Reproduce
1. ...

## Expected Behavior
...

## Actual Behavior
...
```

### Feature
```markdown
## Feature Description
What we're adding and why.

## Acceptance Criteria
- [ ] User can...
- [ ] System validates...

## Technical Approach
...
```

### Technical Debt
```markdown
## Current State
What's wrong with current implementation.

## Desired State
How it should be after cleanup.

## Impact
Why this matters now.
```

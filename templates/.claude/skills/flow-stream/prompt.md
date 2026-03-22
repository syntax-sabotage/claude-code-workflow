---
description: FLOW Stream - Manage milestones/streams
---

**MODEL:** sonnet
**EXECUTION:** foreground
Manage streams (GitHub milestones):

**Usage:**
- `/flow-stream` -- list all streams with issue counts
- `/flow-stream create <name>` -- create a new stream
- `/flow-stream <name>` -- show stream details and issues

**List streams:**
1. Run `gh api repos/{owner}/{repo}/milestones --jq '.[] | {title, open_issues, closed_issues, due_on, state}'`

Present as a formatted table with progress percentages.

**Create stream:**
1. Ask for a description if not provided
2. `gh api repos/{owner}/{repo}/milestones -X POST -f "title=$ARGUMENTS" -f "description=<description>"`

**Show stream:**
1. `gh issue list --milestone "$ARGUMENTS" --state open --json number,title,labels`
2. `gh issue list --milestone "$ARGUMENTS" --state closed --json number,title`
3. Calculate progress percentage (closed vs total)

Present stream details with issue breakdown:
```
STREAM: <name>
Progress: <closed>/<total> (<percentage>%)

Open:
  #<num>  <title>  [<labels>]
  ...

Closed:
  #<num>  <title>
  ...
```

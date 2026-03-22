---
description: FLOW Runner - Autonomous ticket processing agent
---

<!--
  PROCEDURAL SKILL - Autonomous background runner.
  Three modes: start (supervised subagents), batch (fire-and-forget), work (explicit list).
  Manages its own state file and GitHub log issue.
-->

**MODEL:** sonnet (orchestration) -> sonnet (workers)
**EXECUTION:** background (start/batch) or foreground (status/report)
## Usage

```
/flow-runner start [--milestone <name>] [--limit <n>] [--dry-run]
/flow-runner batch [--milestone <name>] [--limit <n>]
/flow-runner work <#N> [<#N>...]
/flow-runner status
/flow-runner report
```

Parse subcommand and options from `$ARGUMENTS`. First word is the subcommand, rest are options.

---

## Shared: Constants & Paths

```bash
STATE_FILE=".flow/runner-state.json"
```

### Config Defaults (embedded in state file on first run)

```json
{
  "max_fix_cycles": 2,
  "eligible_autonomy": [2, 3],
  "eligible_sizes": ["s", "m"],
  "timeout_sec": { "s": 900, "m": 1800 }
}
```

---

## Shared: State File Management

State lives at `.flow/runner-state.json`. Initialize on first run if missing:

```bash
if [[ ! -f "$STATE_FILE" ]]; then
  mkdir -p .flow
  cat > "$STATE_FILE" << 'INIT'
{
  "log_issue_number": null,
  "current_run": null,
  "last_run": null,
  "config": {
    "max_fix_cycles": 2,
    "eligible_autonomy": [2, 3],
    "eligible_sizes": ["s", "m"],
    "timeout_sec": { "s": 900, "m": 1800 }
  }
}
INIT
fi
```

### Log Issue Creation

On first run (when `log_issue_number` is null), create a GitHub issue to accumulate run logs:

```bash
LOG_NUM=$(jq -r '.log_issue_number' "$STATE_FILE")
if [[ "$LOG_NUM" == "null" || -z "$LOG_NUM" ]]; then
  LOG_NUM=$(gh issue create \
    --title "Runner Log -- Autonomous Ticket Processing" \
    --label "type::task,severity::low" \
    --body "$(cat <<'DESC'
Automated log for `/flow-runner` runs. Each run appends a summary comment.

**Do not close** -- this issue accumulates operational history.
DESC
)" 2>&1 | grep -oP '#\K[0-9]+' | head -1)

  # Store in state file
  jq --argjson num "$LOG_NUM" '.log_issue_number = $num' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
  echo "Created runner log issue: #$LOG_NUM"
fi
```

---

## Shared: Queue Query

Build the eligible ticket queue. Filters: `autonomy::2` or `autonomy::3`, `size::s` or `size::m`, `status::ready`, no `blocked::*` labels, unassigned.

```bash
QUEUE=$(gh issue list --label "status::ready" --state open --limit 100 \
  --json number,title,labels,assignees \
  | python3 -c "
import json, sys

issues = json.load(sys.stdin)
blocked_prefixes = ['blocked::']
queue = []
for issue in issues:
    labels = [l['name'] for l in issue.get('labels', [])]
    # Skip if already assigned
    if issue.get('assignees') and len(issue['assignees']) > 0:
        continue
    # Skip if blocked
    if any(l.startswith('blocked::') for l in labels):
        continue
    # Check autonomy
    autonomy_vals = [int(l.split('::')[1]) for l in labels if l.startswith('autonomy::')]
    if not autonomy_vals or max(autonomy_vals) < 2:
        continue
    # Check size
    size_vals = [l.split('::')[1] for l in labels if l.startswith('size::')]
    if not size_vals or size_vals[0] not in ('s', 'm'):
        continue
    sev_vals = [l.split('::')[1] for l in labels if l.startswith('severity::')]
    queue.append({
        'number': issue['number'], 'title': issue['title'], 'labels': labels,
        'size': size_vals[0], 'autonomy': max(autonomy_vals),
        'severity': sev_vals[0] if sev_vals else 'low',
    })
sev_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
queue.sort(key=lambda x: (sev_order.get(x['severity'], 3), x['number']))
print(json.dumps(queue))
")
```

**Milestone filter** (if `--milestone <name>` provided): add `--milestone "<name>"` to the `gh issue list` command.

**Limit** (if `--limit <n>` provided): truncate queue in the python filter: `queue = queue[:N]`.

**Sort order:** severity::critical first, then severity::high, then by number ascending (oldest first).

---

## Shared: Worker Prompt Template

This is the prompt given to each subagent. Substitute `<ISSUE_NUM>`, `<ISSUE_TITLE>`, `<ISSUE_BODY>`, `<BRANCH>`, `<SIZE>`, `<MAX_FIX_CYCLES>`.

```
You are an autonomous worker. Complete this ticket independently.

## Ticket
**#<ISSUE_NUM>**: <ISSUE_TITLE>

<ISSUE_BODY>

## Setup
You are on branch `<BRANCH>`.

## Instructions

0. **Read context first:**
   - Read .context/ai-rules.md if it exists
   - Read CLAUDE.md for project conventions

1. **Explore** the relevant code before making changes.

2. **Implement** the ticket requirements.

3. **Verify** your work:
   Run the project's configured linter/formatter/tests.

4. **Fix cycle** (up to <MAX_FIX_CYCLES> attempts):
   - If checks fail, fix the issues and re-check.
   - If still failing after <MAX_FIX_CYCLES> cycles, STOP and report failure.

5. **Commit** with conventional commit message:
   ```bash
   git add <changed-files>
   git commit -m "<type>(<scope>): <description>

   Closes #<ISSUE_NUM>

   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

6. **Push:**
   ```bash
   git push -u origin <BRANCH>
   ```

7. **Create PR:**
   ```bash
   gh pr create \
     --title "<type>(<scope>): <short description>" \
     --body "$(cat <<'EOF'
   ## Summary
   <bullet points>

   ## Verification
   - [x] Lint/format passed
   - [x] Tests passed (if applicable)

   Closes #<ISSUE_NUM>

   source::runner | Generated with [Claude Code](https://claude.com/claude-code)
   EOF
   )"
   ```

8. **Update acceptance criteria checkboxes** in the issue description (mark completed items).

9. **Update issue labels:**
    ```bash
    gh issue edit <ISSUE_NUM> \
      --remove-label "status::active" --add-label "status::review" --add-label "source::runner"
    ```

## Decision Blocks
If you encounter something that requires a human decision (ambiguous requirements, architectural choice, unclear scope):
1. Do NOT guess. Stop working on this ticket.
2. Add `blocked::agent-escalation` label to the issue.
3. Add a comment explaining what decision is needed.
4. Report back with result: "escalated"

## Result
When done, output a JSON summary as the LAST thing you write:
```json
{
  "result": "shipped" | "escalated" | "failed",
  "pr_number": <number or null>,
  "branch": "<branch-name>",
  "fix_cycles": <number>,
  "summary": "<one-line summary of what was done>"
}
```
```

---

## Subcommand: `start`

Subagent-based mode. Spawns one Task agent per ticket, sequentially.

### Execution

1. **Auth check:**
   ```bash
   gh auth status
   ```

2. **Initialize state file** (see Shared section).

3. **Create log issue** if needed (see Shared section).

4. **Build queue** (see Shared: Queue Query). Apply `--milestone` and `--limit` if provided.

5. **Dry run** (if `--dry-run`): Print the queue and exit.
   ```
   RUNNER DRY RUN -- <n> eligible tickets

   | # | Title | Size | Severity |
   |---|-------|------|----------|
   | #42 | fix: auth timeout | S | medium |
   | #43 | feat: export endpoint | M | low |
   ...

   Run without --dry-run to process.
   ```

6. **Update state: current_run**
   ```bash
   jq --arg id "run-$(date +%Y%m%d-%H%M%S)" \
      --arg mode "start" \
      --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
      '.current_run = {id: $id, mode: $mode, started_at: $ts, tickets: [], totals: {processed: 0, shipped: 0, escalated: 0, failed: 0}}' \
      "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
   ```

7. **Process tickets sequentially.** For each ticket in the queue:

   a. **Create branch:**
      ```bash
      SLUG=$(echo "<title>" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-' | cut -c1-50)
      DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name')
      git fetch origin
      git checkout -b "<NUM>-$SLUG" origin/$DEFAULT_BRANCH
      ```

   b. **Fetch issue body:**
      ```bash
      BODY=$(gh issue view <NUM> --json body -q '.body')
      ```

   c. **Claim issue:**
      ```bash
      gh issue edit <NUM> \
        --remove-label "status::ready" --add-label "status::active"
      ```

   d. **Spawn worker subagent:**
      ```
      Task tool with:
        - prompt: <Worker Prompt Template with substitutions>
      ```

   e. **Parse worker result** from the agent's response. Extract the JSON summary.

   f. **Update state file** with ticket result.

   g. **If result is "escalated" or "failed":** Log it, continue to next ticket.

   h. **Switch back to default branch** before processing next ticket:
      ```bash
      git checkout $DEFAULT_BRANCH
      ```

8. **Finalize run:**
   - Move `current_run` to `last_run` in state file.
   - Post summary comment to log issue.
   - Print summary table.

### Summary Output

```
RUNNER COMPLETE -- run-<id>

| # | Title | Result | PR | Fix Cycles |
|---|-------|--------|----|------------|
| #42 | fix: auth timeout | shipped | #45 | 0 |
| #43 | feat: export endpoint | shipped | #46 | 1 |
| #44 | refactor: data layer | escalated | -- | -- |

Totals: 3 processed, 2 shipped, 1 escalated, 0 failed
Log: #<log_issue_number>
```

---

## Subcommand: `batch`

Fire-and-forget batch mode for long-running processing.

### Execution

1. **Auth check**, **initialize state**, **create log issue** (same as `start`).

2. **Build queue** and serialize to `.flow/runner-queue.json`:
   ```bash
   echo "$QUEUE" > ".flow/runner-queue.json"
   ```

3. **Process each ticket** from the queue file:
   - Read queue file, pop the first ticket
   - If queue is empty, stop
   - Create branch, claim issue, implement, verify, commit, push, create PR
   - Update queue file (remove processed ticket)
   - Update state file with result
   - Continue to next ticket

4. **After all tickets processed:**
   - Finalize state (move current_run to last_run)
   - Post summary to log issue
   - Print summary

### Notes on Batch Mode

- Each ticket is processed independently
- Queue state is maintained in `.flow/runner-queue.json` (file-based, survives interruptions)
- Runner state is maintained in `.flow/runner-state.json`
- Best for processing many small tickets (e.g., i18n, formatting fixes)

---

## Subcommand: `work`

Explicit issue list mode. Process specific tickets by number, bypassing queue query.

### Usage

```
/flow-runner work 42 43 44
/flow-runner work #42 #43 #44
```

### Execution

1. **Parse issue numbers** from arguments (strip `#` prefix if present).

2. **Auth check**, **initialize state**, **create log issue** (same as `start`).

3. **Fetch issue details** for each number:
   ```bash
   for NUM in <issue_numbers>; do
     gh issue view "$NUM" --json number,title,body,labels,assignees
   done
   ```

4. **Validate** each issue exists and is open. Warn (but don't skip) if:
   - Issue has a `blocked::*` label
   - Issue is not `status::ready`
   - Issue doesn't have `autonomy::2` or `autonomy::3`
   - Issue is already assigned to someone

   Present warnings:
   ```
   RUNNER WORK -- <n> tickets queued

   | # | Title | Size | Warnings |
   |---|-------|------|----------|
   | #42 | fix: auth timeout | S | -- |
   | #43 | refactor: data layer | M | Not autonomy::2+, assigned |

   Proceed? [y/n]
   ```

5. **Process tickets** -- same sequential loop as `start` mode.

6. **Finalize** -- same as `start` mode.

### Key Difference from `start`

- No queue query -- issues are explicitly provided.
- No milestone filter or limit -- processes exactly the listed tickets.
- Warns but doesn't block on non-standard labels (user explicitly chose these tickets).

---

## Subcommand: `status`

Show current runner state. Foreground, read-only.

```bash
STATE=$(cat "$STATE_FILE" 2>/dev/null)
```

### If `current_run` exists (runner is active):

```
RUNNER ACTIVE -- <run_id>

Mode: <mode>
Started: <started_at>
Progress: <processed>/<total> tickets

| # | Title | Result | PR |
|---|-------|--------|----|
| #42 | fix: auth timeout | shipped | #45 |
| #43 | feat: export endpoint | in_progress | -- |
```

### If no `current_run` (runner idle):

```
RUNNER IDLE

Last run: <last_run.id or "never">
  Completed: <completed_at>
  Processed: <processed>, Shipped: <shipped>, Escalated: <escalated>, Failed: <failed>

Log issue: #<log_issue_number>
```

---

## Subcommand: `report`

Fetch the full run history from the log issue. Foreground, read-only.

```bash
LOG_NUM=$(jq -r '.log_issue_number' "$STATE_FILE")
gh issue view "$LOG_NUM" --comments
```

Present the issue body and all comments (each comment = one run summary).

---

## Labels

### Used by Runner

| Label | When Applied |
|-------|-------------|
| `status::active` | When runner claims a ticket |
| `status::review` | When runner ships a ticket |
| `source::runner` | On PR description and issue (identifies runner-created work) |
| `blocked::agent-escalation` | When runner hits a decision block |

### Eligibility Filter

Ticket must have ALL of:
- `status::ready`
- `autonomy::2` or `autonomy::3`
- `size::s` or `size::m`
- No `blocked::*` labels
- No assignee (unassigned)

---

## Error Handling

| Scenario | Action |
|----------|--------|
| gh auth fails | Abort with instructions to authenticate |
| Worker crashes / timeout | Mark ticket as "failed", add comment to issue, continue |
| Lint/format fails after max cycles | Mark as "failed", push partial work, continue |
| Queue empty | Report "no eligible tickets" and exit |
| Decision block | Worker adds `blocked::agent-escalation`, continues to next |

---

## Notes

- Runner never touches `autonomy::0` or `autonomy::1` tickets -- those need human interaction.
- Runner never touches `size::l` tickets -- too complex for autonomous processing.
- The `source::runner` label on PRs makes it easy to filter runner-created work for review.
- State file is the single source of truth for run progress -- survives process restarts.
- Log issue accumulates history across runs -- never close it.

---
description: FLOW Start - Begin work on an issue
---

**MODEL: Sonnet (analysis) -> Sonnet/Opus (execution)**
**EXECUTION: Foreground or Background (autonomy-based)**
Start work on issue #$ARGUMENTS:

## 1. Fetch & Analyze Issue

Fetch and analyze the issue:

```bash
gh issue view $ARGUMENTS --json title,body,labels,milestone,assignees
```

Extract and analyze:
1. **title**: Issue title
2. **body**: Full description
3. **labels**: All labels (especially `size::*`, `autonomy::*`, type markers)
4. **milestone**: Stream/milestone name if assigned
5. **complexity_labels**: Any of [architecture, refactor, breaking-change, size::l, size::xl]
6. **description_length**: Character count of body
7. **subtask_count**: Count of `- [ ]` checkbox items in body
8. **is_complex**: true if ANY of:
   - Has complexity labels
   - description_length > 1000
   - subtask_count >= 5
9. **is_blocked**: true if any label starts with `blocked::`
10. **blocked_reason**: The `blocked::` label if present
11. **assignees**: Current assignees
12. **is_assigned**: true if non-empty

### If `is_blocked: true`

Warn user before proceeding:
```
Issue #<number> is blocked

   Label: <blocked_reason>

   Check issue comments for blocking details.

   [c] Continue anyway    [a] Abort
```

If user aborts, stop here.

### If `is_assigned: true`

Warn user before proceeding:
```
Issue #<number> is assigned to @<assigned_to>

   [f] Force-claim (reassign to me)
   [a] Abort
```

If user aborts, stop here.
If user force-claims, proceed -- the claim step will reassign.

## 2. Pre-Flight Model Selection

Based on analysis:

### If `is_complex: true`

Prompt user with complexity details:
```
Suggestion: How would you like to approach this complex issue?

   Detected complexity:
   - ${complexity_reasons joined}

   [y] Plan mode        -- deep planning, human approval before execution
   [n] Direct mode      -- direct implementation
```

**If user chooses plan mode:**
- Use EnterPlanMode tool
- Let user approve plan before execution

**If user declines or `is_complex: false`:**
- Proceed with direct implementation

## 3. Claim and Setup

```bash
# Claim it (assign self, update status labels)
gh issue edit $ARGUMENTS \
  --add-assignee @me \
  --remove-label "status::open" \
  --remove-label "status::ready" \
  --remove-label "status::backlog" \
  --add-label "status::active"
```

### 3.5 Branch Setup

Create a feature branch from the default branch:

```bash
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name')
git fetch origin
git checkout -b $ARGUMENTS-<short-slug-from-title> origin/$DEFAULT_BRANCH
```

**Branch naming:** `<issue-number>-<short-slug>` (e.g., `42-fix-auth-timeout`)

Generate the slug from the issue title: lowercase, spaces to hyphens, strip special chars, max 50 chars.

## 4. Decide Execution Mode (Autonomy-Based)

**Model selection (above) determines WHICH MODEL to use.**
**Autonomy determines EXECUTION MODE (foreground vs background).**

| Autonomy | Mode | Behavior |
|----------|------|----------|
| 0-1 | **Interactive** | Coordinate with user, ask questions, work in foreground |
| 2-3 | **Background** | Spawn subagent with `run_in_background: true`, stay available |

### If Autonomy >= 2 (Background Mode)

Spawn implementation subagent in background:

```
Task tool with:
  - run_in_background: true
  - prompt: |
      Implement GitHub issue #<number>: <title>

      ## Acceptance Criteria
      <from issue body>

      ## Branch
      Already on branch: <branch-name>

      ## Instructions
      0. Read project coding standards and conventions first
      1. Explore relevant code to understand context
      2. Implement the feature/fix
      3. Run project linter/tests if configured
      4. Commit changes with descriptive message
      5. Update issue checklist as you complete items
      6. Report summary of changes made

      ## Checklist Maintenance
      When you complete acceptance criteria items, update the issue:
      ```bash
      gh issue view <number> --json body -q '.body' > /tmp/desc.md
      # Update checkboxes: - [ ] -> - [x] for completed items
      gh issue edit <number> --body-file /tmp/desc.md
      ```

      Work autonomously. Do not ask questions - make reasonable decisions.
```

Report to user:
```
## Started: #<number> <title>

**Mode:** Background (autonomy::<level>)
**Branch:** <branch-name>

Implementation running in background. I'm available for other work.

Check status anytime by asking "status?" or "status on #<number>"
When complete, run `/flow-ship` to create PR.
```

### If Autonomy < 2 (Interactive Mode)

Work in foreground with user coordination:

```
## Starting: #<number> <title>

**Mode:** Interactive (autonomy::<level>)
**Milestone:** <milestone>
**Size:** <size label>
**Branch:** <branch-name>

### Acceptance Criteria
<from issue body>

### Ready to work

This issue requires interactive coordination. I'll explore the codebase
and discuss the approach with you before implementing.
```

Then proceed with exploration and implementation, asking questions as needed.

**Checklist maintenance:** As you complete acceptance criteria, update the issue:
```bash
gh issue view <number> --json body -q '.body' > /tmp/desc.md
# Update checkboxes for completed items
gh issue edit <number> --body-file /tmp/desc.md
```

## 5. Handling "status?" Queries

When user asks about status of a background task:

```bash
# Check if task is still running
Read the output_file from the background task

# Report progress
"#<number> status: <in progress / completed / failed>
<summary of work done so far>"
```

## Notes

- **Model selection happens FIRST** (pre-flight complexity detection)
- **Autonomy determines execution mode** (foreground vs background)
- Background agents work autonomously -- they won't ask questions
- If scope changes significantly, update autonomy label and restart if needed
- `status::active` label signals to other agents this issue is claimed
- Branch naming: `<issue-number>-<short-slug>` (e.g., `83-fix-auth-timeout`)
- When done, use `/flow-ship` to close with learnings and create PR
- **Checklist maintenance:** Update issue checkboxes as you complete acceptance criteria -- don't leave it all for ship time

## Default Autonomy (if not labeled)

If issue has no autonomy label, use these defaults:
- `size::s` -> `autonomy::2` (background)
- `size::m` -> `autonomy::2` (background)
- `size::l` -> `autonomy::1` (interactive)
- No size label -> `autonomy::1` (interactive, safer default)

If no $ARGUMENTS provided:
1. Run `gh issue list --limit 10 --json number,title,labels`
2. Show available issues sorted by priority
3. Ask which one to start

---
description: FLOW Objective - Create a new issue with proper labels
---

**MODEL: Opus** (strategic planning always uses Opus)
**EXECUTION: Foreground**
Create a new objective (GitHub issue) with full context and acceptance criteria:

## Strategic Analysis

Using deep reasoning:

1. **Understand goal:** Parse user's objective description "$ARGUMENTS"
2. **Research context:**
   - Check existing issues for duplicates
   - Review `.context/` for relevant patterns
   - Check current milestone priorities
3. **Define acceptance criteria:**
   - Clear, testable outcomes
   - Technical specifications
   - User-facing impact
4. **Identify dependencies:**
   - Related issues
   - Technical prerequisites
   - Blocked by / blocks relationships
5. **Determine sizing and autonomy:**
   - Size estimate (`size::s`, `size::m`, or `size::l`)
   - Autonomy level (see below)

## Autonomy Level Selection

Choose based on scope, risk, and need for human oversight:

| Level | Label | When to Use | Background? |
|-------|-------|-------------|-------------|
| 0 | `autonomy::0` | Security-sensitive, unfamiliar territory, learning | No |
| 1 | `autonomy::1` | Needs guardrails, might have questions, unclear scope | No |
| **2** | `autonomy::2` | Clear scope, routine work, well-understood patterns | **Yes** |
| 3 | `autonomy::3` | Trusted, can merge own PRs (rare) | Yes |

**Default mapping by size:**
- `size::s` -> `autonomy::2` (small, clear, just do it)
- `size::m` -> `autonomy::2` (standard work)
- `size::l` -> `autonomy::1` (complex, needs coordination)

Override the default if the task involves:
- Security code -> `autonomy::0` or `autonomy::1`
- Database migrations -> `autonomy::1`
- New external integrations -> `autonomy::1`
- Breaking API changes -> `autonomy::0`
- Unfamiliar domain -> `autonomy::1`

## Issue Structure

Create well-formed issue:

```markdown
## Objective
<clear statement of what we're building>

## Why
<user value, business rationale>

## Acceptance Criteria
- [ ] <criterion 1>
- [ ] <criterion 2>
- [ ] <criterion 3>

## Technical Notes
<implementation hints, architecture decisions>
```

**Note:** Dependencies are managed dynamically during implementation, not pre-wired in issues. If a blocker is discovered during work, add `blocked::technical-dependency` label and note the blocking issue in a comment. Remove the label when unblocked.

## Create Issue

```bash
gh issue create \
  --title "<descriptive title>" \
  --label "severity::<level>,type::<type>,size::<size>,autonomy::<level>,status::ready" \
  --body "$(cat <<'EOF'
## Objective
<clear statement>

## Why
<rationale>

## Acceptance Criteria
- [ ] <criterion 1>
- [ ] <criterion 2>

## Technical Notes
<context>
EOF
)"
```

## Suggest Milestone Assignment

Based on objective content:
```
Suggested milestone: <milestone-name>

   This objective fits the <milestone> focus on <rationale>.

   Assign now? [y/n]
```

If yes:
```bash
gh issue edit <number> --milestone "<milestone>"
```

If no milestone fits, leave it unassigned -- it will be assigned during triage.

## Output

```
## Created: #<number> - <title>

**Milestone:** <milestone> (or "Pool - needs triage")
**Size:** <S/M/L>
**Autonomy:** <0/1/2/3> (<supervised/guided/autonomous/full>)
**Background eligible:** <Yes/No> (autonomy >= 2)

<issue summary>

Ready to start? Run /flow-start <number>
```

## Notes

- Always include autonomy label -- it controls execution mode in `/flow-start`
- Higher autonomy (2-3) enables background execution
- Lower autonomy (0-1) requires interactive coordination

# /odoo-spec - Lightweight requirements intake for agentic planning

Capture business requirements through a conversational interview and output an agent-optimized specification.

## Arguments
- `--create-stream` - Optional flag to create FLOW milestone and epic issue from spec

## What This Does

Interviews the product owner to extract:
- **Problem statement** (mandatory) - What business problem we're solving
- **Success criteria** (mandatory) - Testable, measurable outcomes
- **Scope boundaries** (mandatory) - What's in and explicitly out of scope
- **Constraints** (optional) - Technical, time, or dependency limitations
- **Actors** (optional) - People/systems involved
- **Open questions** (optional) - Unknowns to resolve before development

Outputs to `.context/specs/<slug>.md` in a format optimized for plan mode agents.

## Interview Flow

### 1. Problem Statement
Use AskUserQuestion to gather:
```
What business problem are we solving?
- Keep it to 1-2 sentences
- Focus on the "why" not the "how"
```

### 2. Success Criteria
Ask conversationally:
```
What does success look like? What are the measurable outcomes?
- Must be testable (not "improve UX" - instead "user completes flow in <3 clicks")
- Should be observable (not "better performance" - instead "API responds in <200ms")
```

Prompt user to provide 2-5 concrete criteria. Convert to checklist format.

### 3. Scope Boundaries
Ask:
```
What's IN scope for this work?
What's explicitly OUT of scope?
```

This is critical - helps agents avoid gold-plating and scope creep.

### 4. Optional Context

Ask conversationally if there are:
- **Constraints**: "Any technical limitations, time constraints, or dependencies we need to know about?"
- **Actors**: "Who or what systems are involved in this solution?" (skip for simple features)
- **Open Questions**: "Anything unclear that we need to figure out before starting development?"

Only include sections in output if user provides information.

## Generate Spec File

1. **Derive filename** from problem statement:
   - Convert to lowercase
   - Replace spaces with hyphens
   - Remove special characters
   - Truncate to reasonable length (~50 chars)
   - Example: "Nextcloud bidirectional sync" → `nextcloud-bidirectional-sync.md`

2. **Write to** `.context/specs/<slug>.md`:

```markdown
# Spec: <Title from Problem Statement>

## Problem Statement
<1-2 sentence problem description>

## Success Criteria
- [ ] <Testable criterion 1>
- [ ] <Testable criterion 2>
- [ ] <Testable criterion 3>

## Scope

### In Scope
- <Item 1>
- <Item 2>

### Out of Scope
- <Item 1>
- <Item 2>

## Constraints
<Only include if provided>
- <Constraint 1>

## Actors
<Only include if provided>
- <Actor 1>: <role/description>

## Open Questions
<Only include if provided>
- <Question 1>

---

**Created:** <YYYY-MM-DD>
**Status:** Active
```

## FLOW Integration (if --create-stream flag present)

### Create Milestone
```bash
gh api repos/{owner}/{repo}/milestones -X POST -f title="<Spec Title>" -f description="<Problem Statement>"
```

### Create Epic Issue
```bash
gh issue create \
  --title "Epic: <Spec Title>" \
  --body "## Specification
See: .context/specs/<slug>.md

## Problem Statement
<1-2 sentences>

## Success Criteria
<Copy from spec>

## Reference
This epic tracks implementation of the specification. Individual tasks will be broken out as separate issues." \
  --milestone "<Spec Title>" \
  --label "size/L" \
  --label "type/feature" \
  --label "autonomy/1"
```

**Note:** Always set both `size/*` AND `autonomy/*` labels on created issues.

Default autonomy by size:
- size/S -> autonomy/2
- size/M -> autonomy/2
- size/L -> autonomy/1

## Output Format

```
## Created Specification: <Title>

**File:** .context/specs/<slug>.md
**Created:** <date>

### Problem
<1 sentence summary>

### Success Criteria
- Criterion 1
- Criterion 2

[If --create-stream used]
### FLOW Integration
**Milestone:** "<Spec Title>"
**Epic Issue:** #<number>

Start work with: /flow-start <number>

[If --create-stream NOT used]
### Next Steps
Create FLOW stream with: /odoo-spec --create-stream
Or start planning directly with the spec file.
```

## Creating Issues from Specs

When breaking a spec into individual issues, **always set both size and autonomy labels**:

```bash
gh issue create \
  --title "Feature XYZ" \
  --body "..." \
  --milestone "Stream Name" \
  --label "size/M" \
  --label "autonomy/2" \
  --label "type/feature"
```

**Default autonomy by size:**
- size/S -> autonomy/2 (autonomous background execution)
- size/M -> autonomy/2 (autonomous background execution)
- size/L -> autonomy/1 (guided interactive work)

**Override for sensitive work:**
- Security/auth -> autonomy/1 or autonomy/0
- Database migrations -> autonomy/1
- Breaking changes -> autonomy/0

## Tips for Good Specs

- **Problem statements** should describe business value, not technical solutions
- **Success criteria** must be binary (pass/fail) - avoid subjective measures
- **Scope boundaries** are as important as features - explicitly call out what we're NOT doing
- **Constraints** should be real limitations, not assumed ones
- **Keep it tight** - if the spec is >1 page, the problem is too big; break it down

## Example Usage

```
User: /odoo-spec
Claude: [Asks about problem statement]
User: We need to sync Odoo documents with Nextcloud bidirectionally
Claude: [Asks about success criteria]
User: Files uploaded in Odoo appear in Nextcloud, changes sync both ways, works with folders
Claude: [Continues interview...]
Claude: [Generates .context/specs/nextcloud-bidirectional-sync.md]
```

With stream creation:
```
User: /odoo-spec --create-stream
[After interview]
Claude: Created milestone "Nextcloud Sync" and epic issue #30
```

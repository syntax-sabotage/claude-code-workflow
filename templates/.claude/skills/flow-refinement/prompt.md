---
description: FLOW Refinement - Architectural analysis to make tickets implementation-ready
---

<!--
  ARCHITECTURAL SKILL - Deep codebase analysis + ticket enrichment.
  Produces approach guidance, NOT production code.
  Batch mode is the flagship -- cross-ticket analysis is the real value.
-->

**MODEL:** opus (architectural reasoning requires deep analysis)
**EXECUTION:** foreground (single) / background (batch/pipeline)

## Usage

```
/flow-refinement <number>                         # single issue
/flow-refinement --batch <number> <number> ...    # explicit list
/flow-refinement --milestone <name>               # all ready in milestone
/flow-refinement --pipeline                       # all ready issues
/flow-refinement --pipeline --runner-only         # only runner-eligible
```

Parse mode and options from `$ARGUMENTS`.

---

## Phase 1: Gather Context

Load architectural context ONCE before analyzing any tickets:

1. **AI Rules** -- read `.context/ai-rules.md` (coding standards, naming, architecture constraints)
2. **Glossary** -- read `.context/glossary.md` (domain terms)
3. **Anti-patterns** -- read `.context/anti-patterns.md` (patterns to prevent)
4. **Architecture decisions** -- scan `.context/architecture/` for relevant ADRs (if directory exists)
5. **Substrate** -- read `.context/substrate.md` for project overview and dependency tree

This context stays loaded for all tickets in the batch.

---

## Phase 2: Fetch Issues

### Single mode (`/flow-refinement <number>`)

```bash
gh issue view <number> --json title,body,labels,milestone,assignees
```

### Batch mode (`--batch <number> ...`)

Fetch each issue by number.

### Milestone mode (`--milestone <name>`)

```bash
gh issue list --milestone "<name>" --label "status::ready" --state open --json number,title,body,labels --limit 100
```

### Pipeline mode (`--pipeline`)

```bash
gh issue list --label "status::ready" --state open --json number,title,body,labels --limit 100
```

If `--runner-only`, further filter to `autonomy::2` or `autonomy::3`, `size::s` or `size::m`, no `blocked::*` labels (same eligibility as `/flow-runner`).

---

## Phase 3: Per-Ticket Analysis

For EACH issue, perform deep analysis. This is the core of the skill.

### 3a. Parse the ticket

Extract from the issue:
- Title, description, labels (status, severity, size, autonomy, type, blocked)
- Existing acceptance criteria (look for `- [ ]` checkboxes)
- Any technical notes already present

### 3b. Identify affected code

Using codebase search:

1. **Keyword extraction** -- pull domain terms from title + description
2. **Codebase search** -- use `Grep` to find concrete file paths:
   - Search for model names, class names, function names mentioned in the issue
   - Search for related business logic patterns
3. **Dependency trace** -- identify which modules depend on affected code (blast radius)

Output: list of `file:line` references.

### 3c. Determine architectural approach

Based on the issue type and affected code:

- **For feature tickets:** Which module owns this? New component or extension of existing? What's the migration story?
- **For performance tickets:** What's the current implementation pattern? What's the target pattern? What's the expected improvement?
- **For bug tickets:** Where does the defect likely live? What's the fix strategy? What regression risk exists?
- **For test tickets:** What test patterns exist in the codebase? Which base classes to use? What fixtures are needed?
- **For spike tickets:** What questions must be answered? What's the decision framework? What are the options with trade-offs?

Constrain yourself: describe the APPROACH and CONSTRAINTS, not the implementation. Concrete file paths and line numbers are fine. Full implementations are not.

### 3d. Assess dependencies

- **Blocks:** Does this ticket block other open tickets?
- **Blocked by:** Does this depend on another ticket being done first?
- **Shared infrastructure:** Does this ticket need something that other tickets also need?

Cross-reference against ALL open issues from the fetch.

### 3e. Assess risk and blast radius

Rate each:

| Dimension | Low | Medium | High |
|-----------|-----|--------|------|
| **Scope** | Single file/component | Multiple files in one module | Cross-module changes |
| **Data** | No schema change | New fields (safe) | Field type change / migration |
| **Integration** | No external touchpoints | Internal API changes | External API / third-party |
| **Regression** | Isolated feature | Shared utility/mixin | Core model / widely-used component |

Overall risk: Low / Medium / High / Critical

### 3f. Validate or draft acceptance criteria

- If the issue already has `- [ ]` checkboxes: validate they're specific and testable. Flag vague ones.
- If no acceptance criteria exist: draft 3-5 concrete, testable criteria.
- Each criterion should be verifiable by code review, automated test, or manual check.

### 3g. Reassess autonomy

Based on the analysis, confirm or recommend adjustment:
- If risk is Low + approach is clear pattern -> confirm `autonomy::2` or suggest upgrade to `autonomy::3`
- If risk is Medium + some ambiguity -> confirm `autonomy::2` or suggest downgrade to `autonomy::1`
- If risk is High or cross-module or external integration -> suggest `autonomy::1` or `autonomy::0`
- If a previously `autonomy::1` ticket now has clear approach after refinement -> suggest upgrade to `autonomy::2` (this is the force multiplier)

---

## Phase 4: Post Refinement Comment

For each refined ticket, post a structured comment to the GitHub issue.

### Comment template

```markdown
## Refinement -- Architectural Analysis

### Affected Code
| File | Lines | Impact |
|------|-------|--------|
| `<file>:<line>` | <range> | <what changes> |

### Approach
<2-4 sentences: strategy, pattern to follow, constraints to respect>

### Dependencies
- **Requires:** #<number> or "none"
- **Enables:** #<number> or "none"
- **Shared with:** #<number> -- shared infrastructure note

### Risk Assessment
| Dimension | Rating |
|-----------|--------|
| Scope | <Low/Medium/High> |
| Data | <Low/Medium/High> |
| Integration | <Low/Medium/High> |
| Regression | <Low/Medium/High> |
| **Overall** | **<Low/Medium/High/Critical>** |

### Acceptance Criteria
- [ ] <criterion 1>
- [ ] <criterion 2>
- [ ] <criterion 3>

### Autonomy
Current: `autonomy::<N>` -> Recommended: `autonomy::<N>` <rationale if changed>

---
_Refined by Architect -- <date>_
```

### Post the comment

```bash
gh issue comment <number> --body "<comment>"
```

### Update labels (if autonomy changed)

Only if the analysis recommends a different autonomy level:

```bash
gh issue edit <number> \
  --remove-label "autonomy::<old>" --add-label "autonomy::<new>" --add-label "refined"
```

If autonomy unchanged, just add the `refined` label:

```bash
gh issue edit <number> --add-label "refined"
```

---

## Phase 5: Cross-Ticket Analysis (batch/pipeline modes only)

After all individual tickets are refined, produce a cross-cutting summary. This is the batch mode payoff.

### 5a. Dependency graph

Build a directed graph of ticket dependencies discovered during analysis:

```
#42 --> #43  (both touch same core module)
#44 --> #45  (shared data pattern)
#46 --> #44  (depends on pattern from #44)
```

### 5b. Shared infrastructure

Identify common needs across tickets:
- Shared utilities or base classes
- Common migration steps
- Repeated patterns that should be abstracted (but ONLY if 3+ tickets need it)

### 5c. Recommended processing order

Suggest optimal sequencing:

```
Batch 1 (parallel-safe): #42, #43, #47  -- independent fixes
Batch 2 (sequential):    #44 -> #46     -- pattern dependency
Batch 3 (parallel):      #45, #48       -- independent features
```

### 5d. Autonomy promotions

List tickets whose autonomy can be upgraded now that approach is clear:
```
#48  autonomy::1 -> autonomy::2  (approach now clear after refinement)
#50  autonomy::1 stays           (needs external data, keep supervised)
```

---

## Output

### Single mode

Print the refinement analysis inline (same structure as the comment), then confirm it was posted.

```
REFINED: #<number> -- <title>

<full analysis>

Comment posted. Label: refined. Autonomy: <unchanged | N -> M>
```

### Batch/pipeline mode

Print per-ticket summaries (compact) + cross-ticket analysis:

```
REFINEMENT REPORT                              <date>

 REFINED (<n> tickets)
 #     Title                               Risk   A    Change
 #42   perf: optimize query cache          Low    3    --
 #43   feat: add export endpoint           Med    2    --
 #44   perf: batch data fetch              Med    2    --
 #48   spike: auth provider switch         Med    1->2  promoted

 DEPENDENCY GRAPH
 #44 -> #46  (shared data pattern)
 #42, #43, #47  (independent -- parallel safe)

 PROCESSING ORDER
 Batch 1 (parallel): #42, #43, #47
 Batch 2 (sequential): #44 -> #46
 Batch 3 (parallel): #45, #48

 AUTONOMY CHANGES
 #48  autonomy::1 -> autonomy::2  (approach clarified by refinement)

 RUNNER IMPACT
 Before: <n> eligible. After: <m> eligible  (+<diff> promoted)
```

---

## Guardrails

1. **No code in comments.** Approach descriptions only. If you catch yourself writing a function body or query, you've gone too far. File paths and line numbers are fine. Method signatures as references are fine. Implementations are not.

2. **No description overwrites.** Post COMMENTS, don't edit the original issue description. The original is the "what" (product intent). Your comment is the "how" (architectural guidance). They serve different audiences.

3. **No status changes.** Refinement doesn't change `status::ready` or `status::backlog`. It adds the `refined` label. That's it. Don't promote backlog tickets to ready -- that's a product decision, not an architectural one.

4. **Autonomy changes are advisory.** Post the recommendation in the comment. Only actually update the label if the change is clearly justified by the analysis (e.g., approach went from ambiguous to concrete). When in doubt, recommend but don't change.

5. **Don't refine tickets in `status::active` or `status::review`.** Those are already being worked on. Refinement is for tickets waiting in the queue. If asked to refine an active ticket, warn and confirm.

6. **Batch mode: cap at 15 tickets per run.** Deep architectural analysis has diminishing returns beyond this. If pipeline yields more, process the top 15 by severity and report the remainder as "queued for next refinement pass."

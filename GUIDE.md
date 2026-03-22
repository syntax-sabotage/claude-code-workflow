# Claude Code Workflow -- Setup Guide

A practical workflow system for Claude Code that combines institutional memory
(`.context/`), quality enforcement (hooks), multi-agent coordination (workstations),
and GitHub-native task management (skills).

**Prerequisites:** Claude Code installed, `gh` CLI installed and authenticated,
Git 2.15+.

---

## Part 1: The CLAUDE.md Hierarchy

Claude Code reads `CLAUDE.md` files at multiple levels. This creates cascading
context -- each level adds specificity:

```
~/.claude/CLAUDE.md              # Global -- your personal preferences, always loaded
~/projects/CLAUDE.md             # Directory -- shared patterns for project groups
~/projects/my-app/CLAUDE.md      # Project -- specific rules for this codebase
~/projects/my-app-Dev1/CLAUDE.md # Workstation -- role-bound agent instructions
```

### Level 1: Global (~/.claude/CLAUDE.md)

Your personal AI configuration. Sets communication style and tells Claude Code
about the `.context/` system.

Copy `templates/CLAUDE.md.global` and customize.

Key sections:
- Communication style preferences
- Instructions to read `.context/substrate.md` on session start
- Instructions to read `.context/ai-rules.md` before writing code
- The override principle: .context docs take precedence over generic training

### Level 2: Directory

Shared conventions for a group of related projects. Sets tech stack standards,
common mistakes to avoid, and agent role definitions.

Copy `templates/CLAUDE.md.directory` and customize.

### Level 3: Project

Project-specific rules: framework version compliance, language conventions,
security requirements, and workflow skills reference.

Copy `templates/CLAUDE.md.project` and customize.

### Level 4: Workstation

Role-bound instructions for a specific agent. Includes completion standards,
git safety rules, and scope boundaries.

Copy `templates/CLAUDE.md.workstation` and customize per workstation.

See [Part 5: Workstations](#part-5-workstations) for full setup.

---

## Part 2: The .context Knowledge System

A folder of structured documentation that Claude Code reads before working.
This is institutional memory -- it survives context window resets.

### Core Files

```
.context/
├── substrate.md                  # Navigation hub -- READ FIRST
├── ai-rules.md                   # Hard coding constraints
├── anti-patterns.md              # What NOT to do (with examples)
├── glossary.md                   # Domain terminology
├── debt.md                       # Technical debt tracker
├── handover/                     # Per-workstation session state
│   ├── dev1.md
│   └── architect.md
└── architecture/decisions/       # ADRs -- why decisions were made
    ├── ADR-TEMPLATE.md
    └── ADR-001-*.md
```

### Setup

```bash
# Copy all templates
cp -r templates/.context your-project/.context

# Fill in the templates -- replace [PLACEHOLDERS]
# Start with substrate.md (navigation hub), then ai-rules.md
```

### How Agents Use It

| When | Agent Reads |
|------|------------|
| Session start | `substrate.md` (overview), handover file (previous state) |
| Before writing code | `ai-rules.md`, `glossary.md` |
| Before refactoring | `debt.md`, `anti-patterns.md` |
| Architecture questions | `architecture/decisions/` |
| Domain terminology | `glossary.md` |

### The Override Principle

If `.context/ai-rules.md` says "use snake_case for variables" but Claude's
training suggests camelCase, the agent follows `.context/`. This is the single
most important design principle: project documentation overrides generic training.

---

## Part 3: Quality Enforcement Hooks

Hooks are Python scripts that run automatically during Claude Code sessions.
They enforce quality standards without requiring agent discipline.

### Setup

```bash
mkdir -p .claude/hooks
cp templates/.claude/hooks/*.py .claude/hooks/
cp templates/.claude/hooks/patterns.json .claude/hooks/
chmod +x .claude/hooks/*.py
```

### Hook Reference

| Hook | Trigger | What It Does |
|------|---------|-------------|
| `session-debt.py` | PostToolUse (Bash) | Logs errors/warnings to `.flow/session-debt.jsonl` |
| `check-session-debt.py` | Before shipping | Blocks PR creation if unresolved debt exists |
| `clear-session-debt.py` | Utility | Clears the debt ledger (called at session start) |
| `session-context.py` | Session start | Surfaces unreflected learnings, clears previous debt |
| `failure-logger.py` | PostToolUse (Bash) | Captures failures to `.flow/learnings.jsonl` |
| `pre-edit-guard.py` | PreToolUse (Edit/Write) | Warns on anti-pattern matches in code edits |

### How Session Debt Works

1. Agent runs a command that produces an error
2. `session-debt.py` catches it and logs to `.flow/session-debt.jsonl`
3. Agent continues working (hook never blocks)
4. When agent tries to ship (`/flow-ship`), `check-session-debt.py` checks the ledger
5. If unresolved items exist, shipping is blocked
6. Agent must fix the issues or explicitly justify them

This enforces the **Error Ownership** completion standard: if you caused it,
you fix it before shipping.

### Customizing Patterns

Edit `patterns.json` to add anti-patterns specific to your framework:

```json
{
  "patterns": {
    "py": [
      {
        "id": "PY_CUSTOM",
        "regex": "your_regex_here",
        "severity": "warn",
        "message": "Explanation of why this is bad."
      }
    ]
  }
}
```

Supported file types: `py`, `ts`, `tsx`, `js`, `jsx`, `go`, `rs`, `rb`, `xml`.
Add more by extending `get_file_type()` in `pre-edit-guard.py`.

---

## Part 4: GitHub Workflow with Skills

Skills are slash commands that agents invoke during sessions. They integrate
Claude Code with GitHub for issue-driven development.

### Core Skills

| Skill | Purpose |
|-------|---------|
| `/flow-resume` | Start session -- load handover state, clear previous debt |
| `/flow-start <#>` | Pick up a GitHub issue, create branch, load context |
| `/flow-ship` | Check session debt, commit, push, create PR |
| `/flow-handover` | End session -- save state to handover file |
| `/flow-status` | Show current work state across workstations |
| `/flow-reflect` | Synthesize learnings from closed issues into `.context/` |
| `/flow-refinement <#>` | Deep analysis to make a ticket implementation-ready |
| `/flow-runner` | Autonomous mode -- picks up eligible issues |
| `/flow-triage` | Categorize and prioritize open issues |

### GitHub Labels

Set up labels for your repository (run once):

```bash
# Autonomy levels
gh label create "autonomy::0" --color "FEF2C0" --description "Supervised"
gh label create "autonomy::1" --color "FBCA04" --description "Guided"
gh label create "autonomy::2" --color "0075CA" --description "Autonomous"
gh label create "autonomy::3" --color "5319E7" --description "Full trust"

# Size
gh label create "size::xs" --color "E8F5E9"
gh label create "size::s" --color "BFD4F2"
gh label create "size::m" --color "7CB3F7"
gh label create "size::l" --color "1D76DB"
gh label create "size::xl" --color "0D47A1"

# Status
gh label create "status::backlog" --color "EDEDED"
gh label create "status::ready" --color "0E8A16"
gh label create "status::active" --color "FBCA04"
gh label create "status::review" --color "5319E7"

# Type
gh label create "type/bug" --color "D73A4A"
gh label create "type/feature" --color "0075CA"
gh label create "type/debt" --color "CFD3D7"
gh label create "type/security" --color "B60205"

# Role assignment
gh label create "role::developer" --color "0075CA"
gh label create "role::architect" --color "5319E7"
gh label create "role::reviewer" --color "FBCA04"
```

### The Workflow

```
/flow-resume                  # Load context from last session
/flow-start 42                # Pick up issue #42, create branch
  ... implement ...           # Agent works on the issue
/flow-ship                    # Session debt check -> commit -> PR
/flow-handover                # Save state for next session
```

---

## Part 5: Workstations

Workstations are persistent git worktrees, each bound to a specific agent role.
This is optional -- start without workstations and add them when you need
parallel agents.

### When to Use Workstations

- You want multiple agents working simultaneously
- You need clean context separation between roles
- Your project is large enough that a single agent can't hold all context

### Quick Setup

```bash
# Create workstation branches
git checkout -b dev1 && git push -u origin dev1 && git checkout main
git checkout -b reviewer && git push -u origin reviewer && git checkout main

# Create worktrees
git worktree add ../your-project-Dev1 dev1
git worktree add ../your-project-Reviewer reviewer

# Set up role-bound CLAUDE.md in each
# (customize from templates/CLAUDE.md.workstation)

# Protect CLAUDE.md from merge overwrites
echo "CLAUDE.md merge=ours" >> .gitattributes
git config merge.ours.driver true
```

See [docs/WORKSTATIONS.md](docs/WORKSTATIONS.md) for the full guide.

---

## Part 6: Completion Standards

Non-negotiable rules enforced on every workstation. These exist because AI agents
have systematic biases toward declaring work complete prematurely.

### Error Ownership

If you caused it during this session, you fix it. No "that's unrelated" excuses.

### Anti-Deferral

If it's in the acceptance criteria, do it now. "Too much work" is not a valid
deferral reason. Flag scope concerns BEFORE starting, not after.

### Definition of Done

All AC items checked, no new errors, no bare TODOs, session debt clean,
CHANGELOG updated, self-review completed.

### Self-Review

Re-read the original issue before shipping. Compare what was requested against
what was implemented. Report gaps explicitly.

See [examples/completion-standards.md](examples/completion-standards.md) for the
full reference.

---

## Part 7: Onboarding an Existing Project

### Quick Start (15 minutes)

1. **Copy templates:**
   ```bash
   cp -r templates/.context your-project/.context
   cp -r templates/.claude your-project/.claude
   cp -r templates/.flow your-project/.flow
   cp templates/CLAUDE.md.project your-project/CLAUDE.md
   ```

2. **Fill in substrate.md** -- your project overview, modules, tech stack

3. **Fill in ai-rules.md** -- your coding standards and conventions

4. **Fill in glossary.md** -- your domain terms (at least core entities)

5. **Customize patterns.json** -- add anti-patterns for your framework

6. **Start using it:**
   ```bash
   cd your-project
   claude
   # Agent reads .context/substrate.md, loads rules, starts working
   ```

### Extract Knowledge from Existing Codebase

Use Claude Code to analyze your project and populate `.context/`:

```
Analyze this codebase: tech stack, directory structure, key entry points,
database setup, auth approach. Give me a summary.
```

```
Search for technical debt: TODO/FIXME/HACK comments, complex functions,
inconsistent patterns, hardcoded values. List with file references.
```

```
Extract domain terminology: model definitions, enum types, service classes.
Create a glossary with Term, Definition, Where Used.
```

---

## Part 8: Estimation for Human+AI Teams

Traditional estimation (story points, developer days) doesn't work for human+AI
teams. Agent coding speed is not the bottleneck -- human attention is.

### Three Units

| Unit | What It Measures |
|------|-----------------|
| **Session** | One focused human+agent block (1-3 hours of human time) |
| **Agent-slot** | One agent working independently (parallelizable) |
| **Gate** | A human decision/review point |

### Autonomy Reduces Gates

| Level | Gates | Human Time |
|-------|-------|-----------|
| `autonomy::0` | Many | ~1 hour/ticket |
| `autonomy::1` | 2 (approve approach + review PR) | ~20-30 min |
| `autonomy::2` | 1 (review PR only) | ~10 min |
| `autonomy::3` | 0 (agent ships, human merges) | ~2 min |

Promoting tickets from `autonomy::1` to `autonomy::2` via thorough refinement
doubles the human's effective throughput. Refinement is the highest-leverage
activity.

See `templates/.context/architecture/decisions/ADR-002-agentic-estimation-model.md`
for the full framework.

---

## Quick Reference

### File Structure

```
your-project/
├── CLAUDE.md                     # Project-level AI context
├── .gitattributes                # Merge protection for CLAUDE.md
├── .context/                     # Institutional memory
│   ├── substrate.md              # Navigation hub
│   ├── ai-rules.md              # Coding constraints
│   ├── anti-patterns.md         # What not to do
│   ├── glossary.md              # Domain terminology
│   ├── debt.md                  # Tech debt tracker
│   ├── handover/                # Per-workstation state
│   └── architecture/decisions/  # ADRs
├── .claude/
│   └── hooks/                   # Quality enforcement
│       ├── session-debt.py
│       ├── check-session-debt.py
│       ├── clear-session-debt.py
│       ├── session-context.py
│       ├── failure-logger.py
│       ├── pre-edit-guard.py
│       └── patterns.json
└── .flow/
    ├── state.json               # Cross-workstation state (gitignored)
    └── .gitignore
```

### Typical Session

```bash
cd your-project-Dev1
claude
# /flow-resume         -> loads context
# /flow-start 42       -> picks up issue
# ... work ...
# /flow-ship           -> debt check, commit, PR
# /flow-handover       -> saves state
```

---

## TL;DR

1. **CLAUDE.md hierarchy** -- Global -> Directory -> Project -> Workstation
2. **.context system** -- Institutional memory that survives context resets
3. **Hooks** -- Automated quality enforcement (session debt, anti-patterns)
4. **Skills** -- Slash commands for GitHub-native workflow
5. **Workstations** -- Named git worktrees per agent role (optional)
6. **Completion standards** -- Error ownership, anti-deferral, self-review

Start with `.context/` and hooks. Add workstations when you need parallel agents.

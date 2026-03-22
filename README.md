# FLOW — Human-Agent Team Workflow for Claude Code

FLOW is a structured workflow for software teams that combine one human with multiple AI agents. It uses GitHub natively — no external tools, no dashboards, no middleware.

Built and battle-tested in production with a single developer and 7 AI agents shipping a multi-module enterprise software suite.

## What's In This Repo

```
templates/
├── .context/           # Project knowledge system — institutional memory for agents
├── .claude/skills/     # 19 slash commands for Claude Code (FLOW lifecycle + GitHub)
├── .claude/hooks/      # Quality enforcement hooks (session debt, failure logging)
├── .flow/              # Shared state across worktrees
├── CLAUDE.md.*         # Cascading context templates (global, directory, project, workstation)
└── .gitattributes      # Merge protection for branch-specific files

examples/               # Completion standards, anti-deferral rules, role definitions
docs/                   # Workstation setup, migration guide
```

## The Team Model

A FLOW team has one human and multiple named agents, each bound to a role:

| Role | What They Do | Trust Level |
|------|-------------|-------------|
| **Architect** | Designs systems, writes ADRs, triages issues, refines tickets | Strategic |
| **Developer** (×2) | Implements tickets, writes tests, ships PRs | Tactical |
| **Reviewer** (×2) | Reviews PRs, flags issues, applies labels | Quality |
| **Data Engineer** | Writes data scripts, migrations, audits | Cautious |
| **Content Engineer** | Creates docs, listings, website content | Creative |

Each agent gets a **named workstation** — a persistent git worktree with its own branch, Docker stack, and role-bound `CLAUDE.md`:

```
your-project/              # main — shared state
your-project-Dev1/         # Developer 1 workstation
your-project-Dev2/         # Developer 2 workstation
your-project-Reviewer/     # Reviewer workstation
your-project-Architect/    # Architect workstation
```

## Core Concepts

### Institutional Memory (`.context/`)

Each project has a `.context/` folder with structured knowledge agents read before working:

```
.context/
├── substrate.md              # Navigation hub — read this first
├── ai-rules.md               # Coding standards, naming, architecture constraints
├── glossary.md                # Project-specific terminology
├── anti-patterns.md           # Known pitfalls with examples
├── debt.md                    # Tech debt tracker
├── handover/                  # Per-workstation session state
│   ├── dev1.md
│   └── architect.md
└── architecture/decisions/    # ADRs — why decisions were made
    ├── ADR-001-example.md
    └── ADR-TEMPLATE.md
```

This is institutional memory that survives context window resets. Agents read `.context/ai-rules.md` before writing any code.

### Autonomy Levels

Labels on GitHub issues set the trust boundary for agents:

| Label | Behavior | Human Time |
|-------|----------|------------|
| `autonomy::0` | Stop and ask at every decision | ~1 hour/ticket |
| `autonomy::1` | Agent proposes, human approves | ~20-30 min/ticket |
| `autonomy::2` | Agent executes, human reviews PR | ~10 min/ticket |
| `autonomy::3` | Agent ships, human merges | ~2 min/ticket |

**Force multiplier:** Promoting tickets from `autonomy::1` to `autonomy::2` via thorough refinement doubles the human's effective throughput.

### Estimation (Sessions, Gates, Slots)

FLOW doesn't use "developer days" or story points. The human's attention is the bottleneck, not agent coding speed.

| Unit | Definition |
|------|-----------|
| **Session** | One focused human+agent block (1-3 hours) |
| **Agent-slot** | One agent working independently (parallelizable) |
| **Gate** | A point where the human must review/approve |

A `size::m` ticket takes an agent 30-60 minutes. The constraint is how many gates the human can process.

### Completion Standards

Non-negotiable rules enforced via CLAUDE.md on every workstation:

- **Error Ownership:** If you caused it, fix it before moving on.
- **Anti-Deferral:** "Too much work" is not a valid reason to defer acceptance criteria. Flag scope concerns BEFORE starting.
- **Definition of Done:** ALL acceptance criteria checked, no new errors, no bare TODOs.
- **Self-Review:** Re-read the issue before shipping. Report gaps explicitly.

### Skills (Slash Commands)

| Skill | What It Does |
|-------|-------------|
| `/flow-start <#>` | Pick up a GitHub issue, create branch, load context |
| `/flow-ship` | Commit, push, create PR with self-review gates |
| `/flow-handover` | End session, capture state for next session |
| `/flow-resume` | Start session, restore context from last handover |
| `/flow-reflect` | Synthesize learnings from closed issues |
| `/flow-refinement <#>` | Deep codebase analysis to make tickets implementation-ready |
| `/flow-runner` | Autonomous ticket processing (picks up eligible issues) |
| `/flow-status` | Show current work state across workstations |
| `/flow-triage` | Categorize and prioritize open issues |

### Hooks (Quality Enforcement)

| Hook | When | What |
|------|------|------|
| `session-debt.py` | On errors/warnings | Logs to session debt ledger |
| `check-session-debt.py` | Before `/flow-ship` | Blocks shipping with unresolved debt |
| `failure-logger.py` | On command failures | Captures failures for `/flow-reflect` |
| `pre-edit-guard.py` | Before file edits | Prevents edits to protected files |
| `session-context.py` | On session start | Clears debt ledger, sets context |

## Quick Start

1. **Copy templates** to your project:
   ```bash
   cp -r templates/.context your-project/
   cp -r templates/.claude your-project/
   cp -r templates/.flow your-project/
   ```

2. **Fill in the templates** — replace `[PLACEHOLDERS]` in:
   - `.context/substrate.md` — your project overview
   - `.context/ai-rules.md` — your coding standards
   - `.context/glossary.md` — your domain terms

3. **Set up workstations** (optional, for multi-agent teams):
   ```bash
   git worktree add ../your-project-Dev1 dev1
   git worktree add ../your-project-Reviewer reviewer
   ```
   Copy `CLAUDE.md.workstation` to each, customize the role.

4. **Configure GitHub labels**:
   ```
   autonomy::0, autonomy::1, autonomy::2, autonomy::3
   size::xs, size::s, size::m, size::l, size::xl
   status::backlog, status::ready, status::active, status::review
   role::developer, role::architect, role::reviewer
   ```

5. **Start working**: `/flow-resume` to begin, `/flow-handover` to end.

See [GUIDE.md](GUIDE.md) for the full setup walkthrough.

## Design Principles

1. **GitHub is the coordination layer.** No external tools. Issues, labels, milestones, PRs.
2. **Context survives resets.** `.context/` is institutional memory that agents read every session.
3. **Autonomy is earned.** Default `autonomy::1`. Promote to `::2` via refinement, not trust.
4. **Human attention is the bottleneck.** Optimize for fewer gates, not faster agents.
5. **Agents finish what they start.** No partial completion. Flag scope issues before starting.

## License

MIT — use it however you want.

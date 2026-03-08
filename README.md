# FLOW

FLOW is a mixed human-agent team workflow for software projects. It is not an acronym. It is a way of structuring how humans and AI agents collaborate on a codebase — using GitHub natively, with clear role boundaries and trust levels.

## The team model

A FLOW team combines a human developer with specialized Claude agents:

| Role | Agent | Trigger |
|------|-------|---------|
| Human Dev | You | Direct work, setup, review decisions |
| Review Agent | K2SO | `/flow-review <MR#>` |
| Agentic Dev | Kleya | `/flow-runner start` |
| Agentic Dev | Cassian | `/flow-runner start` |

**K2SO** checks out a branch, runs a full review checklist, and posts findings as BLOCKER / WARNING / NOTE — then sets the review label. It does not merge.

**Kleya and Cassian** are agentic developers. They pick up issues, create branches, write code, open PRs. They run autonomously within their assigned trust level.

## Workstations and worktrees

Each agent gets a named git worktree — a full checkout of the repo at its own path, with an isolated Docker stack:

```
your-project/          # main — shared state, CI
your-project-Kleya/    # Kleya's workstation
your-project-Cassian/  # Cassian's workstation
your-project-K2SO/     # K2SO's review station
your-project-109/      # ephemeral issue worktree
```

**Named workstations** are persistent. Each has its own branch, staging environment, and Docker stack. `./start.sh` auto-detects which worktree it is running from.

**Ephemeral issue worktrees** are created per issue via `/flow-worktree create <#>`. Code-only — no Docker stack.

**Shared state** (`.flow/state.json`, cost logs) always lives in the main worktree. Agents read it; they never write to each other's paths.

Detection rule: `project-[A-Za-z]+` = workstation. `project-[0-9]+` = issue worktree.

## GitHub as the coordination layer

FLOW is GitHub-native. There are no external tools, no dashboards, no middleware. Everything lives in Issues, Labels, and Milestones.

- **Issues** are the unit of work
- **Labels** control flow and trust levels
- **Milestones** define scope
- **PRs** trigger the review loop

Agents read GitHub state to decide what to work on next. The human sets the labels.

## Autonomy levels

Labels on issues set the trust boundary for agents:

| Label | Meaning |
|-------|---------|
| `autonomy::0` | Human does the work |
| `autonomy::1` | Agent proposes, human approves each step |
| `autonomy::2` | Agent executes, human reviews output |
| `autonomy::3` | Agent executes and merges without review |

Most work runs at `autonomy::2`. The human moves issues to `autonomy::3` only for well-understood, low-risk tasks.

## Institutional memory with `.context/`

Each project has a `.context/` folder containing structured knowledge for agents:

```
.context/
  substrate.md        # navigation hub — read this first
  ai-rules.md         # coding standards, naming conventions, architecture rules
  glossary.md         # project-specific terminology
  architecture/       # system design decisions
  auth/               # authentication and security patterns
  api/                # API conventions
  database/           # schema and model conventions
  debt.md             # known technical debt and priorities
```

Agents read `.context/ai-rules.md` before writing any code. The substrate.md explains what exists and why — not just what. This is institutional memory that survives context resets.

## Skills

| Skill | Who runs it | What it does |
|-------|------------|--------------|
| `/flow-runner start` | Agentic Dev | Pick up next issue, work it, open PR |
| `/flow-review <MR#>` | Review Agent | Review a PR, post findings, set label |
| `/flow-worktree create <#>` | Any agent | Create ephemeral worktree for an issue |

## Setup

See [flow-methodology.com/demo](https://flow-methodology.com/demo/) for a walkthrough of the full setup — team configuration, worktree initialization, and the first run.

## Repository

This repository contains the FLOW skills (slash commands) used by agents. Each skill is a markdown file in `.claude/commands/` that Claude Code executes when invoked.

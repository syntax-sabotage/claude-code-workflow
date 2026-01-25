# Claude Code Workflow

A practical workflow system for [Claude Code](https://claude.ai/code) that combines project knowledge documentation, GitHub-based task management, and multi-project coordination.

## What This Is

A set of conventions and templates for working effectively with Claude Code on real projects:

- **`.context/` system** - Structured project documentation that Claude reads on demand (based on [andrefigueira/.context](https://github.com/andrefigueira/.context))
- **CLAUDE.md hierarchy** - Cascading configuration from global preferences to project-specific rules
- **GitHub slash commands** - Custom skills for issue-driven development (`/gh-start`, `/gh-done`, etc.)
- **Session handover** - Context continuity between coding sessions
- **Multi-project patterns** - Coordinate work across related codebases

## Quick Start

### 1. Set up global config

Add to `~/.claude/CLAUDE.md`:

```markdown
## .context Project Knowledge System

When working in any project directory, check for a `.context/` folder. If present:

### On Session Start
1. Read `.context/substrate.md` first - it's the navigation hub
2. For coding tasks, read `.context/ai-rules.md` before writing any code
3. Check `.context/anti-patterns.md` to avoid known pitfalls

### Key Principle
The .context folder contains institutional knowledge about WHY decisions were made.
Prefer patterns documented there over generic best practices.
```

See [templates/global-claude-md.md](templates/global-claude-md.md) for the full template.

### 2. Add .context to your project

Copy the template folder:

```bash
cp -r templates/.context your-project/.context
```

Fill in the placeholders in each file:
- `substrate.md` - Project overview, tech stack, navigation
- `ai-rules.md` - Hard coding constraints
- `anti-patterns.md` - What NOT to do
- `glossary.md` - Domain terminology
- `SESSION_HANDOVER.md` - Current state

### 3. Add GitHub workflow commands

Copy the commands folder:

```bash
cp -r templates/.claude-commands your-project/.claude/commands
```

Set up labels (run once per repo):

```bash
gh label create "priority/critical" --color "B60205"
gh label create "priority/high" --color "D93F0B"
gh label create "priority/medium" --color "FBCA04"
gh label create "priority/low" --color "0E8A16"
gh label create "type/bug" --color "D73A4A"
gh label create "type/feature" --color "0075CA"
gh label create "type/debt" --color "CFD3D7"
gh label create "status/blocked" --color "FEF2C0"
gh label create "status/review" --color "5319E7"
```

### 4. Use the workflow

```bash
/gh-status              # See what needs attention
/gh-start 12            # Start work on issue #12
# ... code ...
/gh-done                # Create PR linked to issue
```

## Repository Structure

```
claude-code-workflow/
├── README.md                    # You are here
├── GUIDE.md                     # Full documentation
└── templates/
    ├── global-claude-md.md      # Add to ~/.claude/CLAUDE.md
    ├── .context/                # Copy to your project
    │   ├── substrate.md         # Project overview
    │   ├── ai-rules.md          # Coding constraints
    │   ├── anti-patterns.md     # What NOT to do
    │   ├── glossary.md          # Domain terms
    │   └── SESSION_HANDOVER.md  # Session state
    └── .claude-commands/        # Copy to .claude/commands/
        ├── gh-status.md         # Overview command
        ├── gh-start.md          # Start issue command
        ├── gh-done.md           # Create PR command
        └── gh-bug.md            # Report bug command
```

## The Five Core Files

| File | Purpose | When to Read |
|------|---------|--------------|
| `substrate.md` | Navigation hub, tech stack | Every session start |
| `ai-rules.md` | Hard coding constraints | Before writing ANY code |
| `anti-patterns.md` | What NOT to do | Before writing code |
| `glossary.md` | Domain vocabulary | When confused about terms |
| `SESSION_HANDOVER.md` | Current state, open tasks | Resuming work |

## Slash Commands

| Command | What It Does |
|---------|--------------|
| `/gh-status` | Show issues, PRs, current branch |
| `/gh-start <N>` | Assign issue N, create feature branch |
| `/gh-done` | Push changes and create PR |
| `/gh-bug` | Create bug issue from conversation |

## Documentation

- [GUIDE.md](GUIDE.md) - Full workflow documentation including:
  - CLAUDE.md hierarchy explained
  - Complete .context system setup
  - Onboarding existing projects
  - Multi-project coordination
  - Maintenance practices

## Why This Exists

Claude Code is powerful but works better with context. Instead of explaining your project's patterns, tech stack, and conventions every session, document them once and let Claude read them.

The `.context/` system captures institutional knowledge - not just what the code does, but why decisions were made. This prevents Claude from suggesting patterns your team already rejected, or using conventions that conflict with your codebase.

The GitHub workflow commands reduce friction in issue-driven development. Type `/gh-start 42` instead of manually assigning, creating branches, and remembering issue numbers.

## FLOW Methodology (Experimental)

The `flow-artifacts/` directory contains a concrete implementation of the [FLOW methodology](https://flow-methodology.com) - an AI-native, post-agile approach to software development.

```
flow-artifacts/
├── .flow/                    # Work coordination (dynamic)
│   ├── FLOW.md               # Hub - start here
│   ├── streams/              # Objective groupings
│   ├── objectives/           # Individual work units
│   ├── agents/               # Autonomy levels & handover
│   ├── metrics/              # Throughput, cycle time
│   └── ceremonies/           # Async rituals
└── .claude-commands/         # /flow-* slash commands
```

Key concepts:
- **Streams over sprints** - Related objectives flow continuously
- **Autonomy levels** - Trust boundaries for AI agents (Level 0-3)
- **Async ceremonies** - No mandatory meetings, event-triggered
- **Ship when ready** - No artificial sprint boundaries

See [flow-artifacts/.flow/FLOW.md](flow-artifacts/.flow/FLOW.md) for details.

## Credits

The `.context/` system is based on [andrefigueira/.context](https://github.com/andrefigueira/.context) by [Andre Figueira](https://github.com/andrefigueira). This repo extends the concept with GitHub workflow integration and multi-project patterns for Claude Code.

## License

MIT

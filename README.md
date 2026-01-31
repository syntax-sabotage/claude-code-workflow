# Claude Code Workflow

A practical workflow system for [Claude Code](https://claude.ai/code) that combines project knowledge documentation, GitHub-based task management, and multi-project coordination.

## What This Is

A production-tested workflow system for working effectively with Claude Code on real projects:

- **`.context/` system** - Structured project documentation that Claude reads on demand (based on [andrefigueira/.context](https://github.com/andrefigueira/.context))
- **CLAUDE.md hierarchy** - Cascading configuration from global preferences to project-specific rules
- **FLOW v2** - GitHub-native AI-native workflow (milestones, issues, labels)
- **Statusline integration** - Real-time project state in Claude Code
- **Slash commands** - Custom skills for issue-driven development
- **Session handover** - Context continuity between coding sessions

## What's New in v2

**January 2026** - Major update based on production learnings:

✨ **FLOW v2** - GitHub-native tracking (no more file-based objectives)
- Milestones = Streams
- Issues = Objectives
- Labels = Status/size/autonomy
- No merge conflicts, single source of truth

✨ **Statusline integration** - See active work in Claude Code statusline:
```
[Sonnet] #47 Implement sync | Invoice Pro | 1 blocked | 2 PR * | 45% | $0.23
```

✨ **Specs workflow** - Interview-based requirements capture for complex features

✨ **Advanced examples**:
- Real `.context/` patterns (GitHub integration, deployment docs, specs)
- Domain-specific commands (requirements, validation, deployment)
- Adaptable templates for any domain

✨ **Battle-tested** - Extracted from production Odoo deployment managing 60+ modules

See [FLOW_V2_MIGRATION.md](FLOW_V2_MIGRATION.md) for the evolution story.

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
├── README.md                         # You are here
├── GUIDE.md                          # Full documentation
├── FLOW_V2_MIGRATION.md              # v1 → v2 evolution guide
├── flow-artifacts/                   # FLOW v2 implementation
│   ├── .flow/
│   │   ├── FLOW.md                   # Hub
│   │   ├── statusline.sh             # Statusline integration
│   │   ├── update-state.sh           # State updater
│   │   └── .gitignore                # Ephemeral state
│   └── .claude-commands/             # /flow-* commands
└── templates/
    ├── global-claude-md.md           # Add to ~/.claude/CLAUDE.md
    ├── .context/                     # Basic .context templates
    │   ├── substrate.md
    │   ├── ai-rules.md
    │   ├── anti-patterns.md
    │   ├── glossary.md
    │   └── SESSION_HANDOVER.md
    ├── .context-examples/            # Advanced patterns (NEW)
    │   ├── README.md                 # How to use examples
    │   ├── github.md                 # GitHub integration
    │   └── specs-README.md           # Requirements workflow
    ├── .claude-commands/             # Basic GitHub commands
    │   ├── gh-status.md
    │   ├── gh-start.md
    │   ├── gh-done.md
    │   └── gh-bug.md
    └── .claude-commands-examples/    # Domain commands (NEW)
        ├── README.md                 # How to adapt
        ├── odoo-spec.md              # Requirements interview
        ├── odoo-validate.md          # Module validation
        └── vps-upgrade.md            # Deployment command
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

### GitHub Commands (Basic)

| Command | What It Does |
|---------|--------------|
| `/gh-status` | Show issues, PRs, current branch |
| `/gh-start <N>` | Assign issue N, create feature branch |
| `/gh-done` | Push changes and create PR |
| `/gh-bug` | Create bug issue from conversation |

### FLOW Commands (Advanced)

| Command | What It Does |
|---------|--------------|
| `/flow-status` | Query all milestones + issues via `gh` |
| `/flow-start <N>` | Claim issue, create branch, update statusline |
| `/flow-ship` | PR + merge + close issue + deploy |
| `/flow-resume` | Start session, query current state |
| `/flow-handover` | End session summary |
| `/flow-reflect <stream>` | Synthesize learnings → `.context/` |

### Domain-Specific Commands (Examples)

See [templates/.claude-commands-examples/](templates/.claude-commands-examples/) for adaptable patterns:

| Command | Purpose | Domain |
|---------|---------|--------|
| `/odoo-spec` | Interview-based requirements | Odoo |
| `/odoo-validate` | Module validation | Odoo |
| `/vps-upgrade` | Deploy + upgrade module | DevOps |

Adapt these for your domain (mobile, API, infrastructure, etc.).

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

## FLOW v2: GitHub-Native Workflow

The `flow-artifacts/` directory contains **FLOW v2** - a GitHub-native implementation of AI-native development that eliminates file-based tracking in favor of GitHub Issues, Milestones, and Labels.

```
flow-artifacts/
├── .flow/
│   ├── FLOW.md               # Hub - start here
│   ├── statusline.sh         # Claude Code statusline integration
│   ├── update-state.sh       # State updater (queries GitHub)
│   └── .gitignore            # state.json (cached, ephemeral)
└── .claude-commands/         # /flow-* slash commands
```

**Key improvements over v1:**
- **GitHub is source of truth** - No duplicate state, no merge conflicts
- **Statusline integration** - Real-time project state in Claude Code statusline
- **Specs workflow** - Requirements capture before implementation
- **Battle-tested** - Extracted from production Odoo deployment

**Core concepts:**
- **Streams = Milestones** - Related work flows together
- **Objectives = Issues** - Track work in GitHub
- **Autonomy levels** - Labels control AI agent trust boundaries (0-3)
- **Ship when ready** - No sprint boundaries

**Quick start:**
```bash
# Set up labels
gh label create "active" --color "0E8A16"
gh label create "size/M" --color "7CB3F7"
# ... (see FLOW.md for full list)

# Copy FLOW artifacts
cp -r flow-artifacts/.flow your-project/
cp -r flow-artifacts/.claude-commands/* your-project/.claude/commands/

# Start using
/flow-status              # See all work
/flow-start 42            # Claim issue, create branch
/flow-ship                # PR + merge + deploy
```

See [FLOW_V2_MIGRATION.md](FLOW_V2_MIGRATION.md) for evolution from v1 and [flow-artifacts/.flow/FLOW.md](flow-artifacts/.flow/FLOW.md) for details.

## Credits

The `.context/` system is based on [andrefigueira/.context](https://github.com/andrefigueira/.context) by [Andre Figueira](https://github.com/andrefigueira). This repo extends the concept with GitHub workflow integration and multi-project patterns for Claude Code.

## License

MIT

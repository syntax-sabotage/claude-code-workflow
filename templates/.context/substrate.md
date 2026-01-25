# Project Substrate

> <!-- One-line description of what this project does -->

**Quick Start**: See [CLAUDE.md](../CLAUDE.md) for AI assistant onboarding.

## Quick Navigation

| Domain | Purpose | Start Here |
|--------|---------|------------|
| [Architecture](./architecture/) | System design | overview.md |
| [Auth](./auth/) | Authentication | overview.md |
| [API](./api/) | Endpoints | endpoints.md |
| [Database](./database/) | Schema, models | schema.md |

<!-- Remove domains you don't need -->

## AI Usage Patterns

### Before Writing Code
```
Read: .context/ai-rules.md → .context/anti-patterns.md → relevant domain docs
```

### Task-Specific Loading

| Task | Load These Files |
|------|------------------|
| New API endpoint | `api/endpoints.md`, `auth/overview.md`, `database/models.md` |
| Database changes | `database/schema.md`, `glossary.md` |
| Auth modifications | `auth/overview.md`, `auth/security.md` |
| UI components | `ui/overview.md`, `ui/patterns.md` |
| Bug fixes | `anti-patterns.md`, relevant domain docs |

## Tech Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND                                 │
│  <!-- Your frontend stack -->                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         BACKEND                                  │
│  <!-- Your backend stack -->                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         DATA                                     │
│  <!-- Your data layer -->                                       │
└─────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
project/
├── src/                    # <!-- Describe -->
├── tests/                  # <!-- Describe -->
├── config/                 # <!-- Describe -->
└── ...
```

## Core Domain Concepts

| Entity | Description | Key Relationships |
|--------|-------------|-------------------|
| **User** | <!-- Description --> | <!-- Relationships --> |
| **...** | <!-- Add your entities --> | |

See [glossary.md](./glossary.md) for complete terminology.

## Key Files Reference

| Purpose | Path |
|---------|------|
| Database schema | `<!-- path -->` |
| API routes | `<!-- path -->` |
| UI components | `<!-- path -->` |
| Config | `<!-- path -->` |

## Environment Requirements

| Variable | Purpose | Required |
|----------|---------|----------|
| `DATABASE_URL` | Database connection | Yes |
| `AUTH_SECRET` | Session encryption | Yes |
| `...` | <!-- Add yours --> | |

## Decision History

| Date | Decision | Rationale |
|------|----------|-----------|
| <!-- Date --> | <!-- What --> | <!-- Why --> |

## GitHub Workflow

Task management via GitHub Issues with `/gh-*` slash commands:

| Command | Purpose |
|---------|---------|
| `/gh-status` | Overview of open issues, PRs, current branch |
| `/gh-start <issue#>` | Assign issue, create feature branch |
| `/gh-done` | Push changes, create PR linked to issue |
| `/gh-bug` | Create bug report from conversation context |

**Labels:** `priority/*` (critical/high/medium/low), `type/*` (bug/feature/debt/security), `status/*` (blocked/review)

## Complete File Index

```
.context/
├── substrate.md              # This file - navigation hub
├── ai-rules.md               # Non-negotiable coding rules
├── anti-patterns.md          # Patterns to avoid with examples
├── glossary.md               # Domain terminology reference
├── SESSION_HANDOVER.md       # Current state, open tasks
│
├── architecture/             # (optional)
│   └── overview.md
├── auth/                     # (optional)
│   └── overview.md
├── api/                      # (optional)
│   └── endpoints.md
├── database/                 # (optional)
│   └── schema.md
└── ui/                       # (optional)
    └── overview.md
```

## Related Documentation

- [ai-rules.md](./ai-rules.md) - Hard constraints for code generation
- [anti-patterns.md](./anti-patterns.md) - Patterns to avoid
- [glossary.md](./glossary.md) - Domain terminology
- [CLAUDE.md](../CLAUDE.md) - AI assistant quick-start

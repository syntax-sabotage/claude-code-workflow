# [YOUR_PROJECT] Substrate

> [One-line description: what this project does and who it's for.]

## Quick Navigation

| Domain | Purpose | Start Here |
|--------|---------|------------|
| [Architecture](./architecture/) | System design, ADRs | decisions/ |
| [Auth](./auth/) | Authentication flow | overview.md |
| [API](./api/) | Endpoints, protocols | endpoints.md |
| [Database](./database/) | Schema, models, migrations | schema.md |

<!-- Remove domains you don't need. Add project-specific ones. -->

## Module Inventory

| Module | Purpose | Status |
|--------|---------|--------|
| [YOUR_MODULE_1] | [What it does] | Active |
| [YOUR_MODULE_2] | [What it does] | Active |
| [YOUR_MODULE_3] | [What it does] | Planned |

## Dependency Tree

```
[YOUR_MODULE_1]
  └── [YOUR_MODULE_2] (depends on)
       └── [EXTERNAL_DEPENDENCY]
[YOUR_MODULE_3]
  └── [YOUR_MODULE_1] (depends on)
```

## Development Streams

Active workstreams for planning and milestone tracking.

| Stream | Milestone | Status | Key Issues |
|--------|-----------|--------|------------|
| [Stream name] | [GitHub/GitLab milestone] | Active | #1, #2, #3 |
| [Stream name] | [Milestone] | Planning | -- |

## Development Environment

| Component | Details |
|-----------|---------|
| Runtime | [YOUR_FRAMEWORK] [version] |
| Database | [PostgreSQL/MySQL/SQLite] [version] |
| Package manager | [npm/yarn/pnpm/pip/cargo/go mod] |
| Test runner | [jest/pytest/cargo test/go test] |
| CI/CD | [GitHub Actions/GitLab CI/Jenkins] |

### Quick Commands

```bash
# Install dependencies
[YOUR_INSTALL_COMMAND]

# Start development server
[YOUR_DEV_COMMAND]

# Run tests
[YOUR_TEST_COMMAND]

# Lint/format
[YOUR_LINT_COMMAND]
```

## Deployment Targets

| Environment | URL/Host | Branch | Notes |
|-------------|----------|--------|-------|
| Development | localhost:[PORT] | feature branches | Local Docker/native |
| Staging | [staging URL] | main | Auto-deploy on merge |
| Production | [prod URL] | release tags | Manual approval |

## AI Usage

### Before Writing Code
```
Read: .context/ai-rules.md -> .context/glossary.md -> relevant domain docs
```

### Task-Specific Loading

| Task | Load These Files |
|------|------------------|
| New feature | `ai-rules.md`, `glossary.md`, relevant domain docs |
| Bug fix | `anti-patterns.md`, relevant domain docs |
| Database change | `database/schema.md`, `glossary.md` |
| Architecture change | `architecture/decisions/`, `debt.md` |
| Refactoring | `debt.md`, `anti-patterns.md`, `ai-rules.md` |

## Key Files Reference

| Purpose | Path |
|---------|------|
| Entry point | `[YOUR_PATH]` |
| Database schema | `[YOUR_PATH]` |
| API routes | `[YOUR_PATH]` |
| Config | `[YOUR_PATH]` |
| Tests | `[YOUR_PATH]` |

## Decision History

| Date | Decision | Rationale | ADR |
|------|----------|-----------|-----|
| [DATE] | [What was decided] | [Why] | [ADR-NNN] |

## Complete File Index

```
.context/
├── substrate.md              # This file -- navigation hub
├── ai-rules.md               # Non-negotiable coding rules
├── anti-patterns.md          # Patterns to avoid with examples
├── glossary.md               # Domain terminology reference
├── debt.md                   # Technical debt tracker
├── handover/                 # Per-workstation session state
│   └── [workstation].md
└── architecture/
    └── decisions/            # Architecture Decision Records
        ├── ADR-TEMPLATE.md
        └── ADR-001-*.md
```

## Related Documentation

- [ai-rules.md](./ai-rules.md) -- Hard constraints for code generation
- [anti-patterns.md](./anti-patterns.md) -- Patterns to avoid
- [glossary.md](./glossary.md) -- Domain terminology
- [debt.md](./debt.md) -- Known technical debt
- [CLAUDE.md](../CLAUDE.md) -- AI assistant quick-start

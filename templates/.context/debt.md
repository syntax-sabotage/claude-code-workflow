# Technical Debt Tracker

Known technical debt items, prioritized for resolution.

## Active Debt

| ID | Description | Module | Severity | Effort | Status | Issue |
|----|-------------|--------|----------|--------|--------|-------|
| TD-001 | [Description of the debt item] | [module] | High | M | Open | #-- |
| TD-002 | [Description of the debt item] | [module] | Medium | S | In Progress | #-- |
| TD-003 | [Description of the debt item] | [module] | Low | L | Deferred | #-- |

### Severity Scale
- **Critical** -- Causes production issues or security vulnerabilities
- **High** -- Blocks new features or degrades performance
- **Medium** -- Makes development slower or code harder to maintain
- **Low** -- Cosmetic or minor inconvenience

### Effort Scale
- **XS** -- Less than 1 hour
- **S** -- 1-3 hours (one session)
- **M** -- 3-8 hours (one day)
- **L** -- 1-3 days
- **XL** -- More than 3 days (should be broken down)

### Status
- **Open** -- Identified, not started
- **In Progress** -- Being worked on
- **Deferred** -- Intentionally postponed (must have justification)
- **Resolved** -- Fixed, move to Resolved Debt section

## Resolved Debt

| ID | Description | Resolved Date | Resolution |
|----|-------------|---------------|------------|
| <!-- TD-NNN --> | <!-- What was fixed --> | <!-- YYYY-MM-DD --> | <!-- PR or brief description --> |

## Debt Intake Rules

1. Every new debt item must have a linked GitHub/GitLab issue
2. Severity must be assigned at creation -- no "unknown" severity
3. Deferred items must have a justification and a review date
4. Debt older than 90 days without progress gets escalated to Critical

## Related Documentation

- [anti-patterns.md](./anti-patterns.md) -- Patterns that create debt
- [substrate.md](./substrate.md) -- Navigation hub

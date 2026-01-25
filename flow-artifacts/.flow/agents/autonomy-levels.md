# Agent Autonomy Levels

> Trust boundaries for AI agents operating in this codebase.

## Overview

Not all work is equal. Some changes are low-risk and can be executed autonomously; others require human oversight. This document defines the trust levels and what agents can do at each level.

## Autonomy Levels

### Level 0: Supervised

**Trust:** Minimal - agent executes explicit instructions only.

| Can Do | Needs Approval |
|--------|----------------|
| Read files | Write any file |
| Run read-only commands | Run mutating commands |
| Answer questions | Make suggestions |
| Analyze code | Create branches |

**Use for:** New agents, unfamiliar codebases, learning phase.

---

### Level 1: Guided

**Trust:** Low - agent can make minor changes within guardrails.

| Can Do | Needs Approval |
|--------|----------------|
| Everything in Level 0 | Architecture changes |
| Edit existing files (non-critical) | New files in core paths |
| Create feature branches | Database migrations |
| Run tests | Modify CI/CD |
| Fix lint/type errors | Security-related code |
| Update documentation | Dependency changes |

**Guardrails:**
- Cannot modify files in `**/auth/**`, `**/security/**`, `**/*migration*`
- Cannot run `rm -rf`, `drop table`, destructive commands
- Must run tests before considering work complete

**Use for:** Routine bug fixes, documentation, test improvements.

---

### Level 2: Autonomous

**Trust:** Medium - agent can complete objectives independently.

| Can Do | Needs Approval |
|--------|----------------|
| Everything in Level 1 | Merge to main/master |
| Create new files | Production deployments |
| Modify any non-critical code | Delete files |
| Create pull requests | Breaking API changes |
| Add dependencies (approved list) | New external integrations |
| Create GitHub issues | Change auth/security code |

**Guardrails:**
- PRs require human review before merge
- New dependencies must be from approved list
- Cannot modify `.env`, secrets, or credentials
- Must update `.context/` docs for significant changes

**Use for:** Feature implementation, refactoring, most development work.

---

### Level 3: Full

**Trust:** High - agent operates as team member with merge rights.

| Can Do | Needs Approval |
|--------|----------------|
| Everything in Level 2 | Breaking changes to public API |
| Merge own PRs (with passing CI) | Security-critical modifications |
| Deploy to staging | Production deployments |
| Approve other agents' PRs | Delete repositories |
| Create/archive streams | Modify autonomy levels |

**Guardrails:**
- CI must pass before merge
- Production deploys still require human
- Breaking changes require explicit human approval
- Must log all significant decisions

**Use for:** Trusted, proven agents on well-understood codebases.

---

## Level Assignment

### Default Levels

| Agent Type | Default Level |
|------------|---------------|
| New Claude Code session | 1 |
| Established session (same project, 10+ interactions) | 2 |
| Background/scheduled agents | 0 (promote explicitly) |
| Cross-project agents | 0 |

### Promotion Criteria

To promote an agent:

**0 → 1:**
- Completed 5+ supervised tasks without issues
- Demonstrated understanding of codebase patterns

**1 → 2:**
- Completed 10+ guided tasks
- Zero reverted commits
- Positive human feedback

**2 → 3:**
- Extended track record (50+ completed objectives)
- Demonstrated sound judgment on edge cases
- Explicit human approval

### Demotion Triggers

Immediately drop to Level 0 if:
- Security issue introduced
- Data loss or corruption
- Breaking change without approval
- Repeated pattern violations

## Per-Objective Override

Objectives can specify minimum autonomy:

```markdown
## Autonomy Level Required

**Minimum Level:** 2
**Reason:** Creates new API endpoints, needs ability to create files
```

Agents below the minimum cannot pick up the objective.

## Audit Log

Significant autonomous actions should be logged:

```markdown
## Agent Actions Log

| Timestamp | Agent | Level | Action | Outcome |
|-----------|-------|-------|--------|---------|
| 2025-01-25 14:30 | claude-session-abc | 2 | Created PR #45 | Pending review |
| 2025-01-25 15:45 | claude-session-abc | 2 | Merged PR #44 | Success |
```

## Configuration

### Protected Paths

Files/directories that require Level 3 or human:

```
**/auth/**
**/security/**
**/*secret*
**/*credential*
**/.env*
**/migrations/**
.flow/agents/autonomy-levels.md  # This file
```

### Approved Dependencies

Level 2 agents can add these without approval:

```
# Testing
vitest
@testing-library/*
msw

# Types
@types/*

# Utilities (project-specific list)
zod
date-fns
lodash-es
```

All other dependencies require human approval.

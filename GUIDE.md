# Claude Code Workflow Guide

A practical workflow system for Claude Code that scales from single projects to parallel development across multiple codebases. Combines project knowledge documentation (.context system), GitHub-based task management, and multi-project coordination.

**Prerequisites:** Familiarity with Claude Code basics, `gh` CLI installed, GitHub repos configured.

---

## Part 1: The CLAUDE.md Hierarchy

Claude Code reads `CLAUDE.md` files at multiple levels. This creates a cascading context system:

```
~/.claude/CLAUDE.md              # Global - your personal preferences, always loaded
~/projects/CLAUDE.md             # Directory - shared patterns for project groups
~/projects/my-app/CLAUDE.md      # Project - specific rules for this codebase
```

### Global CLAUDE.md (~/.claude/CLAUDE.md)

Your personal AI assistant configuration. Set communication style, reference the .context system:

```markdown
## Communication Style

Be direct. No cheerleading phrases. Tell me when my ideas are flawed.
Use casual language. Focus on practical problems and realistic solutions.

## .context Project Knowledge System

When working in any project directory, check for a `.context/` folder. If present:

### On Session Start
1. Read `.context/substrate.md` first - it's the navigation hub
2. For coding tasks, read `.context/ai-rules.md` before writing any code
3. Check `.context/anti-patterns.md` to avoid known pitfalls

### When Writing Code
Always consult before generating code:
- `.context/ai-rules.md` - Coding standards and constraints
- `.context/glossary.md` - Project-specific terminology
- `.context/anti-patterns.md` - Patterns to avoid

### Key Principle
The .context folder contains institutional knowledge about WHY decisions were made.
Prefer patterns documented there over generic best practices.
If conflict between training and .context docs, follow .context.
```

### Directory-Level CLAUDE.md

Use for shared patterns across similar projects:

```markdown
# Node.js Projects

## Tech Stack Standards
- Node.js 20+ LTS
- TypeScript 5.3+ strict mode
- Vitest for testing

## Common Mistakes to Avoid
- Missing error handling in async functions
- Not validating external inputs
- Hardcoded configuration values

## Projects in This Directory
- **my-saas/** - Main SaaS platform (Next.js, tRPC, Drizzle, pnpm)
  - Has `.context/` documentation - read `.context/substrate.md` first
- **my-mobile/** - iOS companion app (Swift, SwiftUI)
  - Has `.context/` documentation
```

### Project CLAUDE.md

Quick-start guide pointing to detailed docs:

```markdown
# My Project - AI Assistant Context

Multi-tenant SaaS platform. Next.js 15 + Hono + tRPC + Drizzle ORM.

## .context System

Read these files before writing code:

1. .context/substrate.md     → Navigation hub
2. .context/ai-rules.md      → Hard coding constraints
3. .context/anti-patterns.md → Patterns to avoid

## GitHub Workflow

| Command | Purpose |
|---------|---------|
| `/gh-status` | Overview of issues, PRs, current branch |
| `/gh-start <issue#>` | Assign issue, create feature branch |
| `/gh-done` | Push changes, create PR |
| `/gh-bug` | Create bug report from conversation |

## Quick Commands

```bash
pnpm dev                  # Start development
pnpm build                # Build all packages
pnpm typecheck            # TypeScript check
pnpm test                 # Run tests
```
```

---

## Part 2: The .context Knowledge System

A folder structure for project documentation that Claude Code reads on demand. **Goal:** 80% of value with minimal overhead.

### Core Files (Always Create These 5)

```
.context/
├── substrate.md          # Navigation hub - READ FIRST
├── ai-rules.md           # Hard coding constraints
├── anti-patterns.md      # What NOT to do
├── glossary.md           # Domain terminology
└── SESSION_HANDOVER.md   # Current state for session continuity
```

### substrate.md - The Navigation Hub

```markdown
# Project Substrate

> One-line description of what this project does.

## Quick Navigation

| Domain | Purpose | Start Here |
|--------|---------|------------|
| [Architecture](./architecture/) | System design | overview.md |
| [Auth](./auth/) | Authentication flow | overview.md |
| [API](./api/) | Endpoints, procedures | endpoints.md |
| [Database](./database/) | Schema, models | schema.md |

## Tech Stack

```
Frontend: Next.js 15, React 19, TypeScript
Backend:  Hono, tRPC, Drizzle ORM
Database: PostgreSQL 16
```

## Key Files Reference

| Purpose | Path |
|---------|------|
| Database schema | `packages/database/src/schema/*.ts` |
| API routes | `apps/api/src/routes/*.ts` |
| UI components | `apps/web/src/components/*.tsx` |

## Decision History

| Date | Decision | Rationale |
|------|----------|-----------|
| 2024-12 | Drizzle over Prisma | Type-safe SQL, faster migrations |
| 2024-12 | tRPC over REST | End-to-end type safety |
```

### ai-rules.md - Hard Constraints

Non-negotiable rules Claude must follow:

```markdown
# AI Rules - Hard Constraints

## TypeScript Standards

```typescript
// NEVER use @ts-ignore, @ts-expect-error, or any type
// All function parameters and returns must be typed

// CORRECT: Use workspace aliases
import { db } from '@myproject/database';

// WRONG: Relative imports across packages
import { db } from '../../../packages/database/src';
```

## Database Rules

```typescript
// EVERY query on tenant data MUST include organizationId filter
// CORRECT
.where(
  and(
    eq(table.organizationId, ctx.organizationId),
    eq(table.id, input.id)
  )
)

// WRONG: Missing tenant filter = data leak
.where(eq(table.id, input.id))
```

## Security Non-Negotiables

1. Never log sensitive data (passwords, tokens, PII)
2. Never expose internal errors to clients
3. Always validate file uploads (MIME type AND content)
4. Always use parameterized queries
5. Never trust client-side validation alone
```

### anti-patterns.md - What NOT to Do

Document patterns that caused problems with code examples:

```markdown
# Anti-Patterns

## Missing Tenant Filter

**Problem**: Data leak across tenants.

```typescript
// WRONG
const items = await db.select().from(table).where(eq(table.id, id));

// CORRECT
const items = await db.select().from(table).where(
  and(
    eq(table.organizationId, ctx.organizationId),
    eq(table.id, id)
  )
);
```

**Why it matters**: One missing filter = data breach.

---

## N+1 Query Pattern

**Problem**: Performance disaster.

```typescript
// WRONG - N+1 queries
for (const item of items) {
  item.children = await db.select()...
}

// CORRECT - Single query with join
const itemsWithChildren = await db.select()
  .from(items)
  .leftJoin(children, eq(items.id, children.itemId));
```

---

## Historical Bugs

| Date | Bug | Root Cause | Fix |
|------|-----|------------|-----|
| 2024-12-15 | Users saw other users' data | Missing tenant filter | Added organizationId check |
```

### glossary.md - Domain Terminology

Define project-specific terms:

```markdown
# Glossary

## Core Entities

### Organization
The multi-tenant container. All business data belongs to exactly one organization.
- Database: `organizations` table
- Code: `Organization`, `organizationId`

### Member
A user belonging to an organization with a specific role.
- Roles: `owner` > `admin` > `member`
- Database: `organization_members` table

## Technical Terms

### tenantProcedure
A tRPC procedure requiring auth AND valid organization context via header.

### protectedProcedure
A tRPC procedure requiring auth but not organization context.
```

### SESSION_HANDOVER.md - Context Continuity

Capture state between sessions:

```markdown
# Session Handover

**Last Updated:** 2024-12-20

## Current Focus

Working on issue #47 - User authentication refactor.
Branch: `47-auth-refactor`

## Recent Changes

- Added OAuth provider support (PR #45)
- Fixed session timeout bug (PR #46)

## Open Tasks

```bash
gh issue list --state open
```

- #47 - Auth refactor (in progress)
- #42 - Performance optimization (blocked)

## Blockers

- Waiting on API credentials from client

## Notes for Next Session

- OAuth callback URLs need updating for production
- Run migrations after merging #47
```

### Optional Domain Folders

Only create these when complexity warrants:

```
.context/
├── architecture/
│   └── overview.md       # System diagrams, patterns
├── auth/
│   └── overview.md       # Auth flow, security
├── database/
│   └── schema.md         # ERD, migrations
└── deployment/
    └── overview.md       # How to ship
```

---

## Part 3: GitHub Workflow with Custom Skills

Custom slash commands that integrate Claude Code with GitHub Issues.

### Setup Labels

Run once per repository:

```bash
# Priority labels
gh label create "priority/critical" --color "B60205" --description "Production down or security issue"
gh label create "priority/high" --color "D93F0B" --description "Blocking or major functionality"
gh label create "priority/medium" --color "FBCA04" --description "Important but not urgent"
gh label create "priority/low" --color "0E8A16" --description "Nice to have"

# Type labels
gh label create "type/bug" --color "D73A4A" --description "Something isn't working"
gh label create "type/feature" --color "0075CA" --description "New functionality"
gh label create "type/debt" --color "CFD3D7" --description "Technical debt"
gh label create "type/security" --color "B60205" --description "Security issue"

# Status labels
gh label create "status/blocked" --color "FEF2C0" --description "Waiting on external dependency"
gh label create "status/review" --color "5319E7" --description "Ready for review"
```

### Create Custom Skills

Create `.claude/commands/` in your project:

**.claude/commands/gh-status.md:**
```markdown
---
description: GitHub Status Overview
---

Show me the current state of work:

1. Run `gh issue list --state open --label "priority/critical,priority/high" --limit 10`
2. Run `gh issue list --state open --assignee @me`
3. Run `git branch --show-current` and check if branch name contains issue number
4. Run `gh pr list --state open --limit 5`

Present a summary:
- What needs urgent attention
- What I'm currently working on
- What's ready for review
```

**.claude/commands/gh-start.md:**
```markdown
---
description: Start Work on GitHub Issue
---

Start work on issue #$ARGUMENTS:

1. Run `gh issue view $ARGUMENTS` to see issue details
2. Run `gh issue edit $ARGUMENTS --add-assignee @me` to assign yourself
3. Create branch: `git checkout -b $ARGUMENTS-<short-slug-from-title>`
4. Report back with issue summary and branch name
```

**.claude/commands/gh-done.md:**
```markdown
---
description: Finish Work and Create PR
---

Finish current work and create a PR:

1. Run `git branch --show-current` to get branch name
2. Extract issue number from branch name (e.g., "6-fix-bug" -> 6)
3. Run `git status` - if uncommitted changes, ask what to do
4. Run `git log origin/main..HEAD` - if unpushed commits, push them
5. Create PR: `gh pr create --title "<descriptive title>" --body "Fixes #<issue-number>"`
6. Report back with PR URL
```

**.claude/commands/gh-bug.md:**
```markdown
---
description: Quick Bug Report
---

Create a bug report from our conversation:

1. Gather context: What bug did we discuss? Expected vs actual behavior?
2. Determine priority (critical/high/medium/low)
3. Create issue:
   ```
   gh issue create \
     --title "<concise bug title>" \
     --body "<description with steps to reproduce>" \
     --label "type/bug,priority/<level>"
   ```
4. Report back with issue URL and number
```

### The Workflow

```bash
# See what needs attention
/gh-status

# Start work on an issue
/gh-start 12
# Claude: assigns issue, creates branch 12-add-user-auth

# ... do the work ...

# Create PR when done
/gh-done
# Claude: pushes, creates PR linked to issue #12

# After review, merge
gh pr merge --squash --delete-branch

# Deploy (customize for your setup)
ssh server "cd /app && git pull && docker compose up -d"
```

---

## Part 4: Parallel Project Development

Working on multiple projects simultaneously (e.g., SaaS backend + mobile app).

### Terminal Setup

Run multiple Claude Code instances:

```
┌────────────────────┬────────────────────┐
│  Terminal 1        │  Terminal 2        │
│  ~/projects/saas   │  ~/projects/mobile │
│  claude            │  claude            │
└────────────────────┴────────────────────┘
```

Each instance loads its own CLAUDE.md hierarchy and .context.

### Cross-Project Issue Flow

When work in one project creates tasks for another:

**In SaaS terminal:**
```
> The mobile app will need a new /api/v2/sync endpoint for offline support.
> /gh-bug
# Claude creates issue in current repo
```

**Then in mobile terminal:**
```
> We need to implement offline sync. The backend team created issue saas-repo#47
> for the API endpoint. Create a linked issue here for the mobile implementation.
```

**Or reference across repos:**
```bash
# Create issue referencing another repo
gh issue create \
  --title "Implement offline sync" \
  --body "Depends on org/saas-repo#47 for API endpoint" \
  --label "type/feature,priority/high"
```

### Shared Documentation Patterns

For related projects, consider:

```
projects/
├── CLAUDE.md                    # Shared conventions
├── saas/
│   ├── CLAUDE.md               # SaaS-specific
│   └── .context/
└── mobile/
    ├── CLAUDE.md               # Mobile-specific
    └── .context/
```

The parent CLAUDE.md can document shared API contracts, data models, etc.

### Session Handover Across Projects

Update SESSION_HANDOVER.md with cross-project notes:

```markdown
## Cross-Project Dependencies

- Mobile app waiting on saas#47 (sync API endpoint)
- Created mobile#23 to track implementation
- Shared data model changes need coordination
```

---

## Part 5: Onboarding Existing Projects

### Quick Setup (5 minutes)

1. Create `.context/` folder
2. Add the 5 core files (substrate, ai-rules, anti-patterns, glossary, session-handover)
3. Create `.claude/commands/` with the 4 GitHub skills
4. Update project CLAUDE.md to reference .context

### Extract Knowledge from Existing Codebase

Run these prompts in Claude Code:

**Step 1: Analyze**
```
Analyze this codebase:
1. Tech stack (check package.json, etc.)
2. Directory structure
3. Key entry points
4. Database/ORM setup
5. Auth approach

Give me a summary, not a wall of text.
```

**Step 2: Find Anti-patterns**
```
Search for signs of technical debt:
1. TODO/FIXME/HACK comments
2. Overly complex functions (100+ lines)
3. Inconsistent patterns
4. Hardcoded values

List with file:line references.
```

**Step 3: Extract Domain Terms**
```
Extract domain terminology:
1. Model/entity definitions - what are core business objects?
2. Enum definitions - what states/types exist?
3. Service class names - what operations matter?

Create a glossary with Term, Definition, Where Used.
```

**Step 4: Generate .context**
```
Based on our analysis, create the .context/ folder with:
1. substrate.md - project overview
2. ai-rules.md - based on existing patterns (not idealized)
3. glossary.md - terms we extracted
4. anti-patterns.md - problems we found
5. SESSION_HANDOVER.md - current state
```

---

## Part 6: Maintenance

### After Each Session

Update SESSION_HANDOVER.md:
- What changed
- What's still open
- Any blockers

### When You Hit a Bug

Add to anti-patterns.md Historical Bugs:

```markdown
| Date | Bug | Root Cause | Fix |
|------|-----|------------|-----|
| 2024-12-20 | Data leak | Missing tenant filter | Added org check |
```

### When Patterns Emerge

If you see the same mistake 3 times, add it to anti-patterns.md with:
- BAD code example
- GOOD code example
- Why it matters

### Periodic Review

Monthly: Review .context files for accuracy. Remove outdated info.

---

## Quick Reference

### File Purposes

| File | Purpose | When to Read |
|------|---------|--------------|
| `substrate.md` | Navigation hub | Every session start |
| `ai-rules.md` | Hard constraints | Before writing ANY code |
| `anti-patterns.md` | What NOT to do | Before writing code |
| `glossary.md` | Domain vocabulary | When confused about terms |
| `SESSION_HANDOVER.md` | Current state | Resuming work |

### Slash Commands

| Command | What It Does |
|---------|--------------|
| `/gh-status` | Show issues, PRs, current branch |
| `/gh-start <N>` | Assign issue N, create branch |
| `/gh-done` | Push and create PR |
| `/gh-bug` | Create bug issue from conversation |

### Typical Workflow

```bash
/gh-status              # What needs attention?
/gh-start 12            # Start issue #12
# ... work ...
/gh-done                # Create PR
gh pr merge --squash --delete-branch
# Deploy
```

---

## TL;DR

1. **CLAUDE.md hierarchy** - Global prefs → Directory patterns → Project specifics
2. **.context folder** - 5 core files documenting WHY, not just WHAT
3. **GitHub skills** - 4 custom commands for issue-driven development
4. **Parallel work** - Multiple terminals, cross-reference issues
5. **Maintenance** - Update SESSION_HANDOVER.md, log bugs to anti-patterns

Start minimal. Add documentation as patterns emerge. Don't over-engineer.

# Advanced .context/ Examples

Real-world `.context/` patterns extracted from production projects.

## What's Here

| File | Purpose | When to Use |
|------|---------|-------------|
| `github.md` | GitHub integration patterns, workflows, permissions | Projects using GitHub Actions, Claude Code GitHub integration |
| `specs-README.md` | Requirements capture workflow | Complex features needing upfront spec work |
| `vps-deployment.md` (template below) | Deployment documentation | Projects with custom deployment processes |

## Example: github.md

Shows how to document:
- GitHub workflows (Actions)
- Claude Code permissions
- Allowed CLI commands
- Integration examples

**Use when:**
- Using Claude Code GitHub Actions
- Need to document GitHub workflows
- Want to constrain what `gh` commands Claude can use

## Example: specs/README.md

Shows how to structure requirements capture:
- Spec template
- When to create specs vs start coding
- How specs feed into FLOW streams

**Use when:**
- Building complex features (size/L)
- Multiple stakeholders need clarity
- Requirements are unclear upfront

## VPS Deployment Template

Create `.context/vps-deployment.md` for custom deployment docs:

```markdown
# VPS Deployment Guide

## Server Access

| Setting | Value |
|---------|-------|
| Host | {{VPS_HOST}} |
| User | {{VPS_USER}} |
| SSH | {{SSH_ALIAS}} |

## Deployment Process

1. **Local Testing**
   \`\`\`bash
   ./deploy.sh local
   \`\`\`

2. **Production Deploy**
   \`\`\`bash
   ./deploy.sh production
   \`\`\`

3. **Verification**
   - URL: {{PRODUCTION_URL}}
   - Check: {{HEALTH_CHECK_ENDPOINT}}

## Rollback Procedure

\`\`\`bash
./deploy.sh rollback <version>
\`\`\`

## Common Issues

### Issue: Service won't start
\`\`\`bash
sudo systemctl status {{SERVICE_NAME}}
sudo journalctl -u {{SERVICE_NAME}} --since "10 minutes ago"
\`\`\`
```

## Directory Structure Examples

### Research Directory

For exploratory work, research notes:

```
.context/
└── research/
    ├── api-comparison.md
    ├── architecture-decision-log.md
    └── spike-results.md
```

**Use when:**
- Evaluating technical approaches
- Documenting spikes
- Recording architectural decisions

### Specs Directory

For requirements documentation:

```
.context/
└── specs/
    ├── README.md                # This file explains the workflow
    ├── example-spec.md          # Template showing structure
    └── feature-name.md          # Real specs
```

**Use when:**
- Complex features need upfront clarity
- Multiple implementation options exist
- Success criteria need definition before coding

### Architecture Directory

For system design docs:

```
.context/
└── architecture/
    ├── overview.md
    ├── database-schema.md
    ├── api-design.md
    └── deployment-topology.md
```

**Use when:**
- Multiple developers/agents working together
- System complexity requires documentation
- Onboarding needs system overview

## Tips

### Keep It Focused

Only create files that Claude will **actually read**.

**Good:**
- Files Claude checks before writing code (ai-rules, anti-patterns)
- Files answering "why" questions (architecture decisions)
- Files preventing repeated mistakes (anti-patterns, glossary)

**Bad:**
- Exhaustive API docs (use external docs + links)
- Detailed implementation notes (code comments are better)
- Meeting notes (unless they capture decisions)

### Link, Don't Duplicate

Reference external docs rather than copying:

```markdown
## Authentication

We use OAuth2 with JWT tokens.

Implementation guide: https://docs.example.com/oauth2

## Key Differences from Standard OAuth2

- We use short-lived refresh tokens (30 min, not 24h)
- Tokens include custom `organization_id` claim
- See `.context/anti-patterns.md` for common auth mistakes
```

### Update After Reflection

After `/flow-reflect`, update `.context/` with learnings:

```bash
# Reflect on completed stream
/flow-reflect "Authentication Overhaul"

# Claude synthesizes learnings and updates:
# - .context/ai-rules.md (new constraints)
# - .context/anti-patterns.md (mistakes to avoid)
# - .context/glossary.md (new domain terms)
```

## Integration with FLOW

```
.context/specs/       # Requirements (input to FLOW)
       ↓
GitHub Milestones     # Streams
GitHub Issues         # Objectives
       ↓
Work completed        # Learnings captured
       ↓
.context/ai-rules.md  # Knowledge accumulated
.context/anti-patterns.md
```

**Workflow:**
1. Complex feature arrives
2. Create `.context/specs/<name>.md` via interview
3. Spec creates GitHub milestone + epic issue
4. Break down into objectives, start work
5. After completion, reflect learnings back to `.context/`

## Don't Overdo It

Start minimal:
- `substrate.md` - Overview
- `ai-rules.md` - Hard constraints
- `anti-patterns.md` - Mistakes to avoid

Add advanced patterns as needed:
- Hit the same mistake twice? → `anti-patterns.md`
- Complex deployment? → `vps-deployment.md` or `architecture/deployment.md`
- Unclear requirements? → `specs/` workflow
- GitHub integration? → `github.md`

Let `.context/` grow organically based on pain points.

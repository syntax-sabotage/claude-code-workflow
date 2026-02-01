# FLOW Hub - {{PROJECT_NAME}}

> Fluid Learning Optimization Workflow - AI-native development without sprints.

**Current State:** v2 - GitHub-native tracking
**Source of Truth:** GitHub (milestones, issues, labels)
**Repository:** {{GITHUB_REPO_URL}}

## Quick Reference

| FLOW Concept | GitHub Feature |
|--------------|----------------|
| Stream | Milestone |
| Objective | Issue |
| Pool | Issues with `needs-triage` label |
| Status | `active`, `blocked` labels + open/closed |
| Size | `size/S`, `size/M`, `size/L` labels |
| Learnings | Issue closing comment |
| Reflected | `reflected` label (learnings rolled up) |

## Commands

Each command is defined in `.claude-commands/` (copy to your project's `.claude/commands/`):

| Command | Purpose | Definition |
|---------|---------|------------|
| `/flow-status` | Query milestones + issues via `gh` | [flow-status.md](../../../flow-artifacts/.claude-commands/flow-status.md) |
| `/flow-start <issue#>` | Claim issue + create branch | [flow-start.md](../../../flow-artifacts/.claude-commands/flow-start.md) |
| `/flow-stream <name>` | Query/create milestone, list stream issues | [flow-stream.md](../../../flow-artifacts/.claude-commands/flow-stream.md) |
| `/flow-objective <title>` | `gh issue create` with milestone + labels | [flow-objective.md](../../../flow-artifacts/.claude-commands/flow-objective.md) |
| `/flow-ship` | Close issue + PR + merge + deploy | [flow-ship.md](../../../flow-artifacts/.claude-commands/flow-ship.md) |
| `/flow-triage` | Assign milestones to `needs-triage` issues | [flow-triage.md](../../../flow-artifacts/.claude-commands/flow-triage.md) |
| `/flow-reflect <stream>` | Synthesize learnings -> `.context/`, add `reflected` label | [flow-reflect.md](../../../flow-artifacts/.claude-commands/flow-reflect.md) |
| `/flow-handover` | End session summary | [flow-handover.md](../../../flow-artifacts/.claude-commands/flow-handover.md) |
| `/flow-resume` | Start session, query current state | [flow-resume.md](../../../flow-artifacts/.claude-commands/flow-resume.md) |
| `/flow-health` | System health check | [flow-health.md](../../../flow-artifacts/.claude-commands/flow-health.md) |

## Streams (Milestones)

View at: {{GITHUB_REPO_URL}}/milestones

| Milestone | Focus |
|-----------|-------|
| {{STREAM_NAME}} | {{STREAM_DESCRIPTION}} |

Success criteria live in milestone descriptions.

## Workflow

### Starting Work

```bash
/flow-status                    # See all streams + objectives
/flow-start 47                  # Claim issue + create branch
```

Or manually:
```bash
gh issue list --milestone "{{STREAM_NAME}}" --state open
gh issue edit 47 --add-label "active"   # Claim it
git checkout -b 47-feature-slug
```

### Completing Work

```bash
# After PR merged
gh issue close 47 --comment "## Learnings\n- What we learned..."
gh issue edit 47 --remove-label "active"
```

Or use `/flow-ship` which handles: PR -> merge -> close issue -> deploy.

## Labels

| Label | Purpose |
|-------|---------|
| `active` | Currently being worked on |
| `blocked` | Waiting on something |
| `size/S` | Small (hours) |
| `size/M` | Medium (days) |
| `size/L` | Large (week+) |
| `needs-triage` | Pool item, needs stream assignment |
| `reflected` | Learnings captured in rollup |
| `autonomy/0` | Supervised - needs approval for everything |
| `autonomy/1` | Guided - interactive, asks questions |
| `autonomy/2` | Autonomous - background execution |
| `autonomy/3` | Full - trusted with merge rights |
| `type/bug` | Bug fix |
| `type/feature` | New feature |
| `type/debt` | Technical debt |
| `type/security` | Security related |

### Set Up Labels

Run once per repository:

```bash
gh label create "needs-triage" --color "EDEDED"
gh label create "active" --color "0E8A16"
gh label create "blocked" --color "D93F0B"
gh label create "reflected" --color "5319E7"

gh label create "size/S" --color "BFD4F2"
gh label create "size/M" --color "7CB3F7"
gh label create "size/L" --color "1D76DB"

gh label create "autonomy/0" --color "FEF2C0"
gh label create "autonomy/1" --color "FBCA04"
gh label create "autonomy/2" --color "0075CA"
gh label create "autonomy/3" --color "5319E7"

gh label create "type/bug" --color "D73A4A"
gh label create "type/feature" --color "0075CA"
gh label create "type/debt" --color "CFD3D7"
gh label create "type/security" --color "B60205"

# Add priority labels (optional)
gh label create "priority/critical" --color "B60205"
gh label create "priority/high" --color "D93F0B"
gh label create "priority/medium" --color "FBCA04"
gh label create "priority/low" --color "0E8A16"
```

## Autonomy-Based Execution

Autonomy labels control how `/flow-start` executes work:

| Autonomy | Mode | What Happens |
|----------|------|--------------|
| 0-1 | **Interactive** | Foreground execution, asks questions, coordinates with user |
| 2-3 | **Background** | Spawns subagent with `run_in_background: true`, user stays available |

**Default autonomy by size:**
- `size/S` -> `autonomy/2` (just do it)
- `size/M` -> `autonomy/2` (standard work)
- `size/L` -> `autonomy/1` (needs coordination)

**Override when issue involves:**
- Auth/security -> `autonomy/0` or `autonomy/1`
- Database migrations -> `autonomy/1`
- Breaking changes -> `autonomy/0`
- Infrastructure changes -> `autonomy/1`

## Integration with .context/

```
.context/     # What we KNOW (static knowledge, synced via git)
.flow/        # How we WORK (this doc + ceremonies)
GitHub        # What we're DOING (dynamic state)
```

### Specs Feed FLOW Streams

For complex features, capture requirements **before** creating FLOW issues:

```bash
# 1. Create spec via interview (or manually)
# Creates: .context/specs/<slug>.md
# Creates: GitHub milestone (stream)
# Creates: Epic issue (links to spec)

# 2. Break down epic into objectives
/flow-objective "Implement sync API"

# 3. Start work
/flow-start <issue#>
```

**When to use specs:**
- Large/complex features (size/L)
- Multiple people involved
- Unclear requirements need clarification
- Need testable success criteria before planning

**When to skip specs:**
- Small bug fixes (size/S)
- Simple features with obvious scope
- Technical debt items with clear outcomes

## Statusline Integration

FLOW commands automatically update `.flow/state.json` for the Claude Code statusline.

**What you see:**
```
[Model] #123 Issue title | Stream | 1 blocked | 2 PR * | 45% | $0.23
```

- **Active issue** - Number and truncated title from `active` label
- **Stream** - Milestone name (if assigned)
- **Indicators** - Blocked count, open PRs
- **Git dirty** - `*` when uncommitted changes
- **Context/Cost** - Standard Claude Code metrics

**Refresh triggers:**
- `/flow-status` - Manual refresh
- `/flow-resume` - Session start
- `/flow-start` - Claiming work
- `/flow-ship` - Completing work (clears active)

**Files:**
- `.flow/statusline.sh` - Statusline renderer (reads cached state)
- `.flow/update-state.sh` - State updater (queries GitHub)
- `.flow/state.json` - Cached state (gitignored, ephemeral)

**Setup:**

In `~/.claude/config.json`:
```json
{
  "statusline": "/path/to/your-repo/.flow/statusline.sh"
}
```

## Principles

1. **Ship when ready** - No sprint boundaries
2. **GitHub is truth** - Query, don't read files
3. **Streams over sprints** - Related objectives flow together
4. **Learn continuously** - Every completion captures learnings
5. **Reflect periodically** - Roll up tactical -> strategic knowledge
6. **Test before deploy** - Always validate changes

---

*This is a v2 FLOW implementation. See [FLOW_V2_MIGRATION.md](../../FLOW_V2_MIGRATION.md) for evolution from v1.*

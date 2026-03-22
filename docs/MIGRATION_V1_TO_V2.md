# FLOW v2: GitHub-Native Migration

## What Changed

FLOW v1 used **file-based tracking** (objectives/, streams/, markdown files).
FLOW v2 uses **GitHub-native tracking** (milestones, issues, labels).

### Why the Change?

**Problems with v1:**
- Duplicate state between files and GitHub
- Merge conflicts on shared files (pool.md, metrics, etc.)
- Manual syncing between local state and GitHub
- Hard to query state programmatically
- No built-in notifications/subscriptions

**Benefits of v2:**
- **Single source of truth** -- GitHub is canonical
- **No merge conflicts** -- Issues/labels are atomic
- **Rich querying** -- `gh` CLI with filters
- **Built-in collaboration** -- Mentions, subscriptions, notifications
- **API access** -- Easy automation and statusline integration

## Mapping: v1 to v2

| FLOW Concept | v1 (Files) | v2 (GitHub) |
|--------------|------------|-------------|
| **Stream** | `.flow/streams/<name>.md` | Milestone |
| **Objective** | `.flow/objectives/<slug>.md` | Issue |
| **Pool** | `.flow/objectives/pool.md` | `needs-triage` label |
| **Status** | Frontmatter in .md files | `active`, `blocked` labels + open/closed |
| **Size** | Frontmatter: `size: M` | `size/S`, `size/M`, `size/L` labels |
| **Priority** | Frontmatter: `priority: high` | `priority/critical`, `priority/high`, etc. |
| **Autonomy** | Frontmatter: `autonomy: 2` | `autonomy/0` through `autonomy/3` labels |
| **Type** | Frontmatter: `type: feature` | `type/bug`, `type/feature`, `type/debt`, etc. |
| **Learnings** | `.flow/objectives/<slug>.md` | Issue closing comment |
| **Reflected** | Deleted from objectives/ | `reflected` label (learnings rolled up) |
| **Metrics** | `.flow/metrics/weekly-log.md` | GitHub Insights + custom queries |

## Directory Structure Changes

### v1 (File-Based)
```
.flow/
├── FLOW.md
├── streams/
│   ├── active/
│   │   └── auth-overhaul.md
│   └── STREAM_TEMPLATE.md
├── objectives/
│   ├── obj-001-login-flow.md
│   ├── obj-002-mfa.md
│   └── pool.md
├── agents/
│   ├── autonomy-levels.md
│   ├── handover-protocol.md
│   └── registry.md
├── metrics/
│   ├── overview.md
│   └── weekly-log.md
└── ceremonies/
    └── overview.md
```

### v2 (GitHub-Native)
```
.flow/
├── state.json              # Cached state (gitignored)
└── .gitignore
```

**Everything else lives in GitHub:**
- Streams: milestones
- Objectives: issues
- Pool: issues with `needs-triage` label
- Metrics: GitHub Insights + custom `gh` queries

## Skill Changes

### v1 Skills (File Manipulation)
```bash
/flow-status          # Parse .flow/streams/, .flow/objectives/
/flow-objective       # Create new .md file, update pool.md
/flow-start           # Move from pool.md to objectives/, update status
/flow-ship            # Update .md file, move to completed/
/flow-reflect         # Parse objectives/, generate rollup
```

### v2 Skills (GitHub API)
```bash
/flow-status          # gh issue list, gh pr list
/flow-objective       # gh issue create --milestone --label
/flow-start           # gh issue edit --add-label active, git checkout -b
/flow-ship            # gh pr create, gh issue close
/flow-reflect         # gh issue list --label reflected=false, synthesize
```

## Migration Steps

### 1. Set Up GitHub Labels

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
```

### 2. Migrate Streams to Milestones

For each `.flow/streams/active/<name>.md`:

```bash
gh milestone create "<title>" --description "$(cat success-criteria)"
```

### 3. Migrate Objectives to Issues

For each `.flow/objectives/obj-*.md`:

```bash
gh issue create \
  --title "<title>" \
  --body "<description>" \
  --milestone "<stream>" \
  --label "size/<S|M|L>" \
  --label "type/<bug|feature|debt>" \
  --label "autonomy/<0|1|2|3>"
```

### 4. Update .flow/ Directory

```bash
# Backup old structure
mv .flow .flow-v1-backup

# Create new structure
mkdir .flow
echo '{"workstations":{},"milestones":[],"updated_at":""}' > .flow/state.json
echo "session-debt.jsonl" > .flow/.gitignore
echo "learnings.jsonl" >> .flow/.gitignore
echo "state.json" >> .flow/.gitignore
```

### 5. Update Skills

Replace old skill definitions with v2 versions that use `gh` CLI instead of
file manipulation.

### 6. Initial State Sync

Verify everything migrated correctly:

```bash
gh issue list --state open
gh milestone list
```

## Autonomy Levels (Enhanced in v2)

Still use 0-3 scale, now as labels:
- `autonomy/0` -- Supervised (approval for everything)
- `autonomy/1` -- Guided (interactive, asks questions)
- `autonomy/2` -- Autonomous (background execution)
- `autonomy/3` -- Full trust (merge rights)

**Default by size:**
- `size/S` -> `autonomy/2` (just do it)
- `size/M` -> `autonomy/2` (standard work)
- `size/L` -> `autonomy/1` (needs coordination)

**Override for sensitive work:**
- Auth/security -> `autonomy/0` or `autonomy/1`
- Database migrations -> `autonomy/1`
- Breaking changes -> `autonomy/0`

## Performance Comparison

| Operation | v1 (Files) | v2 (GitHub) |
|-----------|------------|-------------|
| Query all objectives | Parse ~50 .md files (slow) | `gh issue list` (fast) |
| Update objective status | Edit .md, commit, push | `gh issue edit` (instant) |
| Check blocked objectives | Grep frontmatter | `gh issue list --label blocked` |
| Get metrics | Manually update weekly-log.md | `gh issue list --state closed --json closedAt` |
| Merge conflicts | **Common** (pool.md, metrics) | **Never** (atomic API) |

## Gotchas

### API Rate Limits
GitHub API has rate limits (5000/hour authenticated). Mitigate with:
- Cache state in `state.json` (statusline uses cache, not API)
- Only refresh on FLOW skill invocations, not every render
- Use `gh` CLI (handles auth + caching)

### Offline Work
v1 worked offline (files). v2 requires internet for `gh` commands. Workaround:
work offline using git branches for context, sync when back online.

### GitHub CLI Required
```bash
brew install gh              # macOS
gh auth login                # Authenticate
```

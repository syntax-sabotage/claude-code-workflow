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
- **Single source of truth** - GitHub is canonical
- **No merge conflicts** - Issues/labels are atomic
- **Rich querying** - `gh` CLI with filters
- **Built-in collaboration** - Mentions, subscriptions, notifications
- **API access** - Easy automation and statusline integration

## Mapping: v1 → v2

| FLOW Concept | v1 (Files) | v2 (GitHub) |
|--------------|------------|-------------|
| **Stream** | `.flow/streams/<name>.md` | Milestone |
| **Objective** | `.flow/objectives/<slug>.md` | Issue |
| **Pool** | `.flow/objectives/pool.md` | `needs-triage` label |
| **Status** | Frontmatter in .md files | `active`, `blocked` labels + open/closed |
| **Size** | Frontmatter: `size: M` | `size/S`, `size/M`, `size/L` labels |
| **Priority** | Frontmatter: `priority: high` | `priority/critical`, `priority/high`, etc. |
| **Autonomy** | Frontmatter: `autonomy: 2` | `autonomy/0`, `autonomy/1`, `autonomy/2`, `autonomy/3` |
| **Type** | Frontmatter: `type: feature` | `type/bug`, `type/feature`, `type/debt`, etc. |
| **Learnings** | `.flow/objectives/<slug>.md` | Issue closing comment |
| **Reflected** | Deleted from objectives/ | `reflected` label (learnings rolled up) |
| **Metrics** | `.flow/metrics/weekly-log.md` | GitHub Insights + custom queries |
| **Agent Registry** | `.flow/agents/registry.md` | N/A (ephemeral, use gh CLI) |

## Directory Structure Changes

### v1 (File-Based)
```
.flow/
├── FLOW.md                      # Hub
├── streams/
│   ├── active/
│   │   └── auth-overhaul.md     # Stream definition
│   └── STREAM_TEMPLATE.md
├── objectives/
│   ├── obj-001-login-flow.md    # Objective details
│   ├── obj-002-mfa.md
│   └── pool.md                  # Untriaged objectives
├── agents/
│   ├── autonomy-levels.md
│   ├── handover-protocol.md
│   └── registry.md              # Active agents
├── metrics/
│   ├── overview.md
│   └── weekly-log.md            # Manual metrics
└── ceremonies/
    └── overview.md
```

### v2 (GitHub-Native)
```
.flow/
├── FLOW.md                      # Hub (updated for GitHub)
├── statusline.sh                # Claude Code statusline integration
├── update-state.sh              # Fetch GitHub state
└── state.json                   # Cached state (gitignored)
```

**Everything else lives in GitHub:**
- Streams → https://github.com/user/repo/milestones
- Objectives → https://github.com/user/repo/issues
- Pool → Issues with `needs-triage` label
- Metrics → GitHub Insights + custom `gh` queries

## Command Changes

### v1 Commands (File Manipulation)
```bash
/flow-status          # Parse .flow/streams/, .flow/objectives/
/flow-objective       # Create new .md file, update pool.md
/flow-start           # Move from pool.md to objectives/, update status
/flow-ship            # Update .md file, move to completed/
/flow-reflect         # Parse objectives/, generate rollup
```

### v2 Commands (GitHub API)
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
# Extract title and success criteria from markdown
gh milestone create "<title>" --description "$(cat success-criteria)"
```

### 3. Migrate Objectives to Issues

For each `.flow/objectives/obj-*.md`:

```bash
# Extract frontmatter and body
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
cp /path/to/templates/flow-artifacts/.flow/FLOW.md .flow/
cp /path/to/templates/flow-artifacts/.flow/statusline.sh .flow/
cp /path/to/templates/flow-artifacts/.flow/update-state.sh .flow/
chmod +x .flow/*.sh

# Gitignore ephemeral state
echo "state.json" >> .flow/.gitignore
```

### 5. Update Commands

```bash
# Replace old commands
rm .claude/commands/flow-*.md
cp /path/to/templates/flow-artifacts/.claude-commands/* .claude/commands/
```

### 6. Initial State Sync

```bash
# Populate state.json
./.flow/update-state.sh
```

## Statusline Integration (New in v2)

FLOW v2 adds Claude Code statusline integration showing:
- Active issue number + title
- Current milestone (stream)
- Blocked count
- Open PRs
- Git dirty indicator

**Setup:**

In `~/.claude/config.json`:
```json
{
  "statusline": "/path/to/repo/.flow/statusline.sh"
}
```

**How it works:**
1. FLOW commands call `.flow/update-state.sh` to refresh `state.json`
2. `statusline.sh` reads cached state (fast, no API calls)
3. Statusline updates whenever FLOW commands run

**Example output:**
```
[Sonnet] #47 Implement sync API | Invoice Pro | 1 blocked | 2 PR * | 45% | $0.23
```

## Specs Workflow (New in v2)

Complex features need requirements **before** implementation. FLOW v2 adds a specs workflow:

```
.context/
└── specs/
    ├── README.md                    # Specs overview
    ├── example-feature.md           # Spec template
    └── nextcloud-sync.md            # Real spec
```

**When to use:**
- Large features (size/L)
- Unclear requirements
- Multi-objective epics

**Workflow:**
```bash
/odoo-spec                           # Interactive interview, creates spec
# ... creates .context/specs/<slug>.md + GitHub milestone + epic issue

/flow-objective "Sub-task 1"         # Break down epic
/flow-objective "Sub-task 2"

/flow-start <issue#>                 # Start work
```

## What to Keep from v1

Some v1 concepts are still valuable:

### Autonomy Levels (Enhanced in v2)

Still use 0-3 scale, but now as **labels**:
- `autonomy/0` - Supervised (approval for everything)
- `autonomy/1` - Guided (interactive, asks questions)
- `autonomy/2` - Autonomous (background execution)
- `autonomy/3` - Full trust (merge rights)

**Default by size:**
- `size/S` → `autonomy/2` (just do it)
- `size/M` → `autonomy/2` (standard work)
- `size/L` → `autonomy/1` (needs coordination)

**Override for sensitive work:**
- Auth/security → `autonomy/0` or `autonomy/1`
- Database migrations → `autonomy/1`
- Breaking changes → `autonomy/0`

### Reflection (Streamlined in v2)

v1 had manual rollup ceremonies. v2 makes it simpler:

1. Learnings capture on issue close:
   ```bash
   gh issue close 47 --comment "## Learnings\n- What we learned..."
   ```

2. Periodic rollup to `.context/`:
   ```bash
   /flow-reflect "Invoice Pro"      # Query issues, synthesize, update .context/
   ```

3. Mark as reflected:
   ```bash
   gh issue edit 47 --add-label "reflected"
   ```

## Performance Comparison

| Operation | v1 (Files) | v2 (GitHub) |
|-----------|------------|-------------|
| Query all objectives | Parse ~50 .md files (slow) | `gh issue list` (fast) |
| Update objective status | Edit .md, commit, push | `gh issue edit` (instant) |
| Check blocked objectives | Grep frontmatter | `gh issue list --label blocked` |
| Get metrics | Manually update weekly-log.md | `gh issue list --state closed --json closedAt` |
| Statusline data | Parse all files | Read cached `state.json` |
| Merge conflicts | **Common** (pool.md, metrics) | **Never** (atomic API) |

## Gotchas

### API Rate Limits

GitHub API has rate limits (5000/hour authenticated). Mitigate with:
- Cache state in `state.json` (statusline uses cache, not API)
- Only refresh on FLOW commands, not every statusline render
- Use `gh` CLI (handles auth + caching)

### Offline Work

v1 worked offline (files). v2 requires internet for `gh` commands.

**Workaround:**
- Clone issues locally when starting work (issue body in commit message)
- Work offline, sync when back online
- Use git branches to track context (branch name = issue number)

### GitHub CLI Required

v2 requires `gh` CLI. Install:
```bash
brew install gh              # macOS
gh auth login                # Authenticate
```

## Conclusion

**FLOW v2 is simpler and more robust:**
- Less code to maintain (no file parsing)
- Fewer merge conflicts (atomic GitHub operations)
- Better collaboration (built-in GitHub features)
- Richer querying (GitHub API + `gh` CLI)
- Statusline integration (real-time project state)

**Trade-offs:**
- Requires internet connection
- Depends on GitHub (not self-hosted friendly)
- API rate limits (mitigated with caching)

For teams using GitHub, v2 is the clear winner.

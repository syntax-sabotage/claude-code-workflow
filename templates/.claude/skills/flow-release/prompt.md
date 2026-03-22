---
description: FLOW Release - Tag and create a GitHub release
---

<!--
  PROCEDURAL SKILL - Release tagging and GitHub release creation.
  Generates release notes from PRs merged since last tag.
-->

**MODEL:** Sonnet (release notes generation)
**EXECUTION:** Foreground (interactive confirmation required)

## Usage

```
/flow-release              # auto-detect bump type from PR labels
/flow-release patch        # bugfix release (0.1.0 -> 0.1.1)
/flow-release minor        # feature release (0.1.0 -> 0.2.0)
/flow-release major        # breaking release (0.1.0 -> 1.0.0)
```

## 1. Pre-Flight Check

Must be on the default branch with a clean working tree:

```bash
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name')
CURRENT=$(git branch --show-current)
if [ "$CURRENT" != "$DEFAULT_BRANCH" ]; then
  echo "ERROR: Releases must be created from $DEFAULT_BRANCH. Currently on: $CURRENT"
  exit 1
fi

git fetch origin $DEFAULT_BRANCH
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/$DEFAULT_BRANCH)
if [ "$LOCAL" != "$REMOTE" ]; then
  echo "ERROR: Local $DEFAULT_BRANCH is not in sync with origin/$DEFAULT_BRANCH. Pull first."
  exit 1
fi

if [ -n "$(git status --porcelain)" ]; then
  echo "ERROR: Working tree is dirty. Commit or stash changes first."
  exit 1
fi
```

## 2. Determine Version

Get the latest release tag and compute next version:

```bash
# Get latest tag (sorted by version) -- adjust prefix to match your project
# Common patterns: v*, project-*, or plain semver
TAG_PREFIX="v"
LATEST=$(git tag -l "${TAG_PREFIX}*" --sort=-version:refname | head -1)

if [ -z "$LATEST" ]; then
  echo "No previous releases found. Starting from ${TAG_PREFIX}0.1.0"
  LATEST="${TAG_PREFIX}0.0.0"
fi

echo "Latest release: $LATEST"
```

Parse the version components:

```bash
VERSION=${LATEST#$TAG_PREFIX}
IFS='.' read -r MAJOR MINOR PATCH <<< "$VERSION"
```

### Bump Logic

If bump type was provided as argument, use it. Otherwise auto-detect from PR labels:

```bash
# Auto-detect: scan merged PRs since last tag
# - Any PR with "breaking" label -> major
# - Any PR with "feature" or "enhancement" label -> minor
# - Otherwise -> patch
gh pr list --state merged --search "merged:>=$(git log -1 --format=%aI $LATEST 2>/dev/null || echo '2020-01-01')" \
  --json labels -q '.[].labels[].name' | sort -u
```

Apply bump:
- **major**: `MAJOR+=1, MINOR=0, PATCH=0`
- **minor**: `MINOR+=1, PATCH=0`
- **patch**: `PATCH+=1`

```
NEXT_VERSION="${TAG_PREFIX}${MAJOR}.${MINOR}.${PATCH}"
```

## 3. Generate Release Notes

Collect PRs merged since the last tag:

```bash
# If no previous tag, use initial commit
if [ "$LATEST" = "${TAG_PREFIX}0.0.0" ]; then
  SINCE_REF=$(git rev-list --max-parents=0 HEAD | head -1)
else
  SINCE_REF="$LATEST"
fi

# Get merge commits since last release
git log ${SINCE_REF}..HEAD --merges --oneline

# List changed directories/modules
git diff --name-only ${SINCE_REF}..HEAD | cut -d/ -f1 | sort -u
```

### Generate Notes

Compose release notes from PR/commit data:

Group by category based on conventional commit prefixes or PR labels:

```markdown
### Features
- <description> (#<PR-number>)

### Fixes
- <description> (#<PR-number>)

### Internal
- <description> (#<PR-number>)

### Components Changed
<list of top-level directories/modules that had changes>
```

Keep descriptions concise. Use PR titles as the base.

## 4. Confirm with User

Display the release summary and ask for confirmation:

```
## Release: <NEXT_VERSION>

### Changes since <LATEST>
<generated release notes>

### Stats
- Commits: <count>
- PRs merged: <count>
- Components changed: <list>

Proceed with release? [y/n]
```

**Do NOT proceed without explicit user confirmation.**

## 5. Create Tag and Push

```bash
git tag -a "<NEXT_VERSION>" -m "Release <NEXT_VERSION>

<release notes summary -- first 3 lines>"

git push origin "<NEXT_VERSION>"
```

## 6. Create GitHub Release

```bash
gh release create "<NEXT_VERSION>" \
  --title "<NEXT_VERSION>" \
  --notes "$(cat <<'EOF'
<full generated release notes>
EOF
)"
```

## 7. Report

```
## Released: <NEXT_VERSION>

**Tag:** <NEXT_VERSION>
**Commits:** <count> since <LATEST>
**Release URL:** <github-release-url>

Release notes published to GitHub.
```

## Notes

- Releases are always created from the default branch -- never from feature branches
- Tags follow format `<prefix>MAJOR.MINOR.PATCH` (configure `TAG_PREFIX` for your project)
- Adjust the tag prefix to match your project convention (e.g., `v`, `release-`, or project-specific)
- The CI pipeline may have a dedicated release stage that triggers on tag push

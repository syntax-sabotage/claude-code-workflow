#!/bin/bash
# Updates .flow/state.json with current FLOW state from GitHub
# Called by FLOW commands after GitHub operations
#
# Usage: .flow/update-state.sh [--clear-active]
#   --clear-active  Clears the active issue (used after /flow-ship)

set -e

STATE_FILE=".flow/state.json"
CLEAR_ACTIVE=false

# Parse args
while [[ $# -gt 0 ]]; do
  case $1 in
    --clear-active)
      CLEAR_ACTIVE=true
      shift
      ;;
    *)
      shift
      ;;
  esac
done

# Get repo info
REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner' 2>/dev/null || echo "")
if [[ -z "$REPO" ]]; then
  echo "Not in a GitHub repo" >&2
  exit 1
fi

# Query active issue
active_issue_json="null"
stream=""
if [[ "$CLEAR_ACTIVE" == "false" ]]; then
  active_data=$(gh issue list --label "active" --state open --json number,title,milestone --limit 1 2>/dev/null || echo "[]")
  if [[ $(echo "$active_data" | jq 'length') -gt 0 ]]; then
    active_issue_json=$(echo "$active_data" | jq '.[0] | {number: .number, title: .title}')
    stream=$(echo "$active_data" | jq -r '.[0].milestone.title // empty')
  fi
fi

# Query blocked count
blocked_count=$(gh issue list --label "blocked" --state open --json number 2>/dev/null | jq 'length' || echo "0")

# Query open PR count
open_pr_count=$(gh pr list --state open --json number 2>/dev/null | jq 'length' || echo "0")

# Query milestones for stream info
milestones=$(gh api "repos/${REPO}/milestones" --jq '[.[] | {title: .title, open: .open_issues, closed: .closed_issues}]' 2>/dev/null || echo "[]")

# Build state JSON
state=$(jq -n \
  --argjson active "$active_issue_json" \
  --arg stream "${stream:-}" \
  --argjson blocked "$blocked_count" \
  --argjson prs "$open_pr_count" \
  --argjson milestones "$milestones" \
  --arg updated "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  '{
    active_issue: $active,
    stream: (if $stream == "" then null else $stream end),
    blocked_count: $blocked,
    open_pr_count: $prs,
    milestones: $milestones,
    updated_at: $updated
  }'
)

# Write state file
echo "$state" > "$STATE_FILE"
echo "FLOW state updated: $STATE_FILE"

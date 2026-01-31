#!/bin/bash
# FLOW-aware statusline for Claude Code
# Reads cached state from .flow/state.json (fast, no network calls)

set -e

# Read Claude Code's JSON input from stdin
input=$(cat)

# Extract standard fields
model=$(echo "$input" | jq -r '.model.display_name // .model.id // "?"')
context=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | xargs printf "%.0f")
cost=$(echo "$input" | jq -r '.cost.total_cost_usd // 0' | xargs printf "%.2f")

# Get git info (fast local operations)
branch=$(git branch --show-current 2>/dev/null || echo "")
dirty=""
if [[ -n $(git status --porcelain 2>/dev/null) ]]; then
  dirty=" *"
fi

# Read cached FLOW state (no network, instant)
state_file=".flow/state.json"
flow_part=""

if [[ -f "$state_file" ]]; then
  active_num=$(jq -r '.active_issue.number // empty' "$state_file" 2>/dev/null)
  active_title=$(jq -r '.active_issue.title // empty' "$state_file" 2>/dev/null | cut -c1-25)
  stream=$(jq -r '.stream // empty' "$state_file" 2>/dev/null)
  blocked=$(jq -r '.blocked_count // 0' "$state_file" 2>/dev/null)
  open_prs=$(jq -r '.open_pr_count // 0' "$state_file" 2>/dev/null)

  if [[ -n "$active_num" ]]; then
    # Active work: show issue info
    flow_part="#${active_num} ${active_title}"
    [[ -n "$stream" ]] && flow_part="${flow_part} | ${stream}"
  elif [[ -n "$branch" ]]; then
    # No active issue but on a branch
    flow_part="$branch"
  fi

  # Add indicators for blocked/PRs
  indicators=""
  [[ "$blocked" -gt 0 ]] && indicators="${indicators} | ${blocked} blocked"
  [[ "$open_prs" -gt 0 ]] && indicators="${indicators} | ${open_prs} PR"
  flow_part="${flow_part}${indicators}"
else
  # No state file - just show branch
  [[ -n "$branch" ]] && flow_part="$branch"
fi

# Build final output
# Format: [Model] flow_context | git_dirty | context% | $cost
output="[${model}]"
[[ -n "$flow_part" ]] && output="${output} ${flow_part}"
[[ -n "$dirty" ]] && output="${output}${dirty}"
output="${output} | ${context}% | \$${cost}"

echo "$output"

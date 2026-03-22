---
description: FLOW Ship - Commit, push, and create PR
---

<!--
  PROCEDURAL SKILL - Multi-stage shipping workflow.
  Uses subagents for verification and summarization substeps.
-->

**MODEL:** Sonnet (all steps)
**EXECUTION:** Partial background (verification bg, PR creation fg)
## Usage

```
/flow-ship
```

Ship the current work:

## 0. Self-Review Gate (BLOCKING -- do this first)

Before anything else, re-read the original task:

```bash
git branch --show-current  # Extract issue number from branch name
```

If there's an issue number, read it:
```bash
gh issue view <number> --json title,body -q '.title + "\n\n" + .body' 2>/dev/null
```

**Now compare**: read the issue's acceptance criteria line by line. For each item, verify it was actually implemented. If ANY AC item was not done and is not blocked, **STOP and implement it before continuing**. Do not ship incomplete work.

## 0b. Session Debt Check (BLOCKING)

Check for any unresolved errors or warnings from this session. If a session debt tracking script exists:

```bash
python3 .claude/hooks/check-session-debt.py 2>/dev/null || echo "No session debt tracker"
```

If there are unresolved items:
- If you caused it: **fix it now**
- If it's pre-existing: note it in the PR description
- If it's a false positive: clear it and explain why

**Do not proceed to shipping until all items are justified.**

## 0c. New TODO/FIXME Check (BLOCKING)

```bash
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name')
git diff origin/$DEFAULT_BRANCH...HEAD | grep -n '^\+.*\(TODO\|FIXME\|HACK\|XXX\)' || echo "Clean"
```

If new TODO/FIXME markers were introduced, each one MUST have a linked issue number. Bare TODOs without issue references are not acceptable -- either fix the issue now or create a GitHub issue and reference it.

## 1. Pre-Flight Check

```bash
git status                 # Check for uncommitted changes
```

## 2. Background Verification

If there are code changes, run verification checks:

```bash
# Run project-specific linters/formatters (adjust to your project)
# Examples:
# Python: ruff check . && black --check .
# JavaScript: eslint . && prettier --check .
# Rust: cargo clippy && cargo fmt --check
# Go: golangci-lint run && gofmt -l .
```

## 3. Stage and Commit

If uncommitted changes exist:

```bash
git diff --stat           # Review what changed
git add <relevant-files>  # Stage (exclude .env, credentials, etc.)
```

### Generate Commit Message

Analyze the diff and generate a conventional commit message:

```bash
git diff --cached --stat && git diff --cached
```

Generate commit message following conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `refactor:` Code restructuring
- `docs:` Documentation
- `test:` Tests
- `chore:` Maintenance

Format:
```
<type>(<scope>): <short description>

<body with details if needed>
```

Create commit:
```bash
git commit -m "<generated-message>

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## 4. Check Verification Results

If verification was run in background, check the results.

### If verification passed:
```
Verification complete

   Lint: passed
   Format: passed
   Ready for PR creation.
```

### If verification failed:
```
Verification failed

   <error details>

   Fix the errors and run /flow-ship again.
```

**Stop here if verification failed.** Do not create PR.

## 5. Verify Issue Checklist

Before creating PR, check that acceptance criteria are complete:

```bash
# Get issue description and count unchecked items
gh issue view <number> --json body -q '.body' | grep -c '\- \[ \]' || echo 0
```

### If unchecked items remain:

```
Issue #<number> has <count> unchecked acceptance criteria:

   - [ ] <unchecked item 1>
   - [ ] <unchecked item 2>

   [u] Update checklist (mark items done)
   [c] Continue anyway (partial completion)
   [a] Abort shipping
```

If user chooses "Update checklist":
```bash
# Update description to check off completed items
gh issue view <number> --json body -q '.body' > /tmp/desc.md
# Edit /tmp/desc.md to mark completed items
gh issue edit <number> --body-file /tmp/desc.md
```

## 6. Push and Create PR

```bash
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name')
git log origin/$DEFAULT_BRANCH..HEAD --oneline  # See all commits for PR
git push -u origin <branch>
```

Create PR. **Test plan checkboxes must reflect actual verification results** -- if a check passed in step 4, write it as `[x]`. Only leave `[ ]` for items that were NOT verified:

```bash
gh pr create \
  --title "<descriptive title from commits>" \
  --body "$(cat <<'EOF'
## Summary
<bullet points of changes>

## Test plan
- [x/space] Lint passes
- [x/space] Format passes
- [x/space] Tests pass
- [x/space] No errors in logs
- [x/space] Feature works end-to-end

Closes #<issue-number>

Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Use `[x]` for verified items, `[ ]` for unverified. For non-code PRs (docs, config), only include relevant test plan items -- don't add inapplicable checkboxes.

## 7. Update State

```bash
# Update issue labels (remove active, add review status)
gh issue edit <number> \
  --remove-label "status::active" \
  --add-label "status::review"
```

## 8. Report

```
## Shipped: #<number> <title>

**PR:** <pr-url>
**Commits:** <count>
**Verification:** passed / skipped

Ready for review.
```

## Notes

- Background verification saves time -- runs while you stage/commit
- Always stop if verification fails -- don't create broken PRs
- Checklist items should be updated during implementation, not just at ship time
- **Partial completion is NOT OK** unless items are genuinely blocked. If you can do it, do it now.
- The self-review gate (step 0) is the most important step -- it catches scope drift and forgotten AC items
- Session debt check (step 0b) catches errors you caused and ignored during the session

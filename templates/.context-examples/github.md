# GitHub Integration

> GitHub workflows, permissions, and Claude integration details.

## Repository

- **Repo**: `{{GITHUB_ORG}}/{{GITHUB_REPO}}` (private)
- **URL**: https://github.com/{{GITHUB_ORG}}/{{GITHUB_REPO}}

## Claude Code GitHub Workflows

### 1. Interactive Claude Assistance (`claude.yml`)

**Trigger**: Mention `@claude` in issues, PRs, or comments.

```
@claude Please review this implementation
@claude Help me debug this issue
@claude Create tests for this feature
```

### 2. Automatic Code Review (`claude-code-review.yml`)

**Trigger**: PR opened or updated.

Reviews: code quality, bugs, performance, security, test coverage.

## Secrets Required

- `CLAUDE_CODE_OAUTH_TOKEN`: OAuth token for Claude Code GitHub Actions

## Permissions

Claude has access to:
- Repository contents (read)
- Pull requests (read)
- Issues (read)
- CI/CD results (read)
- GitHub CLI commands (via allowed-tools)

### Allowed GitHub CLI Commands

```bash
gh issue view:*      # View issue details
gh search:*          # Search repository
gh issue list:*      # List issues
gh pr comment:*      # Comment on PRs
gh pr diff:*         # View PR diffs
gh pr view:*         # View PR details
gh pr list:*         # List PRs
```

## CLI Usage Examples

```bash
# Create issue with Claude help
gh issue create --title "Feature request" --body "@claude Please help implement..."

# Comment on existing issue
gh issue comment 123 --body "@claude Review my approach"

# Create PR (triggers auto-review)
gh pr create --title "Add feature" --body "Description"

# Ask Claude in PR
gh pr comment 123 --body "@claude Fix the failing tests"
```

## Resources

- Actions: https://github.com/{{GITHUB_ORG}}/{{GITHUB_REPO}}/actions
- Issues: https://github.com/{{GITHUB_ORG}}/{{GITHUB_REPO}}/issues
- PRs: https://github.com/{{GITHUB_ORG}}/{{GITHUB_REPO}}/pulls
- Claude Code Action: https://github.com/anthropics/claude-code-action

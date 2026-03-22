# Changelog

All notable changes to the claude-code-workflow project.

## [Unreleased] -- 2026-03-22

### Added

#### Hooks (`.claude/hooks/`)
- `session-debt.py` -- PostToolUse hook that tracks errors/warnings to `.flow/session-debt.jsonl`
- `check-session-debt.py` -- Completion gate that blocks shipping with unresolved session debt
- `clear-session-debt.py` -- Utility to clear the session debt ledger
- `session-context.py` -- SessionStart hook that surfaces unreflected learnings and clears previous debt
- `failure-logger.py` -- PostToolUse hook that captures command failures to `.flow/learnings.jsonl`
- `pre-edit-guard.py` -- PreToolUse hook that warns on anti-pattern matches in edited code
- `patterns.json` -- Configurable regex patterns for pre-edit-guard (Python, TypeScript, JavaScript, Go, Ruby)

#### .context Templates
- `substrate.md` -- Navigation hub with placeholder sections for project name, modules, dependencies, streams, dev environment, deployment, AI usage
- `ai-rules.md` -- Coding standards template with framework version, naming, architecture, security, testing, commits
- `glossary.md` -- Domain terminology template with example entry format
- `anti-patterns.md` -- Template with 4 generic anti-patterns: hardcoded credentials, bare external imports, reinventing framework patterns, missing scope filters
- `debt.md` -- Technical debt tracker with severity/effort/status columns
- `handover/workstation.md` -- Per-workstation session handover template

#### Architecture Decision Records
- `ADR-TEMPLATE.md` -- Standard ADR format (status, context, decision, consequences, alternatives)
- `ADR-001-multi-workstation-agents.md` -- The multi-worktree agent model: isolated workstations per role
- `ADR-002-agentic-estimation-model.md` -- Sessions, gates, and agent-slots estimation framework

#### CLAUDE.md Templates
- `CLAUDE.md.global` -- Personal preferences + .context system instructions
- `CLAUDE.md.directory` -- Shared standards for project groups, role definitions
- `CLAUDE.md.project` -- Project-level version compliance, language rules, security, workflow
- `CLAUDE.md.workstation` -- Role-bound template with completion standards, git safety, scope boundaries
- `.gitattributes` -- Merge protection for branch-specific CLAUDE.md files

#### Examples
- `completion-standards.md` -- Full NON-NEGOTIABLE section: error ownership, anti-deferral, definition of done, self-review
- `anti-deferral-rules.md` -- Expanded anti-deferral rules with valid/invalid blocker tables
- `role-definitions.md` -- All 5 roles with responsibilities, boundaries, and personality profiles

#### Docs
- `WORKSTATIONS.md` -- Complete guide to setting up named workstations with git worktrees
- `MIGRATION_V1_TO_V2.md` -- Migration guide from file-based FLOW v1 to GitHub-native v2 (moved from root)

#### .flow Templates
- `state.json` -- Cross-workstation state template
- `.gitignore` -- Ignores session-debt.jsonl, learnings.jsonl, state.json

### Changed
- Rewrote `GUIDE.md` to reflect current system: skills (not commands), hooks, workstations, completion standards
- Updated `.context/substrate.md` template with module inventory, dependency tree, streams, deployment targets
- Updated `.context/ai-rules.md` template with framework-agnostic structure
- Updated `.context/anti-patterns.md` template with generic examples (was TypeScript-specific)
- Updated `.context/glossary.md` template with clearer entry format
- Replaced `templates/global-claude-md.md` with 4 CLAUDE.md templates at different hierarchy levels

### Removed
- `FLOW_V2_MIGRATION.md` from root (moved to `docs/MIGRATION_V1_TO_V2.md`)
- `templates/global-claude-md.md` (replaced by `templates/CLAUDE.md.global`)
- `templates/.context/SESSION_HANDOVER.md` (replaced by `templates/.context/handover/workstation.md`)

## [0.1.0] -- 2026-03-08

### Added
- Initial snapshot: GUIDE.md, README.md, basic .context templates
- FLOW v2 migration document
- MIT License

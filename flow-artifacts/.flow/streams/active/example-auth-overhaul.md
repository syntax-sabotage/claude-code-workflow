# Stream: Authentication Overhaul

> Add OAuth providers and improve auth UX while maintaining security.

**Status:** `active`
**Created:** 2025-01-20
**Target:** 2025-02-15
**Lead:** @developer + claude-agent-1

## Objective

Users can authenticate via OAuth providers (Google, GitHub) in addition to email/password, with seamless account linking for users who sign up with email then later connect OAuth.

## Success Criteria

- [x] Google OAuth working in staging
- [ ] GitHub OAuth working in staging
- [ ] Account linking flow implemented
- [ ] Existing users can connect OAuth without losing data
- [ ] Security review completed
- [ ] Production deployment successful

## Current State

### Active Objectives

| ID | Objective | Status | Owner |
|----|-----------|--------|-------|
| OBJ-042 | Implement GitHub OAuth provider | `in_progress` | claude-agent-1 |
| OBJ-043 | Design account linking UX | `in_progress` | @developer |

### Completed Objectives

| ID | Objective | Completed | Learnings |
|----|-----------|-----------|-----------|
| OBJ-040 | Research OAuth libraries | 2025-01-21 | Arctic better than next-auth for our setup |
| OBJ-041 | Implement Google OAuth | 2025-01-24 | Need to handle email scope separately |

### Blocked

| ID | Objective | Blocked By | Since |
|----|-----------|------------|-------|
| OBJ-044 | Production deployment | Security review not scheduled | 2025-01-25 |

## Context

### Why This Stream?

User feedback consistently requests "Login with Google" - currently 34% of signup abandonment happens at password creation step. Also reduces password reset support burden.

Related: GitHub Issue #89, User Research Doc (Notion)

### Scope Boundaries

**In scope:**
- Google and GitHub OAuth
- Account linking
- Session management updates
- Auth-related UI changes

**Out of scope:**
- Apple Sign-In (future stream)
- 2FA/MFA (separate security stream)
- Admin impersonation features

### Dependencies

| Dependency | Type | Status |
|------------|------|--------|
| Database migration for oauth_accounts | `technical` | `completed` |
| Security team review | `external` | `pending` |
| Design system button components | `stream` | `completed` |

### Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| OAuth token storage security | `high` | Using encrypted columns, following OWASP |
| Account linking edge cases | `medium` | Extensive test coverage, manual QA |
| Provider API changes | `low` | Abstraction layer for providers |

## Architecture Notes

- Using Arctic library for OAuth (lighter than alternatives)
- OAuth accounts stored in separate `oauth_accounts` table, linked to `users`
- Tokens encrypted at rest using project encryption key
- Refresh token rotation enabled for all providers

**Decision:** Chose separate table over JSON column for oauth data - better queryability, cleaner migrations, type safety with Drizzle.

## Learnings Log

| Date | Learning | Action |
|------|----------|--------|
| 2025-01-21 | Arctic requires Node 18+ | Updated CI pipeline |
| 2025-01-24 | Google email scope needs explicit request | Added to provider config |
| 2025-01-24 | Session invalidation needed after OAuth link | Added to account linking flow |

## Completion Checklist

When all success criteria are met:

- [ ] All objectives completed or consciously deferred
- [ ] Learnings reviewed and captured
- [ ] Relevant updates made to `.context/` docs
- [ ] Metrics updated in `.flow/metrics/`
- [ ] Stream moved to `streams/completed/`
- [ ] Celebration (optional but recommended)

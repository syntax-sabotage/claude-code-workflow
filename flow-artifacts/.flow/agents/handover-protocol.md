# Agent Handover Protocol

> How context transfers between agents and sessions.

## Why Handover Matters

AI agents don't persist between sessions. Every new Claude Code invocation starts fresh. Without explicit handover, work context is lost, leading to:

- Repeated exploration of same code
- Contradictory decisions across sessions
- Lost momentum on complex tasks
- Inconsistent code patterns

## Handover Types

### 1. Session End Handover

When a human ends a session or context window fills:

**Agent Responsibility:**

```markdown
Before session ends, update:

1. `.flow/FLOW.md` - Active streams status
2. Relevant `streams/active/*.md` - Current state
3. `.context/SESSION_HANDOVER.md` - Immediate context
4. Any objective work logs
```

**Handover Content:**

```markdown
## Session Handover - [DATE TIME]

### What Was Done
- Completed OBJ-042 (GitHub OAuth implementation)
- Started OBJ-043 (account linking UX)
- Fixed bug in token refresh logic

### Current State
- On branch: `42-github-oauth`
- PR #67 created, awaiting review
- OBJ-043 is 40% complete, paused at linking flow

### Immediate Next Steps
1. Finish account linking UI component
2. Add tests for edge cases (existing email, no email from provider)
3. Update API docs with new endpoints

### Blockers
- None currently

### Decisions Made
- Chose to store OAuth state in session cookie (not DB)
- Using 5-minute expiry for OAuth state tokens

### Open Questions
- Should we auto-link accounts with same email? (security implications)
```

---

### 2. Agent-to-Agent Handover

When one agent hands off to another (e.g., specialized agent, different model):

**Trigger:** Explicit handover command or automatic on agent switch.

**Protocol:**

```markdown
## Agent Handover

**From:** claude-opus-session-abc
**To:** claude-sonnet-session-def
**Timestamp:** 2025-01-25T15:30:00Z

### Context Transfer

**Active Stream:** auth-overhaul
**Active Objective:** OBJ-043 (account linking UX)
**Autonomy Level:** 2

### State Summary
[Concise summary of current work state]

### Files Modified This Session
- `src/auth/oauth/link.ts` - New file, 80% complete
- `src/components/AccountLinkButton.tsx` - New file, complete
- `src/auth/oauth/providers.ts` - Added GitHub config

### Uncommitted Changes
[Git diff summary or "all committed"]

### Critical Context
- Using Arctic library for OAuth (not next-auth)
- Token storage is encrypted, see `src/auth/encryption.ts`
- Account linking should NOT auto-merge without user confirmation

### Warnings
- Don't modify `src/auth/session.ts` without reading comments
- Test user "test@example.com" has linked accounts for testing
```

---

### 3. Stream Handover

When responsibility for a stream transfers (human vacation, agent rotation):

**Protocol:**

Update stream file:

```markdown
## Stream Handover - [DATE]

**Previous Lead:** @developer-a
**New Lead:** @developer-b + claude-agent-2

### Stream State
[Current completion %, active objectives, blockers]

### Key Decisions Made
[Decisions the new lead needs to know]

### Tribal Knowledge
[Things not in docs that matter]

### Upcoming Challenges
[What's coming that needs attention]
```

---

## Handover Quality Checklist

Good handover includes:

- [ ] **What:** Clear description of completed and in-progress work
- [ ] **Where:** File paths, branch names, PR numbers
- [ ] **Why:** Decisions made and their rationale
- [ ] **What's Next:** Concrete next steps, not vague directions
- [ ] **Warnings:** Gotchas, things to avoid, non-obvious constraints
- [ ] **Questions:** Unresolved issues that need attention

## Handover Commands

### `/flow-handover`

Generate handover document:

```markdown
---
description: Generate session handover document
---

Create a handover document for the current session:

1. Summarize what was accomplished
2. Document current state (branch, uncommitted changes, active objectives)
3. List decisions made with rationale
4. Identify next steps
5. Note any blockers or open questions
6. Update `.context/SESSION_HANDOVER.md`
7. Update relevant `.flow/streams/active/*.md` files
```

### `/flow-resume`

Resume from handover:

```markdown
---
description: Resume work from handover state
---

Resume work on this project:

1. Read `.context/SESSION_HANDOVER.md` for immediate context
2. Read `.flow/FLOW.md` for active streams overview
3. Check active stream files for current objectives
4. Run `git status` and `git log -5` to verify state
5. Present summary of current state and recommended next action
```

## Failure Modes

### Incomplete Handover

**Symptom:** Next session doesn't know current state.
**Cause:** Session ended abruptly or handover skipped.
**Recovery:**
1. Check git log for recent commits
2. Check PR history for context
3. Review `.flow/` files for last known state
4. Ask human for context if unclear

### Conflicting Handovers

**Symptom:** Multiple agents updated state inconsistently.
**Cause:** Parallel work without coordination.
**Recovery:**
1. Compare timestamps to find most recent
2. Merge states manually
3. Establish single source of truth
4. Improve coordination protocol

### Stale Handover

**Symptom:** Handover references outdated state.
**Cause:** Work continued after handover was written.
**Recovery:**
1. Trust git state over handover document
2. Update handover with current state
3. Note discrepancy in learnings

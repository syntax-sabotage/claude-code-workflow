# Agent Registry

> Active and historical agents working on this project.

## Active Agents

| Agent ID | Type | Autonomy Level | Primary Stream | Last Active |
|----------|------|----------------|----------------|-------------|
| @developer | Human | 3 | all | 2025-01-25 |
| claude-main | Claude Code | 2 | auth-overhaul | 2025-01-25 |

## Agent Profiles

### @developer

**Type:** Human
**Level:** 3 (Full)
**Capabilities:** All
**Contact:** <!-- email/slack -->

---

### claude-main

**Type:** Claude Code (Opus)
**Level:** 2 (Autonomous)
**Assigned Streams:** auth-overhaul, performance
**Restrictions:**
- No production deploys
- No security code without review

**Session History:**

| Session | Date | Duration | Objectives Completed |
|---------|------|----------|---------------------|
| session-abc | 2025-01-25 | 2h | OBJ-042, OBJ-041 (partial) |
| session-xyz | 2025-01-24 | 1.5h | OBJ-040, OBJ-039 |

**Notes:**
- Performs well on OAuth implementation
- Tends to over-engineer error handling (acceptable)

---

## Adding New Agents

When a new agent joins:

1. Add entry to this registry
2. Assign initial autonomy level (usually 0 or 1)
3. Point to onboarding reading:
   - `.context/substrate.md`
   - `.context/ai-rules.md`
   - `.flow/FLOW.md`
   - `.flow/agents/autonomy-levels.md`
4. Assign initial supervised task
5. Update autonomy level as trust builds

## Removing Agents

When an agent is retired:

1. Ensure handover is complete
2. Move to Historical Agents section
3. Archive any agent-specific context
4. Reassign active objectives

## Historical Agents

| Agent ID | Type | Active Period | Objectives Completed | Reason for Removal |
|----------|------|---------------|---------------------|-------------------|
| claude-pilot | Claude Code | 2025-01-01 to 2025-01-15 | 12 | Project phase completed |

## Agent Performance

### Metrics by Agent

| Agent | Objectives Completed | Avg Cycle Time | Rework Rate |
|-------|---------------------|----------------|-------------|
| @developer | 45 | 2.3 days | 5% |
| claude-main | 23 | 0.8 days | 8% |

### Trust Events

| Date | Agent | Event | Impact |
|------|-------|-------|--------|
| 2025-01-20 | claude-main | Promoted 1→2 | Can now create PRs |
| 2025-01-15 | claude-pilot | Retired | Clean handover |

# FLOW Ceremonies

> Async rituals that keep work flowing.

## Philosophy

Traditional agile has synchronous ceremonies (standups, planning, retros). FLOW replaces these with async equivalents that:

- Don't require everyone online at once
- Can be performed by agents or humans
- Happen when needed, not on calendar
- Leave written artifacts

## Ceremony Reference

| Ceremony | Replaces | Frequency | Typical Duration | Who |
|----------|----------|-----------|------------------|-----|
| Triage | Sprint Planning | Continuous | 15 min/batch | Any |
| Stream Sync | Daily Standup | As needed | Written | Stream lead |
| Reflection | Sprint Retro | Per stream completion | 30 min | Team |
| Health Check | Scrum of Scrums | Weekly | Written | Any |

---

## Triage

**Replaces:** Sprint planning, backlog grooming

**Purpose:** Move objectives from pool to streams.

**Trigger:** Pool has 5+ objectives OR high-priority item arrives

**Process:**

1. Review objective pool
2. For each objective:
   - Does it fit an existing stream?
   - Is it urgent enough to create a new stream?
   - Should it wait?
3. Assign to stream and owner
4. Update pool.md

**Artifact:** Updated `objectives/pool.md`, stream files

**Command:** `/flow-triage`

```markdown
---
description: Triage objective pool
---

Process the objective pool:

1. Read `.flow/objectives/pool.md`
2. Read active streams in `.flow/streams/active/`
3. For each pooled objective:
   - Assess fit with existing streams
   - Recommend assignment or deferral
4. Present triage recommendations
5. On approval, update pool.md and stream files
```

---

## Stream Sync

**Replaces:** Daily standup

**Purpose:** Keep stream state current and visible.

**Trigger:**
- When starting work on a stream
- When completing an objective
- When blocked
- At least every 48 hours if stream is active

**Process:**

1. Update stream file with current state
2. Note any blockers
3. Update objective statuses
4. Flag if help needed

**Artifact:** Updated `streams/active/[stream].md`

**Command:** `/flow-sync`

```markdown
---
description: Update stream state
---

Sync current stream state:

1. Identify current stream from branch name or context
2. Read stream file
3. Update:
   - Active objectives status
   - Any new blockers
   - Recent completions
   - Learnings captured
4. Commit updated stream file
```

---

## Reflection

**Replaces:** Sprint retrospective

**Purpose:** Capture learnings when a stream completes.

**Trigger:** Stream reaches "completed" status

**Process:**

1. Review stream from start to finish
2. Identify what went well
3. Identify what could improve
4. Extract learnings for future
5. Update relevant `.context/` docs
6. Archive stream

**Artifact:** Completed stream file with reflection, `.context/` updates

**Command:** `/flow-reflect`

```markdown
---
description: Reflect on completed stream
---

Conduct stream reflection:

1. Read completed stream file
2. Review all objectives and learnings
3. Generate reflection:
   - What went well?
   - What was harder than expected?
   - What would we do differently?
   - What should be documented for future?
4. Propose `.context/` updates (patterns, anti-patterns, etc.)
5. Move stream to completed/
```

### Reflection Template

```markdown
## Stream Reflection: [Name]

**Completed:** [Date]
**Duration:** [X weeks]
**Objectives:** [Completed] / [Total]

### What Went Well
-

### What Was Challenging
-

### Key Learnings
-

### Documentation Updates Made
- Updated `.context/auth/` with OAuth patterns
- Added token rotation to anti-patterns

### Recommendations
-
```

---

## Health Check

**Replaces:** Scrum of scrums, team sync

**Purpose:** Overall project health assessment.

**Trigger:** Weekly, or when metrics indicate problems

**Process:**

1. Review all active streams
2. Check metrics for alerts
3. Identify systemic issues
4. Propose interventions

**Artifact:** Updated `metrics/overview.md`, action items

**Command:** `/flow-health`

```markdown
---
description: Check overall FLOW health
---

Assess project health:

1. Read all active streams
2. Calculate current metrics
3. Check for:
   - Stalled streams (no progress 3+ days)
   - Growing blockers
   - Declining throughput
   - Rising rework rate
4. Generate health report
5. Propose actions for any concerns
```

### Health Report Template

```markdown
## Health Check: [Date]

### Stream Status
| Stream | Health | Concern |
|--------|--------|---------|
| | | |

### Metrics Summary
- Throughput: [trend]
- Cycle Time: [trend]
- Blockers: [count]

### Alerts
-

### Recommended Actions
-
```

---

## Ceremony Calendar

While ceremonies are async, some cadence helps:

| Day | Recommended Activity |
|-----|---------------------|
| Monday | Health check, triage if needed |
| Daily | Stream sync for active work |
| On completion | Stream reflection |
| As needed | Triage when pool grows |

---

## Anti-Patterns

### Ceremony Theater

**Problem:** Going through motions without value.
**Solution:** Skip ceremony if nothing to discuss. Async doesn't mean mandatory.

### Documentation Debt

**Problem:** Ceremonies done but artifacts not updated.
**Solution:** Ceremony isn't complete until artifacts are committed.

### Sync Creep

**Problem:** "Let's just hop on a call" for every decision.
**Solution:** Default to async. Sync only for high-bandwidth problem-solving.

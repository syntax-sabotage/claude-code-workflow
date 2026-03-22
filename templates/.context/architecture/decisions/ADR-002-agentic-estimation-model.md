<!-- ctx-type: decision -->
<!-- ctx-status: accepted -->

# ADR-002: Agentic Estimation Model

## Status

Accepted

## Context

Traditional estimation methods (story points, developer days, T-shirt sizing) assume human developer teams. In a human+AI team where one human works with multiple AI agents, these models break down:

- AI agents compress coding time by 5-10x compared to human developers
- A small ticket takes 10-20 minutes of agent time, a medium ticket 30-60 minutes
- But coding speed is **not the bottleneck** -- **human attention is**

The human must review PRs, approve designs, make product decisions, and provide context. The number of "gates" (human decision points) determines throughput, not agent coding speed.

## Decision

Estimate all work using three units:

### Units

| Unit | Definition | Example |
|------|-----------|---------|
| **Session** | One focused human+agent block. Typically 1-3 hours of the human's time. | "This is a 1-session task" |
| **Agent-slot** | One agent working independently. Multiple slots can run in parallel across workstations. | "These two tickets can run in 2 parallel agent-slots" |
| **Gate** | A point where the human must review, approve, or provide input before work continues. | "This needs 2 gates: design approval + PR review" |

### Estimation Format

When sizing work, state:

```
Sessions: 1
Agent-slots: 2 (parallel)
Gates: 3 (refinement approval, mid-implementation check, PR review)
Sequential chain: #A -> #B (cannot parallelize)
```

### Autonomy x Estimation

| Autonomy Level | Gates Required | Human Time Per Ticket |
|----------------|---------------|----------------------|
| `autonomy::0` | Many -- stop and ask at every decision | ~1 hour (high involvement) |
| `autonomy::1` | 2 -- confirm approach + review output | ~20-30 min |
| `autonomy::2` | 1 -- PR review only | ~10 min |
| `autonomy::3` | 0 -- agent ships, human merges | ~2 min |

**Force multiplier:** Promoting tickets from `autonomy::1` to `autonomy::2` via thorough refinement doubles the human's effective throughput. This makes refinement the highest-leverage activity.

### Size x Agent Time

| Size | Agent Implementation Time | Notes |
|------|--------------------------|-------|
| `size::xs` | 5-15 min | Config changes, single-field fixes |
| `size::s` | 10-20 min | Single-model changes, view updates |
| `size::m` | 30-60 min | Multi-file features, new models |
| `size::l` | 1-2 hours | Cross-module features, migrations |
| `size::xl` | 2-4 hours | Major features, architectural changes |

These are agent execution times, not calendar times. Calendar time depends on gates and dependencies.

### Bottleneck Analysis

| Resource | Constraint | Mitigation |
|----------|-----------|------------|
| Human attention | Single human, every low-autonomy ticket needs them | Maximize `autonomy::2-3` tickets via thorough refinement |
| Sequential dependencies | Some tickets must land before others can start | Identify chains during refinement, minimize them |
| Testing/CI | Build + test execution takes real clock time | Can't parallelize beyond the number of workstation instances |
| Agent coding speed | Almost never the bottleneck | Not worth optimizing |

## Consequences

- All issue descriptions, refinement comments, and handover notes use session/gate/slot language
- Never estimate in "developer days" or "story points"
- Refinement explicitly states the gate count and parallelization potential
- Sprint planning (if adopted) counts the human's available sessions, not agent capacity
- Throughput optimization focuses on reducing gates (better refinement -> higher autonomy) and breaking sequential chains

## Alternatives Considered

### Story Points
Abstract but calibrated to human teams. Doesn't capture the human-bottleneck dynamic. A 3-point ticket that needs 3 human approvals takes longer than an 8-point ticket that runs autonomously.

### Developer Hours
Misleading -- implies coding time is the constraint. In an agentic team, coding is the cheap part.

### T-shirt Sizing Only
Too vague -- doesn't distinguish "easy but needs 3 approvals" from "hard but fully autonomous." The gate count is the critical missing dimension.

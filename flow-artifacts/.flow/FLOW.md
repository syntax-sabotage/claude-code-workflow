# FLOW Hub

> Fluid Learning Optimization Workflow - AI-native development without sprints.

**Current State:** Active development
**Active Streams:** <!-- count -->
**Pending Objectives:** <!-- count -->

## Quick Navigation

| Section | Purpose |
|---------|---------|
| [streams/active/](./streams/active/) | Currently flowing work |
| [objectives/](./objectives/) | Objective backlog and templates |
| [agents/](./agents/) | Agent configuration and protocols |
| [metrics/](./metrics/) | Stream health and throughput |
| [ceremonies/](./ceremonies/) | Async rituals and triggers |

## Active Streams

<!-- Auto-updated or manually maintained -->

| Stream | Objective Count | Health | Lead |
|--------|-----------------|--------|------|
| <!-- stream name --> | <!-- n --> | <!-- status --> | <!-- human/agent --> |

## How FLOW Works

### Core Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                        OBJECTIVE POOL                            │
│   Unassigned objectives waiting for stream placement            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Triage (continuous)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ACTIVE STREAMS                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Stream A   │  │  Stream B   │  │  Stream C   │             │
│  │  ────────►  │  │  ────────►  │  │  ────────►  │             │
│  │  obj→obj→   │  │  obj→obj→   │  │  obj→       │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Completion (when ready)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         SHIPPED                                  │
│   Released to production, stream archived with learnings        │
└─────────────────────────────────────────────────────────────────┘
```

### Key Differences from Sprint-Based

| Sprint-Based | FLOW |
|--------------|------|
| Work batched into 2-week cycles | Work flows continuously |
| Planning meetings before sprint | Triage happens as objectives arrive |
| Demo at sprint end | Ship when ready |
| Retro after sprint | Continuous learning capture |
| Fixed team capacity per sprint | Elastic capacity (agents scale) |

## Integration with .context/

FLOW builds on top of the `.context/` knowledge system:

```
project/
├── .context/           # Project knowledge (static-ish)
│   ├── substrate.md    # Tech stack, architecture
│   ├── ai-rules.md     # Coding constraints
│   ├── anti-patterns.md
│   └── glossary.md
│
└── .flow/              # Work coordination (dynamic)
    ├── FLOW.md         # This file - hub
    ├── streams/        # Active work
    ├── objectives/     # What needs doing
    ├── agents/         # Who/what does it
    ├── metrics/        # How's it going
    └── ceremonies/     # Rituals and triggers
```

**Rule:** `.context/` = what we know, `.flow/` = what we're doing

## Commands

| Command | Purpose |
|---------|---------|
| `/flow-status` | Overview of all streams and objectives |
| `/flow-triage` | Process objective pool, assign to streams |
| `/flow-ship` | Complete objective, update metrics, capture learnings |
| `/flow-stream <name>` | Create or switch to a stream |
| `/flow-objective <title>` | Create new objective |

## Getting Started

1. Read [agents/autonomy-levels.md](./agents/autonomy-levels.md) - understand trust boundaries
2. Check [streams/active/](./streams/active/) - see current work
3. Run `/flow-status` - get oriented
4. Pick up work or create objectives

## Principles

1. **Ship when ready** - No waiting for sprint boundaries
2. **Context is king** - Agents maintain perfect memory via `.context/` + `.flow/`
3. **Streams over sprints** - Related objectives flow together
4. **Async by default** - No synchronous ceremonies required
5. **Learn continuously** - Every completion captures learnings

# Objective Pool

> Unassigned objectives waiting for triage into streams.

**Last Triage:** <!-- DATE -->
**Pool Size:** <!-- count -->

## Triage Process

Run `/flow-triage` or manually:

1. Review each pooled objective
2. Determine if it fits an existing stream
3. If yes: assign to stream, set owner
4. If no: create new stream or mark for later
5. Update this file

## Pooled Objectives

### High Priority

| ID | Title | Size | Created | Notes |
|----|-------|------|---------|-------|
| OBJ-050 | Fix memory leak in WebSocket handler | S | 2025-01-25 | Production impact |
| OBJ-051 | Add rate limiting to public API | M | 2025-01-25 | Security concern |

### Normal Priority

| ID | Title | Size | Created | Notes |
|----|-------|------|---------|-------|
| OBJ-052 | Improve error messages in form validation | S | 2025-01-24 | User feedback |
| OBJ-053 | Add dark mode support | L | 2025-01-23 | Feature request |
| OBJ-054 | Migrate to new email provider | M | 2025-01-22 | Cost reduction |

### Low Priority / Someday

| ID | Title | Size | Created | Notes |
|----|-------|------|---------|-------|
| OBJ-055 | Refactor legacy notification system | XL | 2025-01-15 | Tech debt |
| OBJ-056 | Add keyboard shortcuts | S | 2025-01-10 | Nice to have |

## Recently Assigned

| ID | Title | Assigned To | Stream | Date |
|----|-------|-------------|--------|------|
| OBJ-049 | Update OAuth callback URLs | claude-agent-1 | auth-overhaul | 2025-01-25 |
| OBJ-048 | Write auth migration guide | @developer | auth-overhaul | 2025-01-24 |

## Deferred

Objectives consciously postponed:

| ID | Title | Reason | Revisit |
|----|-------|--------|---------|
| OBJ-030 | Multi-language support | Not enough users yet | Q3 2025 |

## Quick Add

<!-- Drop new objectives here for later triage -->

```
- [ ] <!-- Quick objective note -->
```

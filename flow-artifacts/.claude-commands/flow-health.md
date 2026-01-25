---
description: FLOW Health Check
---

Assess overall project health:

1. Read all active streams from `.flow/streams/active/`
2. For each stream, assess:
   - Progress (objectives done vs total)
   - Blockers (count and age)
   - Last activity date
3. Read `.flow/metrics/overview.md`
4. Check for alerts:
   - Stalled streams (no progress 3+ days)
   - Growing blocker count
   - Objectives aging in pool
   - Declining throughput trend
5. Generate health report:
   - Overall status (healthy/concerning/critical)
   - Stream-by-stream assessment
   - Metrics summary
   - Recommended actions
6. Update `.flow/metrics/overview.md` with current data

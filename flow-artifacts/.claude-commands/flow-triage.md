---
description: Triage Objective Pool
---

Process the objective pool and assign to streams:

1. Read `.flow/objectives/pool.md` to see pending objectives
2. Read `.flow/streams/active/` to understand current streams
3. For each pooled objective:
   - Assess if it fits an existing stream
   - Assess priority and urgency
   - Recommend: assign to stream, create new stream, or defer
4. Present triage recommendations in a table:
   | Objective | Recommendation | Reason |
5. On approval, update:
   - `objectives/pool.md` - move from pool
   - Relevant stream file - add objective
   - Create new stream file if needed

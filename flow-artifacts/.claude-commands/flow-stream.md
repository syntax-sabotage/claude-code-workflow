---
description: Create or Switch Stream
---

Work with stream "$ARGUMENTS":

If stream exists:
1. Read `.flow/streams/active/$ARGUMENTS.md`
2. Show stream status, active objectives, blockers
3. Ask what to work on next

If stream doesn't exist (creating new):
1. Ask for:
   - Stream objective (what outcome?)
   - Success criteria
   - Initial scope
2. Create `.flow/streams/active/$ARGUMENTS.md` from template
3. Create git branch: `stream/$ARGUMENTS`
4. Report back with stream summary

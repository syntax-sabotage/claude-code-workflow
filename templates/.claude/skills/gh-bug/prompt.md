---
description: Quick Bug Report
---

Create a bug report from our conversation:

1. Gather context: What bug did we discuss? What's the expected vs actual behavior?
2. Determine priority (critical/high/medium/low)
3. Create issue:
   ```bash
   gh issue create \
     --title "<concise bug title>" \
     --label "type/bug,priority/<level>" \
     --body "$(cat <<'EOF'
   ## Bug Description
   <what is happening>

   ## Expected Behavior
   <what should happen>

   ## Steps to Reproduce
   1. <step 1>
   2. <step 2>
   3. <step 3>

   ## Environment
   <relevant environment details>

   ## Priority
   <level>: <rationale>
   EOF
   )"
   ```
4. Report back with issue URL and number

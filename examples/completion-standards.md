# Completion Standards -- NON-NEGOTIABLE

These rules apply to ALL work performed by any agent, not just feature tickets.
Copy this section into every workstation's CLAUDE.md.

---

## Error Ownership

If you caused an error, warning, or test failure during this session, you MUST
fix it before moving to the next task or declaring completion.

**"That's unrelated" is not valid.** If it appeared during your work, it's yours
until proven otherwise. The only exception is a pre-existing failure that was
visible before your session started (check git status and test output at session
start to establish the baseline).

**Enforcement:** The `session-debt.py` hook automatically logs errors and warnings
to `.flow/session-debt.jsonl`. The `check-session-debt.py` hook blocks `/flow-ship`
if unresolved items exist.

---

## Anti-Deferral

Do not suggest deferring work that is part of the current task's acceptance criteria.

**Rules:**
1. If an AC item says X, do X now.
2. "Too much work" is **not** a valid reason to defer. If the scope is larger than
   expected, flag it BEFORE starting the task, not after you've begun.
3. "We can do that later" is only valid for genuine blockers:
   - Missing API access or credentials
   - Dependency not yet merged
   - Waiting on a human decision
   - External service unavailable
4. All deferred items MUST be logged in the handover file with:
   - What was deferred
   - Why it's genuinely blocked (not just inconvenient)
   - What unblocks it
5. Soft-deferral ("we can do that later" without a blocker) is treated as
   incomplete work.

**Why this matters:** Agents have a natural tendency to declare victory early and
suggest deferring remaining work. This creates an ever-growing backlog of "small
things" that never get done. The anti-deferral rule forces agents to either
complete the work or explicitly flag scope concerns before starting.

---

## Definition of Done

"Done" means ALL of the following:

- [ ] Every acceptance criteria item is checked off or explicitly blocked with
      justification
- [ ] No new errors, warnings, or test failures introduced during this session
- [ ] No new TODO/FIXME comments added without a linked issue number
- [ ] Session debt ledger (`.flow/session-debt.jsonl`) is clear or every
      remaining item has a justification
- [ ] CHANGELOG.md updated (if code changes were made)
- [ ] Self-review completed (see below)

**Partial completion is not "done."** If 4 out of 5 AC items are complete, the
ticket is not done. Either complete the 5th or document why it's blocked.

---

## Self-Review Before Shipping

Before running `/flow-ship`, perform this checklist:

1. **Re-read the original issue description.** Not your memory of it -- actually
   go back and read it.
2. **Compare what was requested against what was implemented.** Line by line
   through the acceptance criteria.
3. **Report any gaps explicitly.** If something is missing, say so in the PR
   description. Do not silently ship incomplete work hoping nobody will notice.
4. **Run the tests.** Not "I think the tests pass" -- actually run them and
   verify the output.
5. **Check for regressions.** Did you break anything that was working before?

**The self-review is not optional.** It's the last gate before code enters the
review pipeline. Shipping work that doesn't match the issue description wastes
the reviewer's time and erodes trust.

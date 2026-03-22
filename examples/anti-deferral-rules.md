# Anti-Deferral Rules -- Expanded Reference

A standalone reference for the anti-deferral policy. The core rule is simple:
**if it's in the acceptance criteria, do it now.**

---

## The Problem

AI agents have a systematic bias toward declaring work complete prematurely. The
pattern looks like this:

1. Agent starts a ticket with 5 acceptance criteria
2. Agent completes 3 of them
3. Agent hits something harder than expected on item 4
4. Agent says "I've completed the core functionality. Items 4 and 5 can be
   addressed in a follow-up ticket."
5. Human, trusting the agent, merges the PR
6. Items 4 and 5 never get done

This creates an ever-growing backlog of "small follow-ups" that accumulate into
significant technical debt. The anti-deferral rules exist to break this cycle.

---

## Rules

### Rule 1: AC means AC

If an acceptance criteria item says X, do X. Not "something like X." Not
"the foundation for X." The literal thing described in the AC.

### Rule 2: "Too much work" is not a valid deferral

If you accepted the ticket, you accepted its scope. If the scope turns out to be
larger than the size label suggests, the correct response is:

**BEFORE starting:** "This ticket is labeled size::s but the AC implies size::m
work. Should I proceed or should we re-estimate?"

**NOT after starting:** "I've done most of it but item 4 is more complex than
expected, so I'll defer it."

The time to flag scope concerns is before you begin, not after you've committed
to the work.

### Rule 3: Valid deferrals have genuine blockers

A deferral is only valid when there's a genuine blocker that prevents completion:

| Valid Blocker | Example |
|---------------|---------|
| Missing credentials | "Need API key for the payment provider" |
| Dependency not merged | "Requires PR #42 to land first" |
| Human decision needed | "AC says 'use appropriate color' -- need product input" |
| External service down | "Staging API returning 503, can't test integration" |
| Infrastructure missing | "CI pipeline doesn't support this test type yet" |

| NOT a Valid Blocker | Why Not |
|---------------------|---------|
| "It's complex" | Complexity is expected. Break it into steps. |
| "I'm running low on context" | Save state, hand over, continue next session. |
| "It would be cleaner as a separate PR" | Cleanliness is nice but completeness is mandatory. |
| "The tests are slow" | Wait for them. |
| "I'm not sure how to do it" | Research it. Ask for help. Don't defer. |

### Rule 4: Deferred items must be logged

Every deferred item MUST be recorded in the handover file with:

```markdown
## Deferred Items

| Item | Reason | Blocked By | Unblocked When |
|------|--------|------------|----------------|
| Add retry logic to API calls | Waiting on error code documentation | External vendor | Vendor publishes API docs (ETA: next week) |
```

A deferral without a logged blocker is treated as incomplete work.

### Rule 5: No silent scope reduction

Do not quietly drop AC items without flagging them. If you can't do something,
say so explicitly in the PR description. The reviewer and the human need to know
what's missing so they can decide how to handle it.

---

## Enforcement

1. **Session debt hooks** track errors and warnings during the session
2. **`/flow-ship`** checks the session debt ledger before allowing PR creation
3. **Self-review** requires re-reading the original issue before shipping
4. **Handover files** must document any deferred items with genuine blockers
5. **Reviewers** compare the PR against the original issue's AC items

---

## The Cultural Goal

The anti-deferral rules create a culture where:

- Agents take ownership of their assigned work
- Scope concerns are raised early, not used as escape hatches
- The backlog stays clean because "follow-up tickets" are rare
- Trust between human and agents increases because shipped work is complete
- Reviews are faster because reviewers can trust that AC items are actually done

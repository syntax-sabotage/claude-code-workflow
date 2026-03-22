---
description: FLOW Reflect - Capture learnings from recent work
---

<!--
  ADAPTIVE SKILL - Upgrades to Opus for deep synthesis.

  UPGRADE CONDITIONS:
  - 6+ closed issues to reflect on -> spawn Opus
  - Otherwise use Sonnet

  Can run in BACKGROUND for large reflection jobs.
-->

**MODEL:** sonnet (adaptive - upgrades to opus at 6+ issues)
**EXECUTION:** background (for large reflections)
Synthesize learnings from recent work:

1. Run `gh issue list --state closed --limit 10 --json number,title,labels,body`
2. Run `gh pr list --state merged --limit 10 --json number,title,labels,body`
3. Read `.context/anti-patterns.md` for existing entries (if it exists)

For each closed issue/merged PR:
- What was the root cause?
- Were there unexpected complications?
- Did we discover a new anti-pattern or best practice?
- Should anything be added to `.context/` docs?

Then:
1. Read `.flow/learnings.jsonl` for entries where `reflected` is false (if file exists). Group by category. For each failure group: determine if it reveals a new anti-pattern (add to anti-patterns.md), a repeated known issue (note frequency), or a one-off (skip).
2. Mark all processed entries as `reflected: true` by rewriting `.flow/learnings.jsonl`.
3. Update `.context/anti-patterns.md` if new patterns found
4. Update `.context/ai-rules.md` if coding standards need refinement
5. Update `.context/glossary.md` if new terms emerged
6. Label reflected issues: `gh issue edit <number> --add-label "reflected"`
7. Present a summary of what was learned and what docs were updated.

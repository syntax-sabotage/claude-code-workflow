# Specifications Directory

This directory contains agent-optimized specifications created via `/odoo-spec`.

## Purpose

Specs serve as the **source of truth** for feature development before entering FLOW streams. They capture:

- **What problem** we're solving (not how)
- **Success criteria** (testable, measurable)
- **Scope boundaries** (what's in, what's explicitly out)
- **Constraints** (technical, time, dependencies)
- **Open questions** (to resolve before dev)

## Lifecycle

1. **Creation**: Product owner runs `/odoo-spec` → spec file created here
2. **Planning**: Spec fed to plan mode for implementation strategy
3. **Execution**: FLOW issues track implementation, reference spec
4. **Validation**: Check success criteria at ship time
5. **Archive**: Specs stay as historical record (git history = audit trail)

## Format

Specs are lightweight and agent-optimized. We avoid:
- ❌ Executive summaries
- ❌ Market analysis
- ❌ Stakeholder matrices
- ❌ Detailed technical designs (those emerge in plan mode)

We focus on:
- ✅ Unambiguous criteria
- ✅ Clear boundaries
- ✅ Testable outcomes
- ✅ Explicit non-goals

## Integration with FLOW

Use `--create-stream` flag to auto-generate:
- GitHub milestone (stream) from spec
- Epic issue linking to spec

```bash
/odoo-spec --create-stream
```

## Versioning

Specs are **living documents** during their active development:
- Update in place as understanding evolves
- Git history provides audit trail
- If requirements change drastically, create a **new spec** for the new problem

## Naming Convention

Filenames are derived from problem statement:
- Lowercase, hyphen-separated
- Descriptive but concise (~50 chars max)
- Example: `nextcloud-bidirectional-sync.md`

## Example Spec

See `.claude/commands/odoo-spec.md` for the template structure and guidance.

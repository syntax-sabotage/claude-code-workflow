<!-- ctx-type: decision -->
<!-- ctx-status: accepted -->

# ADR-001: Multi-Workstation Agent Model

## Status

Accepted

## Context

Projects that use multiple AI agents for different concerns (architecture, implementation, review, data engineering, content creation) face context pollution when all work happens in a single session. Architecture thinking leaks into implementation, review notes compete with active coding, and the context window fills with irrelevant information.

A single Claude Code session has a fixed context window. Mixing roles means every agent sees every other agent's work, leading to confused outputs and wasted context capacity.

## Decision

Use git worktrees to create isolated workstations, each bound to a specific agent role with its own branch, runtime environment, and CLAUDE.md instructions.

**Workstation structure:**

```
[project]/                    # main -- shared state, CI/CD, releases
[project]-[Dev1]/             # Developer workstation 1
[project]-[Dev2]/             # Developer workstation 2
[project]-[Reviewer]/         # Reviewer workstation
[project]-[Architect]/        # Architect workstation
```

**Branch strategy:**
- `main` -- integration branch, PRs only
- Workstation branches (e.g., `dev1`, `architect`) -- home branches for each agent
- Issue branches -- created from workstation branch, PR'd to `main`

**Shared state:**
- `.context/` -- shared knowledge (synced via merge from main)
- `.flow/state.json` -- cross-workstation coordination
- `.context/handover/<workstation>.md` -- session persistence per agent

**Isolated state:**
- `CLAUDE.md` -- per-branch, role-specific instructions (merge=ours in .gitattributes)
- Runtime environment -- separate ports, separate databases (if applicable)

**Port allocation (example for web projects):**

| Workstation | App Port | Debug Port | DB Port |
|-------------|----------|------------|---------|
| main | 3000 | 9229 | 5432 |
| dev1 | 3010 | 9230 | 5433 |
| dev2 | 3020 | 9231 | 5434 |
| reviewer | 3030 | 9232 | 5435 |
| architect | 3040 | 9233 | 5436 |

## Consequences

**Positive:**
- Clean context separation -- Architect doesn't pollute Developer's prompt
- Parallel work -- multiple agents can work simultaneously on different issues
- Role enforcement -- each agent stays in its lane via CLAUDE.md instructions
- Independent testing -- each workstation has its own runtime environment
- Persistent identity -- each workstation remembers its session state via handover files

**Negative:**
- Branch management overhead -- must keep workstation branches in sync with main
- Disk space -- N worktrees * full repo (though git shares objects)
- Coordination cost -- handover files and state must be maintained
- Setup complexity -- initial configuration of N workstations takes time

## Alternatives Considered

### Single Branch, Role Switching
Switch roles by changing CLAUDE.md content in a single worktree. Rejected because context window still gets polluted with previous role's artifacts, and there's no parallel work capability.

### Separate Repositories
Give each agent its own full repository clone. Rejected because it makes shared state (.context/, .flow/) much harder to synchronize, and git worktrees solve the isolation problem with less overhead.

### Docker-per-Agent
Run each agent in a separate container. Rejected as overkill for context isolation -- the problem is context window management, not process isolation. Docker adds unnecessary complexity.

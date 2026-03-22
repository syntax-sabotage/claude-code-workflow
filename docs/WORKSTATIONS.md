# Setting Up Named Workstations

A workstation is a persistent git worktree bound to a specific agent role. Each
workstation has its own branch, runtime environment, and CLAUDE.md instructions.

This guide covers setup from scratch.

---

## Prerequisites

- Git 2.15+ (worktree support)
- A project repository with at least one commit on `main`
- Claude Code installed

## 1. Plan Your Workstations

Decide how many workstations you need based on your team model:

| Team Size | Recommended Setup |
|-----------|-------------------|
| Solo + 1 agent | No workstations needed -- work directly on main |
| Solo + 2-3 agents | 2 workstations: 1 Developer + 1 Reviewer |
| Solo + 4-7 agents | Full team: Architect, 2 Developers, 2 Reviewers, Data Engineer, Content Engineer |

Pick short, memorable names for your workstations. Use a consistent naming theme
(characters, colors, planets -- whatever works for your team).

## 2. Create Workstation Branches

From your main worktree:

```bash
# Create branches for each workstation
git checkout -b dev1
git push -u origin dev1
git checkout main

git checkout -b dev2
git push -u origin dev2
git checkout main

git checkout -b reviewer
git push -u origin reviewer
git checkout main

git checkout -b architect
git push -u origin architect
git checkout main
```

## 3. Create Worktrees

Git worktrees share the same `.git` objects but have independent working
directories. Each worktree checks out a different branch.

```bash
# From the main worktree directory
cd /path/to/your-project

# Create worktrees (one per workstation)
git worktree add ../your-project-Dev1 dev1
git worktree add ../your-project-Dev2 dev2
git worktree add ../your-project-Reviewer reviewer
git worktree add ../your-project-Architect architect
```

This creates the following structure:

```
parent-directory/
├── your-project/              # main branch (shared state, CI/CD)
├── your-project-Dev1/         # dev1 branch (Developer 1)
├── your-project-Dev2/         # dev2 branch (Developer 2)
├── your-project-Reviewer/     # reviewer branch
└── your-project-Architect/    # architect branch
```

## 4. Set Up CLAUDE.md Per Workstation

Each workstation needs its own role-bound CLAUDE.md. Copy the workstation template
and customize:

```bash
# In each worktree
cp templates/CLAUDE.md.workstation your-project-Dev1/CLAUDE.md
cp templates/CLAUDE.md.workstation your-project-Dev2/CLAUDE.md
cp templates/CLAUDE.md.workstation your-project-Reviewer/CLAUDE.md
cp templates/CLAUDE.md.workstation your-project-Architect/CLAUDE.md
```

Edit each CLAUDE.md to set:
- Role binding (Developer, Reviewer, Architect, etc.)
- Workstation name
- Home branch name
- Port numbers (if applicable)
- Scope & boundaries for this specific role

## 5. Protect CLAUDE.md with .gitattributes

Without merge protection, merging `main` into a workstation branch would overwrite
the workstation's CLAUDE.md with main's version.

Add to `.gitattributes` in your project root (this goes on every branch):

```
CLAUDE.md merge=ours
```

Then configure the merge driver (once per clone):

```bash
git config merge.ours.driver true
```

This tells git: "On merge conflicts for CLAUDE.md, always keep the current
branch's version."

Commit `.gitattributes` on every branch:

```bash
# On main
cp templates/.gitattributes .gitattributes
git add .gitattributes
git commit -m "chore: add merge protection for CLAUDE.md"
git push

# On each workstation branch, merge main to get .gitattributes
cd ../your-project-Dev1
git merge main
cd ../your-project-Dev2
git merge main
# ... etc
```

## 6. Set Up Runtime Environments (Optional)

If your project needs separate runtime environments per workstation (e.g., web
servers, databases), allocate non-conflicting ports:

### Docker Compose (example)

Create a `docker-compose.override.yml` in each worktree:

```yaml
# your-project-Dev1/docker-compose.override.yml
services:
  app:
    ports:
      - "3010:3000"
  db:
    ports:
      - "5433:5432"
```

```yaml
# your-project-Dev2/docker-compose.override.yml
services:
  app:
    ports:
      - "3020:3000"
  db:
    ports:
      - "5434:5432"
```

### Port Allocation Table

Document your port assignments somewhere central (e.g., in substrate.md):

| Workstation | App | Debug | DB |
|-------------|-----|-------|-----|
| main | 3000 | 9229 | 5432 |
| Dev1 | 3010 | 9230 | 5433 |
| Dev2 | 3020 | 9231 | 5434 |
| Reviewer | 3030 | 9232 | 5435 |
| Architect | 3040 | 9233 | 5436 |

## 7. Set Up Handover Files

Create a handover file for each workstation:

```bash
mkdir -p .context/handover
cp templates/.context/handover/workstation.md .context/handover/dev1.md
cp templates/.context/handover/workstation.md .context/handover/dev2.md
cp templates/.context/handover/workstation.md .context/handover/reviewer.md
cp templates/.context/handover/workstation.md .context/handover/architect.md
```

These files live on `main` and are shared across all worktrees. Each agent
updates its own handover file at session end.

## 8. Install Hooks

Copy the hook scripts to `.claude/hooks/` in the main worktree. Since all
worktrees share the same `.git`, hooks only need to be set up once:

```bash
mkdir -p .claude/hooks
cp templates/.claude/hooks/*.py .claude/hooks/
cp templates/.claude/hooks/patterns.json .claude/hooks/
chmod +x .claude/hooks/*.py
```

## 9. Daily Workflow

### Starting a Session

Open a terminal in the workstation directory and launch Claude Code:

```bash
cd /path/to/your-project-Dev1
claude
# Agent runs /flow-resume, loads handover state
```

### Keeping Branches in Sync

Periodically merge `main` into workstation branches to pick up shared changes
(`.context/`, `.flow/`, etc.):

```bash
cd /path/to/your-project-Dev1
git fetch origin
git merge origin/main
```

The `.gitattributes` merge strategy ensures CLAUDE.md stays branch-specific.

### Ending a Session

The agent runs `/flow-handover` to save state, then you close the terminal.

## Troubleshooting

### "fatal: branch is already checked out"

A branch can only be checked out by one worktree at a time. If you see this
error, another worktree already has that branch. Check with:

```bash
git worktree list
```

### Disk Space

Worktrees share git objects, so the overhead is mainly the working directory
files. For a typical project, each worktree adds 10-100 MB.

### Removing a Workstation

```bash
# Remove the worktree
git worktree remove ../your-project-Dev2

# Optionally delete the branch
git branch -d dev2
git push origin --delete dev2
```

---
description: FLOW Simplify - Run code simplification on a module or path
---

**MODEL:** sonnet (coordination + agents)
**EXECUTION:** team, background
## Usage

```
/flow-simplify <module_or_path>
```

**Examples:**
- `/flow-simplify src/auth` -- simplify a directory
- `/flow-simplify src/auth/middleware.py` -- simplify a single file

## Steps

### 1. Resolve target path

If a bare directory name is given, resolve to `<name>/`.
If a relative path is given, use as-is from repo root.

### 2. Glob the target to plan the split

```bash
# Adjust glob pattern for your project's file types
find <target_path> -type f \( -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "*.go" -o -name "*.rs" \) | sort
```

Split files into groups for parallel agents. Standard split for a full directory:
- **core**: main entry points, core logic files
- **supporting**: helper/utility files, secondary modules
- **config-tests**: configuration, tests, static assets

Merge groups if the target is small (< 5 source files -- single agent is fine).

### 3. Spawn agents in background

For each group, spawn an agent with `run_in_background: true`:

```
Review and simplify the code in these files:
<file list>

Constraints:
- Follow the project's existing coding standards (read .context/ai-rules.md if it exists)
- No new docstrings or comments unless logic is non-obvious
- Remove dead code, redundant comments, and over-engineered abstractions
- Preserve all business logic exactly
- Fix any correctness bugs (shared mutable state, race conditions, etc.)
- Maintain consistent formatting with the rest of the codebase

When done, report every file changed (and what changed)
plus every file that was already clean.
```

Inform the user the agents are running in background and they can continue working.

### 4. Collect results as agents report in

When each agent completes, accumulate results. Once all agents have reported, proceed to step 5.

### 5. Run quality checks

```bash
# Run project-specific linters/formatters (adjust to your project)
# Examples:
# Python: black --check <target>/ && ruff check <target>/
# JavaScript: eslint <target>/ && prettier --check <target>/
# Go: gofmt -l <target>/ && golangci-lint run <target>/
```

Fix any issues before proceeding.

### 6. Commit

Stage only the modified files and commit:
```bash
git diff --name-only
git add <changed files>
git commit -m "refactor(<scope>): simplification pass

<bullet summary of changes>

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### 7. Report

Summarise:
- Files changed and what was simplified
- Any correctness bugs found and fixed
- Files that were already clean

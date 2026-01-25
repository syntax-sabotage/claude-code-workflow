# Global CLAUDE.md Template

Add this content to `~/.claude/CLAUDE.md`:

---

## Communication Style

<!-- Customize to your preferences -->
Be direct and straightforward. No cheerleading phrases.
Tell me when my ideas are flawed or incomplete.
Focus on practical problems and realistic solutions.

## .context Project Knowledge System

When working in any project directory, check for a `.context/` folder. If present, this contains structured project knowledge you MUST use.

### On Session Start

1. Read `.context/substrate.md` first - it's the navigation hub
2. For coding tasks, read `.context/ai-rules.md` before writing any code
3. Check `.context/anti-patterns.md` to avoid known pitfalls

### When Writing Code

**Always consult these before generating code:**
- `.context/ai-rules.md` - Coding standards, naming conventions, architecture rules
- `.context/glossary.md` - Project-specific terminology and domain language
- `.context/anti-patterns.md` - Patterns to avoid with explanations

### Key Principle

The .context folder contains institutional knowledge about WHY decisions were made, not just WHAT exists. Prefer patterns documented there over generic best practices. If you encounter a conflict between your training and .context docs, follow .context.

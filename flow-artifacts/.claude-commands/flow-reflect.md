# /flow-reflect <stream> - Capture Learnings

Synthesize tactical learnings from closed issues into strategic knowledge.

## Arguments
- `stream` - Milestone name to reflect on

## Steps

1. **Find Unreflected Closed Issues**
```bash
gh issue list --state closed --milestone "<stream>" --json number,title,body,comments,labels | \
  jq '[.[] | select(.labels | map(.name) | contains(["reflected"]) | not)]'
```

2. **Extract Learnings from Each Issue**
   - Read closing comments for "## Learnings" section
   - Note patterns that emerged
   - Identify what worked well
   - Flag what caused problems

3. **Synthesize Patterns**
   - Group similar learnings
   - Identify recurring themes
   - Extract actionable rules

4. **Update .context/ Files**

### For New Rules
Add to `.context/ai-rules.md`:
```markdown
### New Rule from #47, #52
<description>
```

### For Anti-Patterns
Add to `.context/anti-patterns.md`:
```markdown
### <Pattern Name>
**Discovered in:** #47
**Problem:** ...
**Solution:** ...
```

### For Terminology
Add to `.context/glossary.md`:
```markdown
| **Term** | Definition learned from implementation |
```

5. **Create/Update Stream Learnings**
```
.context/learnings/<stream-slug>.md
```

```markdown
# Learnings - <Stream Name>

## Rollup <date>
Synthesized from: #47, #52, #55

### Patterns Discovered
- ...

### Rules Added
- Added to ai-rules.md: <rule description>

### Anti-Patterns Identified
- Added to anti-patterns.md: <pattern name>

### Process Improvements
- ...
```

6. **Mark Issues as Reflected**
```bash
gh issue edit 47 --add-label "reflected"
gh issue edit 52 --add-label "reflected"
```

7. **Commit Changes**
```bash
git add .context/
git commit -m "chore: reflect on <stream> learnings (#47, #52)"
```

## Output Format

```
## Reflection Complete - Invoice Pro

### Issues Processed
- #47 Add date validation
- #52 PDF export feature
- #55 Performance optimization

### Knowledge Captured

#### Rules Added (ai-rules.md)
- Always validate dates against fiscal periods
- Use streaming for large PDF generation

#### Anti-Patterns (anti-patterns.md)
- Loading full invoice history in memory

#### Glossary (glossary.md)
- "Fiscal Period" - accounting term added

### Stream Learnings
Created: .context/learnings/invoice-pro.md

### Issues Marked Reflected
- #47 ✓
- #52 ✓
- #55 ✓

Committed: "chore: reflect on Invoice Pro learnings"
```

## When to Run

- After `/flow-ship` suggests reflection (3+ unreflected)
- End of major milestone
- When patterns are becoming clear
- Before starting new stream

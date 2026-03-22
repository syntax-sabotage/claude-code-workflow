# Anti-Patterns -- What NOT to Do

Patterns that have caused problems. Learn from past mistakes.

---

## Hardcoded Credentials

**Problem**: Secrets in source code get committed to version control.

```python
# WRONG -- credentials in code
API_KEY = "sk-abc123secret"
db_password = "hunter2"

# CORRECT -- environment variables
API_KEY = os.environ["API_KEY"]
db_password = os.environ["DATABASE_PASSWORD"]
```

**Why it matters**: Once a secret is in git history, it's compromised. Rotating credentials is expensive and easy to forget.

**Detection**: `pre-edit-guard.py` pattern PY003 catches hardcoded passwords.

---

## Bare External Imports Without Error Handling

**Problem**: External dependencies fail at runtime with cryptic errors.

```python
# WRONG -- bare import, crashes if not installed
from special_library import magic_function

# CORRECT -- graceful degradation
try:
    from special_library import magic_function
    HAS_SPECIAL_LIBRARY = True
except ImportError:
    HAS_SPECIAL_LIBRARY = False
    magic_function = None
```

```javascript
// WRONG -- unhandled external call
const data = await fetch(EXTERNAL_API_URL);
const json = await data.json();

// CORRECT -- handle failures
try {
    const data = await fetch(EXTERNAL_API_URL);
    if (!data.ok) throw new Error(`API returned ${data.status}`);
    const json = await data.json();
} catch (error) {
    logger.error({ error }, 'External API call failed');
    throw new AppError({ code: 'EXTERNAL_SERVICE_UNAVAILABLE' });
}
```

**Why it matters**: External dependencies are the most common source of production incidents. Always handle their absence or failure.

---

## Reinventing Framework Patterns

**Problem**: Writing custom implementations for things the framework already provides.

```python
# WRONG -- custom date formatting
def format_date(dt):
    return f"{dt.year}-{dt.month:02d}-{dt.day:02d}"

# CORRECT -- use the framework/stdlib
formatted = dt.strftime("%Y-%m-%d")
# Or: dt.isoformat() for ISO 8601
```

```javascript
// WRONG -- custom deep clone
function deepClone(obj) {
    return JSON.parse(JSON.stringify(obj));
}

// CORRECT -- use structuredClone (available since Node 17, all modern browsers)
const clone = structuredClone(obj);
```

**Why it matters**: Custom implementations have bugs the framework has already fixed. They also confuse other developers who expect standard patterns.

---

## Missing Tenant/Scope Filter on Queries

**Problem**: Data leaks between users, organizations, or tenants.

```sql
-- WRONG -- no scope filter
SELECT * FROM documents WHERE id = $1;

-- CORRECT -- always scope to the current tenant/user
SELECT * FROM documents WHERE id = $1 AND organization_id = $2;
```

**Why it matters**: A single missing filter is a data breach. This is the most common security vulnerability in multi-tenant applications.

---

## Historical Bugs

Track bugs that made it to production so the team learns from them.

| Date | Bug | Root Cause | Fix |
|------|-----|------------|-----|
| <!-- YYYY-MM-DD --> | <!-- What happened --> | <!-- Why --> | <!-- How fixed --> |

---

## Summary Table

| Anti-Pattern | Risk Level | Detection |
|--------------|------------|-----------|
| Hardcoded credentials | Critical | pre-edit-guard, code review |
| Bare external imports | High | Code review, integration tests |
| Reinventing framework | Medium | Code review |
| Missing scope filter | Critical | Code review, integration tests |

## Related Documentation

- [ai-rules.md](./ai-rules.md) -- Coding constraints
- [substrate.md](./substrate.md) -- Navigation hub

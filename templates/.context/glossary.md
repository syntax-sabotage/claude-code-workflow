# Glossary -- Domain Terminology

Project-specific terms. Use consistently in code, docs, and communication.

> **How to fill this out:** Add terms specific to your project's domain.
> Focus on terms that Claude might misinterpret or use inconsistently.
> Include the database column/table name and code variable name for each entity
> so Claude generates consistent code.

## Core Entities

### [Entity Name]
[What this entity represents in your domain.]
- **Database**: `[table_name]` table
- **Code**: `[TypeName]`, `[idField]`
- **Relationships**: [belongs to X, has many Y]

### [Entity Name]
[Description]
- **Database**: `[table_name]` table
- **Code**: `[TypeName]`, `[idField]`

## Business Logic Terms

### [Term]
[Definition. When and how it's used in the business domain.]
- **Code**: `[variable or type name]`
- **Example**: [Concrete example of usage]

## Technical Terms

### [Internal Concept]
[Definition of an internal technical concept that is project-specific.]

```
// Example usage in code
[code snippet showing how this concept appears]
```

## Statuses / States

### [Entity] Lifecycle
| Status | Meaning | Transitions To |
|--------|---------|----------------|
| `draft` | [Initial state] | `active` |
| `active` | [In use] | `archived`, `suspended` |
| `archived` | [No longer active] | -- |

## Abbreviations

| Abbreviation | Meaning |
|--------------|---------|
| [ABC] | [Full name and context] |

## Related Documentation

- [substrate.md](./substrate.md) -- Navigation hub
- [ai-rules.md](./ai-rules.md) -- Coding constraints using these terms

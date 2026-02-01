# Glossary - Domain Terminology

Project-specific terms. Use consistently in code, docs, and communication.

> **How to fill this out:** Add terms that are specific to your project's domain.
> Focus on terms that Claude might misinterpret or use inconsistently.
> Include the database column/table name and code variable name for each entity
> so Claude generates consistent code. Remove placeholder sections you don't need.

## Core Entities

### User
<!-- Description of User in your domain -->
- **Database**: `users` table
- **Code**: `User`, `userId`

### Organization (if multi-tenant)
<!-- Description -->
- **Database**: `organizations` table
- **Code**: `Organization`, `organizationId`

### <!-- Your Entity -->
<!-- Description -->
- **Database**: `<!-- table_name -->` table
- **Code**: `<!-- TypeName -->`, `<!-- idField -->`

## Business Logic Terms

### <!-- Term -->
<!-- Definition. When/how it's used. -->
- **Database**: `<!-- column or table -->`
- **Code**: `<!-- variable or type -->`

## Technical Terms

### <!-- Term (e.g., tenantContext) -->
<!-- Definition of internal technical concept -->

```typescript
// Example usage
interface ExampleContext {
  // ...
}
```

## Statuses / States

### <!-- Entity --> Status
| Status | Meaning |
|--------|---------|
| `active` | <!-- Description --> |
| `inactive` | <!-- Description --> |
| `...` | |

## Abbreviations

| Abbreviation | Meaning |
|--------------|---------|
| <!-- ABC --> | <!-- Full name --> |

## Related Documentation

- [substrate.md](./substrate.md) - Navigation hub
- [database/schema.md](./database/schema.md) - Table definitions
- [api/endpoints.md](./api/endpoints.md) - API using these terms

# AI Rules - Hard Constraints

These rules are **non-negotiable**. Follow them exactly when generating code.

## TypeScript Standards

<!-- Customize for your language/framework -->

### Strict Mode Required
```typescript
// tsconfig.json enforces strict: true
// NEVER use @ts-ignore, @ts-expect-error, or any type
// All function parameters and returns must be typed
```

### Import Patterns
```typescript
// CORRECT: Use workspace aliases (if monorepo)
import { db } from '@myproject/database';

// WRONG: Relative imports across packages
import { db } from '../../../packages/database/src';
```

### Validation Required
```typescript
// ALL external input must be validated
// Use Zod, Joi, or equivalent

// CORRECT
export const createItem = procedure
  .input(createItemSchema)
  .mutation(async ({ input }) => { ... });

// WRONG: Trusting input without validation
export const createItem = procedure
  .mutation(async ({ input }) => { ... }); // NO!
```

## Database Rules

### Use Query Builder / ORM
```typescript
// CORRECT: Type-safe queries
const items = await db
  .select()
  .from(itemsTable)
  .where(eq(itemsTable.userId, userId));

// WRONG: Raw SQL with string interpolation
const items = await db.execute(`SELECT * FROM items WHERE user_id = '${userId}'`);
```

### Tenant Isolation (if multi-tenant)
```typescript
// EVERY query on tenant data MUST include tenant filter

// CORRECT
.where(
  and(
    eq(table.organizationId, ctx.organizationId),
    eq(table.id, input.id)
  )
)

// WRONG: Missing tenant filter = data leak
.where(eq(table.id, input.id))
```

## Error Handling

```typescript
// Use specific error codes
throw new AppError({
  code: 'NOT_FOUND',
  message: 'Item not found',
});

// NEVER expose internal errors to clients
// NEVER include stack traces in production responses
```

## Naming Conventions

### Files
| Type | Convention | Example |
|------|------------|---------|
| React components | PascalCase | `ItemForm.tsx` |
| Utilities | kebab-case | `date-utils.ts` |
| Routes/handlers | camelCase | `items.ts` |

### Database
| Type | Convention | Example |
|------|------------|---------|
| Tables | snake_case plural | `user_items` |
| Columns | snake_case | `created_at` |
| Foreign keys | singular_id | `user_id` |

### TypeScript
| Type | Convention | Example |
|------|------------|---------|
| Types/Interfaces | PascalCase | `CreateItemInput` |
| Functions | camelCase | `createItem` |
| Constants | SCREAMING_SNAKE | `MAX_FILE_SIZE` |

## Security Non-Negotiables

1. **Never log sensitive data**: passwords, tokens, PII
2. **Never expose internal errors**: use generic messages in production
3. **Always validate file uploads**: check MIME type AND content
4. **Always use parameterized queries**: never string concatenation
5. **Never trust client-side validation alone**: always validate server-side

## Performance Rules

1. **Paginate list queries**: default limit, max limit
2. **Use database indexes**: for foreign keys and frequently queried columns
3. **Lazy load heavy components**: where applicable

## Testing Requirements

### Test File Location
```
// Co-locate tests with source
src/
  items.ts
  items.test.ts
```

### Test Structure
```typescript
describe('items', () => {
  describe('create', () => {
    it('creates an item with valid input', async () => {
      // Arrange, Act, Assert
    });
    it('rejects invalid input', async () => { ... });
  });
});
```

## Related Documentation

- [substrate.md](./substrate.md) - Navigation hub
- [anti-patterns.md](./anti-patterns.md) - What NOT to do
- [glossary.md](./glossary.md) - Domain terminology

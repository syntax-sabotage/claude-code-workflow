# Anti-Patterns - What NOT to Do

Patterns that have caused problems. Avoid these.

## Database Anti-Patterns

### Missing Tenant Filter (if multi-tenant)

**Problem**: Data leak across tenants.

```typescript
// WRONG - Data leak vulnerability
const items = await db
  .select()
  .from(itemsTable)
  .where(eq(itemsTable.id, itemId));

// CORRECT - Always include tenant filter
const items = await db
  .select()
  .from(itemsTable)
  .where(
    and(
      eq(itemsTable.organizationId, ctx.organizationId),
      eq(itemsTable.id, itemId)
    )
  );
```

**Why it matters**: One missing filter = data breach.

---

### N+1 Query Pattern

**Problem**: Fetching related data in a loop.

```typescript
// WRONG - N+1 queries
const items = await db.select().from(itemsTable);
for (const item of items) {
  item.children = await db.select().from(childTable).where(...);
}

// CORRECT - Single query with join
const itemsWithChildren = await db
  .select()
  .from(itemsTable)
  .leftJoin(childTable, eq(itemsTable.id, childTable.itemId));
```

---

### Raw SQL String Interpolation

**Problem**: SQL injection.

```typescript
// WRONG - SQL injection
const result = await db.execute(
  `SELECT * FROM items WHERE name = '${userInput}'`
);

// CORRECT - Parameterized via ORM
const result = await db
  .select()
  .from(itemsTable)
  .where(eq(itemsTable.name, userInput));
```

---

## API Anti-Patterns

### Exposing Internal Errors

**Problem**: Stack traces leak implementation details.

```typescript
// WRONG
catch (error) {
  throw new Error(error.message); // SQL errors, paths, etc.
}

// CORRECT
catch (error) {
  logger.error({ error }, 'Operation failed');
  throw new AppError({
    code: 'INTERNAL_ERROR',
    message: 'Operation failed. Please try again.',
  });
}
```

---

### Unbounded List Queries

**Problem**: Memory exhaustion, slow responses.

```typescript
// WRONG - No limit
const items = await db.select().from(itemsTable);

// CORRECT - Always paginate
const items = await db
  .select()
  .from(itemsTable)
  .limit(input.limit ?? 50)
  .offset(input.offset ?? 0);
```

---

### Missing Input Validation

**Problem**: Invalid data corrupts database.

```typescript
// WRONG - Trusting input
export const updateItem = procedure
  .mutation(async ({ input }) => {
    await db.update(itemsTable).set(input).where(...);
  });

// CORRECT - Validate everything
export const updateItem = procedure
  .input(updateItemSchema)
  .mutation(async ({ input }) => {
    await db.update(itemsTable).set(input).where(...);
  });
```

---

## Frontend Anti-Patterns

### Missing Loading States

**Problem**: Users don't know if action worked.

```tsx
// WRONG - No feedback
<Button onClick={() => mutation.mutate(data)}>Save</Button>

// CORRECT - Loading and error states
<Button
  disabled={mutation.isPending}
  onClick={() => mutation.mutate(data)}
>
  {mutation.isPending ? 'Saving...' : 'Save'}
</Button>
```

---

### Stale Cache After Mutations

**Problem**: UI shows outdated data.

```typescript
// WRONG - Mutation without invalidation
const mutation = useMutation({ mutationFn: createItem });

// CORRECT - Invalidate related queries
const mutation = useMutation({
  mutationFn: createItem,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['items'] });
  },
});
```

---

## File Upload Anti-Patterns

### Trusting File Extension

**Problem**: Malicious files can be renamed.

```typescript
// WRONG - Trust extension
if (file.name.endsWith('.jpg')) { ... }

// CORRECT - Check MIME type AND magic bytes
const type = await fileTypeFromBuffer(buffer);
if (!ALLOWED_TYPES.includes(type?.mime)) {
  throw new Error('Invalid file type');
}
```

---

## Historical Bugs

Document bugs that made it to production:

| Date | Bug | Root Cause | Fix |
|------|-----|------------|-----|
| <!-- Date --> | <!-- What happened --> | <!-- Why --> | <!-- How fixed --> |

---

## Summary Table

| Anti-Pattern | Risk Level | Detection |
|--------------|------------|-----------|
| Missing tenant filter | Critical | Code review |
| SQL injection | Critical | Static analysis |
| Exposed internal errors | High | Log monitoring |
| Unbounded queries | High | Performance testing |
| Missing loading states | Medium | UX review |
| Stale cache | Medium | Integration testing |

## Related Documentation

- [ai-rules.md](./ai-rules.md) - Coding constraints
- [substrate.md](./substrate.md) - Navigation hub

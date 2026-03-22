# AI Rules -- Hard Constraints

These rules are **non-negotiable**. Follow them exactly when generating code.

## [YOUR_FRAMEWORK] Version Compliance

<!-- Replace with your framework's version-specific rules -->

- Target version: [YOUR_FRAMEWORK] [VERSION]
- Deprecated APIs to avoid: [LIST]
- Required patterns: [LIST]

## Language Rules

<!-- Define what language is used where -->

| Context | Language |
|---------|----------|
| User-facing content | [YOUR_UI_LANGUAGE] |
| Code, comments, docs | [English recommended] |
| Commit messages | [English recommended] |
| Variable/function names | [English recommended] |

## Naming Conventions

### Files
| Type | Convention | Example |
|------|------------|---------|
| [Components/Views] | [PascalCase/kebab-case] | `[Example.tsx]` |
| [Utilities/Helpers] | [kebab-case/snake_case] | `[date-utils.ts]` |
| [Tests] | [Convention] | `[example.test.ts]` |

### Code
| Type | Convention | Example |
|------|------------|---------|
| [Classes/Types] | [PascalCase] | `[UserProfile]` |
| [Functions/Methods] | [camelCase/snake_case] | `[createUser]` |
| [Constants] | [SCREAMING_SNAKE] | `[MAX_RETRIES]` |
| [Database tables] | [snake_case plural] | `[user_profiles]` |
| [Database columns] | [snake_case] | `[created_at]` |

## Module Architecture

<!-- How modules/packages should be structured -->

```
[YOUR_MODULE]/
├── [models/src/lib]       # Business logic
├── [views/components]     # Presentation
├── [tests/spec/__tests__] # Tests
├── [config]               # Configuration
└── [README.md]            # Module documentation
```

### Rules
- [Rule 1: e.g., "Every module must have a README"]
- [Rule 2: e.g., "No circular dependencies between modules"]
- [Rule 3: e.g., "Shared code goes in the core/common module"]

## Security

1. **Never hardcode credentials** -- use environment variables or secrets manager
2. **Never log sensitive data** -- passwords, tokens, PII
3. **Never expose internal errors** -- use generic messages in production
4. **Always validate external input** -- server-side validation is mandatory
5. **Always use parameterized queries** -- never string concatenation for SQL
6. **Copy-sensitive fields** -- tokens, UUIDs, credentials must have `copy=False` (or equivalent immutability)

## Testing Requirements

### Every new module/feature must include:
- [ ] Unit tests for business logic
- [ ] Integration tests for API endpoints
- [ ] Edge case coverage (empty input, max values, invalid data)

### Test structure:
```
# [YOUR_FRAMEWORK test pattern]
# Arrange -> Act -> Assert
```

## Commit Messages

Format: `type(scope): description`

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`

Examples:
```
feat(auth): add OAuth2 provider support
fix(api): handle null response from external service
refactor(database): extract query builder utility
```

## Quality Gates

- [ ] All tests pass
- [ ] No new warnings or errors
- [ ] No TODO/FIXME added without a linked issue
- [ ] Security rules checked
- [ ] Code follows naming conventions

## Related Documentation

- [substrate.md](./substrate.md) -- Navigation hub
- [anti-patterns.md](./anti-patterns.md) -- What NOT to do
- [glossary.md](./glossary.md) -- Domain terminology

# Domain-Specific Command Examples

Real-world slash commands from production projects.

## What's Here

| Command | Purpose | Domain |
|---------|---------|--------|
| `odoo-spec.md` | Interview-based requirements capture | Odoo development |
| `odoo-validate.md` | Module validation before deployment | Odoo development |
| `vps-upgrade.md` | Upgrade module on VPS | DevOps/deployment |

## How to Adapt for Your Domain

These examples show patterns you can copy for your own projects:

### Pattern 1: Requirements Interview (`odoo-spec.md`)

**What it does:**
- Interactive interview to capture requirements
- Creates `.context/specs/<name>.md`
- Optionally creates GitHub milestone + epic issue
- Feeds into FLOW workflow

**Adapt for:**
- **Mobile app:** `/mobile-spec` - Platform selection, screen flows, offline support
- **API design:** `/api-spec` - Endpoint design, auth, rate limiting
- **Data pipeline:** `/pipeline-spec` - Sources, transforms, destinations
- **Infrastructure:** `/infra-spec` - Services, scaling, disaster recovery

**Key sections to customize:**
1. **Interview questions** - Change to your domain
2. **Spec template** - Update sections for your needs
3. **Validation** - Check domain-specific requirements

### Pattern 2: Validation Command (`odoo-validate.md`)

**What it does:**
- Checks module structure (files, manifest, security)
- Runs static analysis
- Verifies dependencies
- Reports issues before deployment

**Adapt for:**
- **npm package:** `/npm-validate` - Check package.json, types, exports
- **Docker image:** `/docker-validate` - Scan for vulnerabilities, check layers
- **Infrastructure:** `/terraform-validate` - Check syntax, plan, cost estimate
- **Mobile:** `/app-validate` - Check bundle size, permissions, signing

**Key sections to customize:**
1. **Structure checks** - What files/dirs must exist
2. **Static analysis** - Linters, type checkers for your stack
3. **Dependencies** - How to verify deps are available
4. **Pre-deployment checks** - Domain-specific validations

### Pattern 3: Deployment Command (`vps-upgrade.md`)

**What it does:**
- SSH to VPS
- Pull latest code
- Upgrade specific module
- Restart services
- Verify deployment

**Adapt for:**
- **Kubernetes:** `/k8s-deploy` - Apply manifests, rollout status, health check
- **Serverless:** `/lambda-deploy` - Package, upload, update function
- **Static site:** `/deploy-site` - Build, sync to CDN, invalidate cache
- **Database:** `/db-migrate` - Backup, apply migrations, verify

**Key sections to customize:**
1. **Connection** - How to reach your deployment target
2. **Pre-deploy checks** - Safety validations
3. **Deployment steps** - Your deploy process
4. **Verification** - How to confirm success
5. **Rollback** - How to undo if needed

## Creating Your Own Commands

### 1. Identify Repeated Tasks

Look for tasks you do manually that could be automated:
- "I always forget to check X before deploying"
- "Setting up Y requires 10 steps in a specific order"
- "I need to gather requirements for Z type of feature"

### 2. Create the Command File

```bash
touch .claude/commands/your-command.md
```

### 3. Use This Template

```markdown
# /your-command

> One-line description of what this does

## Purpose

Explain the problem this solves and when to use it.

## Usage

\`\`\`bash
/your-command [args]
\`\`\`

## What This Command Does

1. **Step 1** - What happens first
2. **Step 2** - Next action
3. **Step 3** - Final step

## Example

\`\`\`bash
/your-command --option value
\`\`\`

Expected output:
\`\`\`
Success! Your thing was done.
\`\`\`

## Notes

- Important gotcha 1
- Important gotcha 2

## See Also

- `.context/related-doc.md`
- `/related-command`
\`\`\`

### 4. Test It

```bash
/your-command
```

Claude will read the command file and execute the instructions.

### 5. Refine Based on Usage

After using it a few times:
- Add edge cases you discovered
- Clarify ambiguous steps
- Add examples of common failures

## Command Categories

### Project Setup

Commands for initializing new projects/features:
- `/init-feature <name>` - Scaffold feature structure
- `/setup-env` - Configure local development
- `/create-service <name>` - Generate microservice boilerplate

### Validation

Commands to check before committing/deploying:
- `/<stack>-validate` - Pre-commit checks
- `/security-scan` - Check for vulnerabilities
- `/performance-check` - Benchmark critical paths

### Deployment

Commands for shipping code:
- `/deploy-<env>` - Deploy to environment
- `/rollback` - Undo last deployment
- `/health-check` - Verify deployment succeeded

### Requirements

Commands for capturing requirements:
- `/<domain>-spec` - Interview-based spec creation
- `/user-story` - Capture user story in standard format
- `/api-contract` - Define API before implementation

### Maintenance

Commands for ongoing work:
- `/update-deps` - Safely update dependencies
- `/cleanup-<thing>` - Remove obsolete code/data
- `/generate-changelog` - Create release notes

## Integration with FLOW

Domain commands often feed FLOW:

```bash
# Capture requirements
/your-spec "Feature name"
# → Creates .context/specs/feature-name.md
# → Creates GitHub milestone (stream)
# → Creates epic issue

# Break down into work
/flow-objective "Implement API endpoint"
/flow-objective "Add frontend UI"

# Start work
/flow-start 42

# Validate before shipping
/your-validate

# Deploy
/your-deploy production

# Complete
/flow-ship
```

## Examples by Domain

### Web Development

```bash
/api-spec         # Design API contract
/component-spec   # Plan React component
/lighthouse       # Run performance audit
/deploy-vercel    # Deploy to Vercel
```

### Mobile Development

```bash
/screen-spec      # Design mobile screen
/ios-validate     # Check iOS bundle
/android-validate # Check Android bundle
/testflight       # Deploy to TestFlight
```

### Data Engineering

```bash
/pipeline-spec    # Design data pipeline
/sql-validate     # Check SQL syntax and performance
/dag-validate     # Validate Airflow DAG
/deploy-airflow   # Deploy DAG to Airflow
```

### Infrastructure

```bash
/infra-spec       # Design infrastructure
/terraform-validate # Check Terraform
/cost-estimate    # Estimate cloud costs
/apply-terraform  # Apply infrastructure changes
```

### Machine Learning

```bash
/model-spec       # Define model requirements
/train-model      # Start training run
/eval-model       # Evaluate model performance
/deploy-model     # Deploy to serving endpoint
```

## Tips

### Keep Commands Focused

One command = one clear purpose.

**Good:**
- `/deploy-production` - Deploy to production
- `/deploy-staging` - Deploy to staging

**Bad:**
- `/deploy [env]` - Too generic, easy to deploy to wrong env

### Make Them Discoverable

Use clear names:
- `/<domain>-<action>` format
- Match user's mental model
- Use verbs for actions

### Add Safety Rails

For destructive operations:
```markdown
## Safety Checks

Before executing, verify:
1. [ ] Current branch is `main`
2. [ ] All tests pass
3. [ ] No uncommitted changes
4. [ ] User confirms with "yes"
```

### Document Edge Cases

```markdown
## Common Issues

### Issue: X fails with error Y

**Cause:** Z is not configured

**Fix:**
\`\`\`bash
Do this thing
\`\`\`
```

## Testing Your Commands

1. **Happy path** - Does it work as expected?
2. **Edge cases** - What if args are missing?
3. **Failures** - Does it fail gracefully?
4. **Idempotency** - Can I run it twice safely?
5. **Documentation** - Is the output clear?

## When to Create a Command vs Script

| Create Slash Command | Create Bash Script |
|---------------------|-------------------|
| Involves AI decision-making | Fully deterministic |
| Requires code reading/analysis | Just shell commands |
| Needs user interaction | Fully automated |
| Changes based on context | Always same steps |

**Example:**
- `/deploy-production` (command) - Needs to verify code, run tests, check env
- `deploy.sh production` (script) - Just executes deployment steps

Commands can **call** scripts:
```markdown
# /deploy-production

1. Read `.context/vps-deployment.md` to understand deployment process
2. Verify all tests pass
3. Check no one else is deploying (check GitHub Actions)
4. Execute `./scripts/deploy.sh production`
5. Monitor deployment, report status
```

---

Adapt these examples to your domain. Focus on automating **repetitive, error-prone tasks** that benefit from AI assistance.

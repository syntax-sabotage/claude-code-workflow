# /flow-health - System Health Check

Check development and production environment health.

## Steps

1. **Check Git Status**
```bash
git status
git log --oneline -5
```

2. **Check GitHub Connectivity**
```bash
gh auth status
gh repo view --json name,url
```

3. **Check Development Environment**

Adapt to your project's stack:
```bash
# Example: Docker-based project
# docker ps | grep <service-name>
# docker logs <container> --tail=20

# Example: Local dev server
# curl -s http://localhost:3000/health

# Example: Database check
# psql $DATABASE_URL -c "SELECT 1"
```

4. **Check Production (If Applicable)**
```bash
# Example: SSH to production
# ssh $PROD_HOST "systemctl status $SERVICE && tail -20 /var/log/$SERVICE/$SERVICE.log"
```

5. **Check .context/ Freshness**
```bash
git log -1 --format="%ar" -- .context/
```

## Output Format

```
## System Health Check

### Git
- Branch: main
- Clean: Yes
- Last commit: 2 hours ago

### GitHub
- Auth: OK
- Repo: org/project

### Development Environment
- Status: Running
- Last log: [normal operation]

### Production
- Service: active
- Uptime: 15 days

### .context/ Freshness
- Last updated: 1 day ago
- Consider reflection if stale

### FLOW Status
- Active issues: 2
- Blocked: 0
- Pool: 3

### Overall: HEALTHY
```

## When to Run

- Start of session (after /flow-resume)
- Before deploying to production
- When things seem broken
- After major changes

## Customization

Replace the placeholder commands above with your project-specific checks.
For a concrete example, see `templates/.claude-commands-examples/vps-upgrade.md`.

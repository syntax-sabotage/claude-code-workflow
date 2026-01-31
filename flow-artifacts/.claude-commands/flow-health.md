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

3. **Check Docker Environment**
```bash
docker ps | grep odoo
docker logs odoo19-dev --tail=20
```

4. **Check Production (VPS)**
```bash
ssh root@185.163.117.155 "systemctl status odoo && tail -20 /var/log/odoo/odoo.log"
```

5. **Verify Sync State**
```bash
# Compare local and Docker
diff -rq addons/invoice_pro/ /Users/larsweiler/Dev-Odoo19/docker/odoo/addons/invoice_pro/ \
  --exclude='__pycache__' --exclude='*.pyc'
```

6. **Check .context/ Freshness**
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
- Repo: lweiler-lab/it-beratung

### Docker Dev Environment
- Container: odoo19-dev (running)
- Uptime: 3 days
- Last log: "INFO odoo.modules.loading: Modules loaded"

### Production (VPS)
- Service: odoo (active)
- Uptime: 15 days
- Last log: [normal operation]

### Sync Status
- Local <-> Docker: IN SYNC
- Local <-> Prod: [check manually before deploy]

### .context/ Freshness
- Last updated: 1 day ago
- Consider reflection if stale

### FLOW Status
- Active issues: 2
- Blocked: 0
- Pool: 3

### Overall: HEALTHY ✓
```

## Quick Fixes

### Docker Not Running
```bash
cd /Users/larsweiler/Dev-Odoo19/docker
docker-compose up -d odoo19
```

### Out of Sync
```bash
rsync -av --exclude='__pycache__' --exclude='*.pyc' --exclude='.git' --delete \
  addons/invoice_pro/ \
  /Users/larsweiler/Dev-Odoo19/docker/odoo/addons/invoice_pro/
docker-compose restart odoo19
```

### Production Issues
```bash
ssh root@185.163.117.155
systemctl restart odoo
tail -f /var/log/odoo/odoo.log
```

## When to Run

- Start of session (after /flow-resume)
- Before deploying to production
- When things seem broken
- After major changes

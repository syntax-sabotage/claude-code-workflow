# /vps-upgrade - Upgrade Module on VPS

Quick command to upgrade a module on the production VPS.

## Usage

```
/vps-upgrade <module_name>
```

## Instructions

1. **Read** `.context/vps-deployment.md` if you need full context.

2. **Execute the upgrade**:
```bash
source /Volumes/External/Development/odoo-projects/customer-deployments/it-beratung/.env && \
ssh $VPS_SSH_ALIAS "sudo systemctl stop odoo19 && \
  sudo -u odoo19 /opt/odoo19/venv/bin/python /opt/odoo19/odoo/odoo-bin \
    -c /etc/odoo19.conf \
    -d odoo_itberatung \
    -u <MODULE_NAME> \
    --stop-after-init && \
  sudo systemctl start odoo19"
```

3. **Verify**:
```bash
source .env && ssh $VPS_SSH_ALIAS "systemctl status odoo19 | head -10"
source .env && ssh $VPS_SSH_ALIAS "tail -30 /var/log/odoo/odoo19.log | grep -E '(ERROR|CRITICAL|Modules loaded)'"
```

4. **Report result** to user:
   - Service status (running/failed)
   - Any errors in logs
   - Confirmation of successful upgrade

## VPS Quick Reference

| Setting | Value |
|---------|-------|
| SSH | `$VPS_SSH_ALIAS` from `.env` |
| User | `odoo19` |
| Database | `odoo_itberatung` |
| Config | `/etc/odoo19.conf` |
| Addons | `/opt/odoo19/addons-foundation-prod/` |

## When to Use

- After `./deploy.py vps` when schema changes are needed
- When "column does not exist" errors appear
- When new fields/models need to be created in database

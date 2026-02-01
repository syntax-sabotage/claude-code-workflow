# /vps-upgrade - Upgrade Module on VPS

> **Note:** This is a project-specific example from an Odoo deployment. Adapt the paths, SSH targets, and commands to your own infrastructure.

Quick command to upgrade a module on the production VPS.

## Usage

```
/vps-upgrade <module_name>
```

## Instructions

1. **Read** `.context/vps-deployment.md` if you need full context.

2. **Execute the upgrade**:
```bash
source .env && \
ssh $VPS_SSH_ALIAS "sudo systemctl stop $SERVICE_NAME && \
  sudo -u $SERVICE_USER $VENV_PATH/bin/python $ODOO_PATH/odoo-bin \
    -c $SERVICE_CONFIG \
    -d $DATABASE_NAME \
    -u <MODULE_NAME> \
    --stop-after-init && \
  sudo systemctl start $SERVICE_NAME"
```

3. **Verify**:
```bash
source .env && ssh $VPS_SSH_ALIAS "systemctl status $SERVICE_NAME | head -10"
source .env && ssh $VPS_SSH_ALIAS "tail -30 $LOG_PATH | grep -E '(ERROR|CRITICAL|Modules loaded)'"
```

4. **Report result** to user:
   - Service status (running/failed)
   - Any errors in logs
   - Confirmation of successful upgrade

## VPS Quick Reference

| Setting | Value |
|---------|-------|
| SSH | `$VPS_SSH_ALIAS` from `.env` |
| User | `$SERVICE_USER` from `.env` |
| Database | `$DATABASE_NAME` from `.env` |
| Config | `$SERVICE_CONFIG` from `.env` |
| Addons | `$ADDONS_PATH` from `.env` |

## When to Use

- After `./deploy.py vps` when schema changes are needed
- When "column does not exist" errors appear
- When new fields/models need to be created in database

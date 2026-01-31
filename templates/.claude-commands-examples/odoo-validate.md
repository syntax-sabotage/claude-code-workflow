# /odoo-validate - Odoo Module Validation

Run comprehensive validation on Odoo modules before deployment.

## What This Does

Executes all validation scripts in `scripts/validation/`:

1. **Manifest Validator** - V19 manifest compliance (version format, required fields, forbidden fields)
2. **XML Validator** - V19 view syntax (no attrs=, no expand=, deprecated attributes)
3. **Python Validator** - Syntax errors, deprecated decorators, hardcoded credentials
4. **Security Validator** - ir.model.access.csv coverage, sensitive fields with copy=False, sudo() audit
5. **Dependency Validator** - Manifest depends vs actual imports

## Usage

```
/odoo-validate [module_path]
```

If no module_path provided, validates all modules in `addons/`.

## Instructions

1. Run the validation suite:
```bash
./scripts/validation/run-all-validations.sh
```

2. Report results to the user with:
   - Total errors (MUST be fixed before deploy)
   - Total warnings (should review)
   - Specific fixes needed for any failures

3. If specific module requested, also check:
   - That security/ir.model.access.csv covers all declared models
   - That security/security.xml has appropriate record rules
   - That sensitive fields (password, token, secret, api_key) have `copy=False`

## Critical Checks

### Access Rules (Prevents AccessError)
Every model with `_name = 'x.y.z'` needs:
- Entry in `security/ir.model.access.csv`
- Format: `access_model_name,access_model_name,module.model_x_y_z,base.group_user,1,1,1,0`

### Sensitive Fields (Prevents Credential Exposure)
Fields named with password/token/secret/api_key patterns need:
```python
api_token = fields.Char(string="API Token", copy=False)  # copy=False is CRITICAL
```

### Dependencies (Prevents ImportError)
Every `from odoo.addons.X import` needs `'X'` in manifest `depends` list.

## Exit Codes

- `0` - All validations passed
- `1` - One or more validations failed

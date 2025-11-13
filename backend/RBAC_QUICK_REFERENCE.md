# RBAC Quick Reference

## 🔐 Role Names (Both Supported)

| Thai | English | Access Level |
|------|---------|--------------|
| Admin ใหญ่ | admin_main | Full system access |
| Admin กลุ่มงาน | admin_group | Meeting & agenda management |
| ผู้ใช้ทั่วไป | user | Read-only access |

## 🛡️ Role Checkers

### require_any_admin
```python
from app.core.rbac import require_any_admin

@router.post("/meetings")
async def create_meeting(
    current_user: User = Depends(require_any_admin)
):
    # Both admin_main and admin_group can access
    pass
```

**Accepts:** admin_main, admin_group (Thai or English)

### require_admin
```python
from app.core.rbac import require_admin

@router.post("/meetings/{id}/close")
async def close_meeting(
    current_user: User = Depends(require_admin)
):
    # Only admin_main can access
    pass
```

**Accepts:** admin_main only (Thai or English)

### require_authenticated
```python
from app.core.rbac import require_authenticated

@router.get("/meetings")
async def get_meetings(
    current_user: User = Depends(require_authenticated)
):
    # All authenticated users can access
    pass
```

**Accepts:** All roles

## 📋 Permission Matrix

| Action | admin_main | admin_group | user |
|--------|-----------|-------------|------|
| Create Meeting | ✅ | ✅ | ❌ |
| View Meetings | ✅ | ✅ | ✅ |
| Close Meeting | ✅ | ❌ | ❌ |
| Add Agenda | ✅ | ✅ | ❌ |
| Approve Agenda | ✅ | ❌ | ❌ |
| Upload Files | ✅ | ✅ | ❌ |
| View Reports | ✅ | ✅ | ✅ |
| Manage Reports | ✅ | ❌ | ❌ |
| Search Reports | ✅ | ✅ | ✅ |

## 🔧 Using Permissions Class

```python
from app.core.rbac import Permissions

# Check if user can add agenda
user_roles = ["admin_group"]  # or ["Admin กลุ่มงาน"]
if Permissions.can_add_agenda(user_roles):
    # Allow action
    pass

# Check if user can close meeting
if Permissions.can_close_meeting(user_roles):
    # Allow action
    pass
```

## 🧪 Testing Roles

### Test with curl
```bash
# Login
TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=group_admin&password=any" \
  | jq -r '.access_token')

# Test endpoint
curl -X GET http://localhost:8000/api/v1/meetings \
  -H "Authorization: Bearer $TOKEN"
```

### Test in Python
```python
from app.core.rbac import require_any_admin

# This will work for both:
# - User with role "admin_group"
# - User with role "Admin กลุ่มงาน"
```

## 🚨 Common Issues

### 403 Forbidden Error
**Cause:** User role not in allowed list  
**Fix:** Check user's role in database matches one of the accepted role names

### Role Not Found
**Cause:** Role name mismatch  
**Fix:** Use either Thai or English name consistently, or ensure both are in database

## 📝 Adding Custom Roles

```python
# In app/core/rbac.py
custom_checker = RoleChecker(["custom_role", "another_role"])

# Use in endpoint
@router.get("/custom")
async def custom_endpoint(
    current_user: User = Depends(custom_checker)
):
    pass
```

## ✅ Verification

Run RBAC test:
```bash
cd backend
python test_rbac_fix.py
```

Expected: All tests pass ✅

---
**Version:** v9.3.1  
**Updated:** 2024-12-20
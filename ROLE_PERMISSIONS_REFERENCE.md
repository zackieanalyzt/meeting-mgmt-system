# Role Permissions Reference

## System Roles

### 1. Admin ใหญ่ (Super Admin)
**Thai:** ผู้ดูแลระบบหลัก  
**English:** Main System Administrator

#### Permissions
- ✅ Create meetings
- ✅ Edit meetings
- ✅ Delete meetings
- ✅ Close meetings
- ✅ Approve agendas
- ✅ Add agendas
- ✅ Upload files
- ✅ Manage reports
- ✅ Search reports
- ✅ View all content
- ✅ Full system access

#### UI Features (Phase 9.2)
- Dashboard with full statistics
- "Create New Meeting" button
- "Manage Agendas" button
- Edit/Delete/Close buttons on meeting details
- All permission indicators

#### Test User
- Username: `admin`
- Fullname: ผู้ดูแลระบบ
- Department: IT
- Email: admin@hospital.local

---

### 2. Admin กลุ่มงาน (Group Admin)
**Thai:** ผู้ดูแลกลุ่มงาน  
**English:** Group Administrator

#### Permissions
- ✅ Add agendas to meetings
- ✅ Upload files
- ✅ Edit content before meeting closure
- ✅ Search reports
- ✅ View all content
- ❌ Cannot create meetings
- ❌ Cannot approve agendas
- ❌ Cannot close meetings
- ❌ Cannot manage reports

#### UI Features (Phase 9.2)
- Dashboard with statistics
- "Manage Agendas" button
- View meetings (no create button)
- No edit/delete/close buttons on meetings
- Limited permission indicators

#### Test User
- Username: `group_admin`
- Fullname: นายสมชาย ใจดี
- Department: การพยาบาล
- Email: somchai@hospital.local

---

### 3. ผู้ใช้ทั่วไป (Regular User)
**Thai:** ผู้ใช้งานทั่วไป  
**English:** Regular User

#### Permissions
- ✅ View meetings
- ✅ View agendas
- ✅ Search reports
- ❌ Cannot create meetings
- ❌ Cannot edit meetings
- ❌ Cannot add agendas
- ❌ Cannot upload files
- ❌ Cannot manage reports

#### UI Features (Phase 9.2)
- Dashboard with statistics (read-only)
- "View All Meetings" button only
- View meetings (no action buttons)
- Basic permission indicators

#### Test User
- Username: `user1`
- Fullname: นางสาวมาลี สวยงาม
- Department: เภสัชกรรม
- Email: malee@hospital.local

---

## Permission Matrix

| Feature | Admin ใหญ่ | Admin กลุ่มงาน | ผู้ใช้ทั่วไป |
|---------|-----------|---------------|-------------|
| View Dashboard | ✅ | ✅ | ✅ |
| View Meetings | ✅ | ✅ | ✅ |
| Create Meeting | ✅ | ❌ | ❌ |
| Edit Meeting | ✅ | ❌ | ❌ |
| Delete Meeting | ✅ | ❌ | ❌ |
| Close Meeting | ✅ | ❌ | ❌ |
| View Agendas | ✅ | ✅ | ✅ |
| Add Agenda | ✅ | ✅ | ❌ |
| Approve Agenda | ✅ | ❌ | ❌ |
| Upload Files | ✅ | ✅ | ❌ |
| Manage Reports | ✅ | ❌ | ❌ |
| Search Reports | ✅ | ✅ | ✅ |

---

## Implementation Details

### Backend (RBAC)

**File:** `backend/app/core/rbac.py`

```python
# Predefined role checkers
require_admin = RoleChecker(["Admin ใหญ่"])
require_group_admin = RoleChecker(["Admin กลุ่มงาน", "Admin ใหญ่"])
require_any_admin = RoleChecker(["Admin ใหญ่", "Admin กลุ่มงาน"])
require_authenticated = RoleChecker(["Admin ใหญ่", "Admin กลุ่มงาน", "ผู้ใช้ทั่วไป"])
```

### Frontend (AuthContext)

**File:** `frontend/src/contexts/AuthContext.jsx`

```javascript
// Helper functions
hasRole(role)           // Check if user has specific role
isAdmin()              // Check if user is Admin ใหญ่
isGroupAdmin()         // Check if user is Admin กลุ่มงาน or Admin ใหญ่
```

### Frontend (RoleGuard)

**File:** `frontend/src/components/common/RoleGuard.jsx`

```jsx
<RoleGuard allowedRoles={['Admin ใหญ่']}>
  <CreateMeeting />
</RoleGuard>
```

---

## Usage Examples

### Backend Endpoint Protection

```python
@router.post("/", response_model=MeetingResponse)
async def create_meeting(
    meeting: MeetingCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)  # Admin only
):
    # Create meeting logic
    pass
```

### Frontend Route Protection

```jsx
<Route 
  path="/meetings/create" 
  element={
    <ProtectedRoute>
      <RoleGuard allowedRoles={['Admin ใหญ่']}>
        <CreateMeeting />
      </RoleGuard>
    </ProtectedRoute>
  } 
/>
```

### Frontend Conditional Rendering

```jsx
{isAdmin() && (
  <button onClick={() => navigate('/meetings/create')}>
    Create New Meeting
  </button>
)}
```

---

## Role Assignment

Roles are assigned in the database through the `user_roles` table:

```sql
-- Example: Assign Admin role to user
INSERT INTO user_roles (user_id, role_id)
SELECT u.user_id, r.role_id
FROM users_local u, roles r
WHERE u.username = 'admin' AND r.role_name = 'Admin ใหญ่';
```

Dummy users are created automatically on backend startup via:
- `backend/app/services/auth_service.py`
- Function: `create_dummy_users()`

---

## Testing Role-Based Access

### Test Admin Access
```bash
# Login as admin
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -F "username=admin" \
  -F "password=test"

# Create meeting (should succeed)
curl -X POST http://127.0.0.1:8000/api/v1/meetings \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"meeting_name": "Test", "meeting_date": "2024-11-15"}'
```

### Test Non-Admin Access
```bash
# Login as regular user
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -F "username=user1" \
  -F "password=test"

# Try to create meeting (should fail with 403)
curl -X POST http://127.0.0.1:8000/api/v1/meetings \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"meeting_name": "Test", "meeting_date": "2024-11-15"}'
```

---

## Future Enhancements (Phase 9.3+)

1. **Dynamic Role Assignment**
   - UI for assigning roles to users
   - Role management interface

2. **Granular Permissions**
   - Department-based access
   - Meeting-specific permissions
   - Agenda-level permissions

3. **Audit Logging**
   - Track who performed what action
   - Role-based activity logs

4. **Role Hierarchy**
   - Inherit permissions from parent roles
   - Custom role creation

---

## Quick Reference

| Need to... | Use... |
|-----------|--------|
| Protect backend endpoint | `Depends(require_admin)` |
| Protect frontend route | `<RoleGuard allowedRoles={[...]}>` |
| Check role in component | `isAdmin()` or `hasRole('role')` |
| Show/hide UI element | `{isAdmin() && <Button />}` |
| Get user roles | `user.roles` from AuthContext |

---

## Support

For role-related issues:
1. Check user roles in database: `SELECT * FROM user_roles WHERE user_id = ?`
2. Verify role names match exactly (Thai characters)
3. Check backend logs for RBAC errors
4. Verify token includes user data with roles

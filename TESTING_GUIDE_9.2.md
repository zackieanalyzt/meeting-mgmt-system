# Testing Guide - Phase 9.2

## Quick Start

### 1. Start Backend
```bash
cd backend
python -m uvicorn app.main:app --reload
```
Wait for: `Application startup complete`

### 2. Start Frontend
```bash
cd frontend
npm run dev
```
Open: http://localhost:5173

---

## Test Cases

### Test 1: Login with Different Roles

#### Admin User
1. Go to http://localhost:5173
2. Login with username: `admin` (any password)
3. ✅ Should see Dashboard with:
   - Full name: "ผู้ดูแลระบบ"
   - Roles: "Admin ใหญ่"
   - "Create New Meeting" button visible
   - "Manage Agendas" button visible
   - Permission list showing admin capabilities

#### Group Admin User
1. Logout (click Logout button)
2. Login with username: `group_admin` (any password)
3. ✅ Should see Dashboard with:
   - Full name: "นายสมชาย ใจดี"
   - Roles: "Admin กลุ่มงาน"
   - "Manage Agendas" button visible
   - NO "Create New Meeting" button
   - Permission list showing group admin capabilities

#### Regular User
1. Logout
2. Login with username: `user1` (any password)
3. ✅ Should see Dashboard with:
   - Full name: "นางสาวมาลี สวยงาม"
   - Roles: "ผู้ใช้ทั่วไป"
   - Only "View All Meetings" button
   - Permission list showing basic user capabilities

---

### Test 2: Meeting Statistics

1. Login as any user
2. Check Dashboard statistics cards
3. ✅ Should show:
   - Total Meetings count
   - Active Meetings count
   - Closed Meetings count
4. Numbers should match actual data in database

---

### Test 3: View Meetings List

1. From Dashboard, click "View All Meetings"
2. ✅ Should see:
   - List of all meetings (if any exist)
   - Filter dropdown (All/Active/Closed)
   - Each meeting card shows:
     - Meeting name
     - Date and time
     - Location
     - Description preview
     - Status badge
3. Try filtering by status
4. ✅ Filter should work correctly

---

### Test 4: Create Meeting (Admin Only)

#### As Admin
1. Login as `admin`
2. Go to Dashboard
3. Click "Create New Meeting"
4. Fill in form:
   - Meeting Name: "Test Meeting 2024"
   - Date: Select today's date
   - Time: "14:00"
   - Location: "Conference Room A"
   - Description: "This is a test meeting"
5. Click "Create Meeting"
6. ✅ Should:
   - Show success alert
   - Redirect to meeting detail page
   - Display the new meeting

#### As Non-Admin
1. Login as `user1`
2. Try to access: http://localhost:5173/meetings/create
3. ✅ Should see "Access Denied" message
4. ✅ Should show required roles: "Admin ใหญ่"

---

### Test 5: View Meeting Details

1. From Meetings list, click on any meeting
2. ✅ Should see:
   - Meeting name as heading
   - Status badge (Active/Closed)
   - Date, time, location in info cards
   - Full description
   - Created/Updated/Closed timestamps
   - Admin action buttons (if admin)

---

### Test 6: Close Meeting (Admin Only)

1. Login as `admin`
2. View an active meeting
3. Click "Close Meeting" button
4. Confirm the action
5. ✅ Should:
   - Show success alert
   - Status badge changes to "Closed"
   - "Closed" timestamp appears
   - "Close Meeting" button disappears

---

### Test 7: Delete Meeting (Admin Only)

1. Login as `admin`
2. View any meeting
3. Click "Delete Meeting" button
4. Confirm the action
5. ✅ Should:
   - Show success alert
   - Redirect to meetings list
   - Meeting no longer appears in list

---

### Test 8: Token Persistence

1. Login as any user
2. Navigate to Dashboard
3. Refresh the page (F5)
4. ✅ Should:
   - Stay logged in
   - Show same user info
   - Not redirect to login

---

### Test 9: Logout

1. From any page, click "Logout" button
2. ✅ Should:
   - Redirect to login page
   - Clear user data
   - Require login to access protected pages

---

### Test 10: Protected Routes

1. Without logging in, try to access:
   - http://localhost:5173/dashboard
   - http://localhost:5173/meetings
2. ✅ Should redirect to login page

---

## Expected Backend API Responses

### Login Response
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "username": "admin",
    "email": "admin@hospital.local",
    "fullname": "ผู้ดูแลระบบ",
    "department": "IT",
    "roles": ["Admin ใหญ่"]
  }
}
```

### Meetings List Response
```json
[
  {
    "meeting_id": 1,
    "meeting_name": "Monthly Review",
    "meeting_date": "2024-11-15",
    "meeting_time": "14:00",
    "location": "Conference Room A",
    "description": "Monthly review meeting",
    "status": "active",
    "created_at": "2024-11-10T10:00:00",
    "updated_at": null,
    "closed_at": null
  }
]
```

---

## Troubleshooting

### Issue: "Failed to fetch meetings"
- Check backend is running
- Check browser console for errors
- Verify token is present in localStorage
- Check backend logs for errors

### Issue: "Access Denied" for admin user
- Check user roles in localStorage
- Verify backend returned roles in login response
- Check browser console for role data

### Issue: CORS errors
- Verify backend CORS settings include `http://localhost:5173`
- Check backend/app/core/config.py ALLOWED_ORIGINS

### Issue: 401 Unauthorized
- Token may be expired
- Logout and login again
- Check token in localStorage

### Issue: Meeting not appearing after creation
- Check backend logs for errors
- Verify database connection
- Check browser network tab for API response

---

## Browser Console Checks

### Check Token
```javascript
localStorage.getItem('token')
```

### Check User Data
```javascript
JSON.parse(localStorage.getItem('user'))
```

### Clear Storage (if needed)
```javascript
localStorage.clear()
```

---

## Success Criteria

✅ All 3 user roles can login  
✅ Dashboard shows correct role-based UI  
✅ Meeting statistics display correctly  
✅ Meeting list loads and filters work  
✅ Admin can create meetings  
✅ Non-admin cannot access create page  
✅ Meeting details display correctly  
✅ Admin can close meetings  
✅ Admin can delete meetings  
✅ Token persists across page refresh  
✅ Logout works correctly  
✅ Protected routes redirect to login  

---

## Next: Phase 9.3

After successful testing, proceed to Phase 9.3 for:
- Edit Meeting functionality
- Agenda management
- File uploads
- Enhanced UI styling

# Local Testing Guide - End-to-End Functionality

## Quick Start (5 Minutes)

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

### 3. Test Login & Create Meeting

1. **Login as admin_group:**
   - Username: `group_admin`
   - Password: (any)

2. **Open Browser DevTools:**
   - Press F12
   - Go to Network tab
   - Keep it open

3. **Create Meeting:**
   - Click "Create New Meeting"
   - Fill in:
     - Meeting Title: "Test Meeting"
     - Date: Select any future date
     - Start Time: "14:00"
     - End Time: "16:00"
     - Location: "Conference Room A"
   - Click "Create Meeting"

4. **Verify in Network Tab:**
   - Find POST request to `/api/v1/meetings`
   - Click on it
   - Go to "Headers" tab
   - Scroll to "Request Headers"
   - **Verify:** `Authorization: Bearer <token>` is present ✅

5. **Verify Response:**
   - Go to "Response" tab
   - **Verify:** Response includes `created_by_fullname` ✅
   - Example:
     ```json
     {
       "meeting_id": 4,
       "created_by": 533,
       "created_by_fullname": "นายสมชาย ใจดี",
       ...
     }
     ```

6. **Check Status:**
   - Should see success message
   - Should redirect to meeting detail page
   - **Verify:** Status is 201 Created ✅

---

## API Testing (Alternative Method)

### Using curl:

```bash
# 1. Login
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -F "username=group_admin" \
  -F "password=test"

# Copy the access_token from response

# 2. Create Meeting (replace <TOKEN> with your token)
curl -X POST http://127.0.0.1:8000/api/v1/meetings \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "meeting_title": "API Test Meeting",
    "meeting_date": "2024-11-20",
    "start_time": "14:00:00",
    "end_time": "16:00:00",
    "location": "Room B",
    "description": "Testing via curl"
  }'

# Expected: 201 Created with created_by_fullname

# 3. List Meetings
curl -X GET http://127.0.0.1:8000/api/v1/meetings \
  -H "Authorization: Bearer <TOKEN>"

# Expected: Array of meetings with created_by_fullname
```

### Using Postman:

1. **Login:**
   - Method: POST
   - URL: `http://127.0.0.1:8000/api/v1/auth/login`
   - Body: form-data
     - username: `group_admin`
     - password: `test`
   - Send
   - Copy `access_token` from response

2. **Create Meeting:**
   - Method: POST
   - URL: `http://127.0.0.1:8000/api/v1/meetings`
   - Headers:
     - Authorization: `Bearer <your_token>`
     - Content-Type: `application/json`
   - Body: raw JSON
     ```json
     {
       "meeting_title": "Postman Test",
       "meeting_date": "2024-11-20",
       "start_time": "14:00:00",
       "end_time": "16:00:00",
       "location": "Room C"
     }
     ```
   - Send
   - Verify: Status 201, response includes `created_by_fullname`

---

## Verification Checklist

### ✅ Priority 1: JWT Support
- [ ] Login successful
- [ ] Token saved in localStorage
- [ ] Network tab shows `Authorization: Bearer <token>` header
- [ ] All API requests include the header

### ✅ Priority 2: admin_group Can Create
- [ ] Login as `group_admin` works
- [ ] User roles include "Admin กลุ่มงาน"
- [ ] Create meeting button visible
- [ ] POST /api/v1/meetings returns 201 Created
- [ ] Meeting appears in database

### ✅ Priority 3: created_by_fullname
- [ ] Create meeting response includes `created_by_fullname`
- [ ] GET /api/v1/meetings includes fullname for all meetings
- [ ] GET /api/v1/meetings/{id} includes fullname
- [ ] Fullname matches database value

---

## Troubleshooting

### Issue: "Authorization header not present"
**Solution:**
- Check localStorage has token: Open DevTools → Application → Local Storage → Check for 'token'
- If missing, logout and login again
- Verify api.js interceptor is working

### Issue: "403 Forbidden when creating meeting"
**Solution:**
- Verify user has correct role: Check localStorage 'user' → roles
- Should include "Admin กลุ่มงาน" or "Admin ใหญ่"
- If not, check backend dummy user creation

### Issue: "created_by_fullname is null"
**Solution:**
- Check meeting.created_by is not null in database
- Verify user exists in users_local table
- Check relationship is loading (should use joinedload)

### Issue: "CORS error"
**Solution:**
- Verify backend CORS settings include frontend URL
- Check backend/app/core/config.py ALLOWED_ORIGINS
- Should include "http://localhost:5173"

---

## Expected Results Summary

### Login Response:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "username": "group_admin",
    "email": "somchai@hospital.local",
    "fullname": "นายสมชาย ใจดี",
    "department": "การพยาบาล",
    "roles": ["Admin กลุ่มงาน"]
  }
}
```

### Create Meeting Response (201):
```json
{
  "meeting_id": 4,
  "meeting_title": "Test Meeting",
  "meeting_date": "2024-11-20",
  "start_time": "14:00:00",
  "end_time": "16:00:00",
  "location": "Conference Room A",
  "description": "Test description",
  "status": "active",
  "created_by": 533,
  "created_by_fullname": "นายสมชาย ใจดี",
  "created_at": "2024-11-15T14:30:00",
  "updated_at": null,
  "closed_at": null
}
```

### List Meetings Response:
```json
[
  {
    "meeting_id": 1,
    "meeting_title": "Monthly Review",
    "created_by": 1,
    "created_by_fullname": "ผู้ดูแลระบบ",
    ...
  },
  {
    "meeting_id": 4,
    "meeting_title": "Test Meeting",
    "created_by": 533,
    "created_by_fullname": "นายสมชาย ใจดี",
    ...
  }
]
```

---

## Browser DevTools Tips

### Check Token:
1. Open DevTools (F12)
2. Go to Application tab
3. Expand Local Storage
4. Click on http://localhost:5173
5. Look for 'token' key
6. Value should be JWT token string

### Check Network Requests:
1. Open DevTools (F12)
2. Go to Network tab
3. Perform action (create meeting)
4. Click on request
5. Check Headers → Request Headers
6. Verify Authorization header

### Check Console Logs:
1. Open DevTools (F12)
2. Go to Console tab
3. Look for any errors
4. Should see success messages

---

## Test Users

| Username | Role | Password | Can Create Meeting |
|----------|------|----------|-------------------|
| admin | Admin ใหญ่ | any | ✅ Yes |
| group_admin | Admin กลุ่มงาน | any | ✅ Yes (NEW) |
| user1 | ผู้ใช้ทั่วไป | any | ❌ No |

---

## Success Criteria

All of these should be true:

✅ Login as group_admin successful  
✅ Token stored in localStorage  
✅ Authorization header in all API requests  
✅ Create meeting returns 201 Created  
✅ Response includes created_by_fullname  
✅ Meeting appears in list with fullname  
✅ No console errors  
✅ No network errors  

---

## Next Steps

After successful testing:
1. Review IMPLEMENTATION_REPORT.md for technical details
2. Review TEST_EVIDENCE.md for test results
3. Review CHANGE_SUMMARY.txt for changes made
4. Deploy to staging/production

---

## Support

If you encounter issues:
1. Check this README troubleshooting section
2. Review browser console for errors
3. Check backend logs for errors
4. Verify database connections
5. Check IMPLEMENTATION_REPORT.md for details

---

**Happy Testing! 🚀**

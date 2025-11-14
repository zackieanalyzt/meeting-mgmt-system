# Vue 3 Frontend - Quick Test Guide

## 🚀 Quick Start (2 Minutes)

### 1. Start Backend
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### 2. Start Vue Frontend
```bash
cd frontend
npm run dev
```

### 3. Open Browser
http://localhost:5173

---

## ✅ Test Checklist

### Test 1: Login
- [ ] Open http://localhost:5173
- [ ] Should redirect to /login
- [ ] Login with: `group_admin` / any password
- [ ] Should redirect to Dashboard

### Test 2: Dashboard Quick Action
- [ ] On Dashboard, find "การดำเนินการด่วน" section
- [ ] Click "สร้างการประชุมใหม่" button (blue button with + icon)
- [ ] Should navigate to /meetings/create

### Test 3: Create Meeting
- [ ] Fill in form:
  - ชื่อการประชุม: "ทดสอบการประชุม"
  - วันที่: Select today or future date
  - เวลาเริ่ม: "14:00"
  - เวลาสิ้นสุด: "16:00"
  - สถานที่: "ห้องประชุม 1"
  - รายละเอียด: "ทดสอบระบบ"
- [ ] Click "สร้างการประชุม"
- [ ] Should see success message
- [ ] Should auto-redirect to /meetings

### Test 4: Meeting List
- [ ] Should see the newly created meeting
- [ ] Try filter dropdown (ทั้งหมด/กำลังดำเนินการ/ปิดแล้ว)
- [ ] Click on a meeting card
- [ ] Should navigate to detail page

### Test 5: Navigation Menu
- [ ] Click "จัดการการประชุม" in navbar
- [ ] Should go to /meetings
- [ ] Click "สร้างการประชุมใหม่" button
- [ ] Should go to /meetings/create

### Test 6: JWT Token (DevTools)
- [ ] Open DevTools (F12)
- [ ] Go to Network tab
- [ ] Create a new meeting
- [ ] Find POST request to `/api/v1/meetings`
- [ ] Check Request Headers
- [ ] Should see: `Authorization: Bearer <token>`

---

## 🎯 Expected Results

### Dashboard
```
✅ "สร้างการประชุมใหม่" button visible (blue, with + icon)
✅ "ดูรายการการประชุม" button visible (green)
✅ Other quick action buttons present
```

### Create Meeting Page
```
✅ Form with all fields (title, date, times, location, description)
✅ Required fields marked with *
✅ Cancel and Submit buttons
✅ Thai labels
```

### Meeting List Page
```
✅ "สร้างการประชุมใหม่" button in top right
✅ Filter dropdown
✅ Meeting cards in grid layout
✅ Each card shows: title, date, time, location, creator, status
✅ Click card → navigate to detail
```

### Navigation Bar
```
✅ "จัดการการประชุม" link visible
✅ Highlights when on meeting pages
✅ Other menu items still present
```

---

## 🔍 Verification Points

### 1. JWT Token Attached
**How to verify:**
1. Open DevTools → Network tab
2. Create a meeting
3. Find POST `/api/v1/meetings` request
4. Check Headers → Request Headers
5. Look for: `Authorization: Bearer eyJ...`

**Expected:** ✅ Token present in all API requests

### 2. Backend Response
**Expected response from POST /meetings:**
```json
{
  "meeting_id": 5,
  "meeting_title": "ทดสอบการประชุม",
  "meeting_date": "2024-11-20",
  "start_time": "14:00:00",
  "end_time": "16:00:00",
  "location": "ห้องประชุม 1",
  "description": "ทดสอบระบบ",
  "status": "active",
  "created_by": 533,
  "created_by_fullname": "นายสมชาย ใจดี",
  "created_at": "2024-11-15T...",
  "updated_at": null,
  "closed_at": null
}
```

### 3. Meeting List Response
**Expected response from GET /meetings:**
```json
[
  {
    "meeting_id": 1,
    "meeting_title": "...",
    "created_by_fullname": "...",
    ...
  }
]
```

---

## 🐛 Troubleshooting

### Issue: "Cannot read property 'token'"
**Solution:** Login again, token may have expired

### Issue: "403 Forbidden"
**Solution:** User doesn't have permission. Login as `group_admin` or `admin`

### Issue: "Network Error"
**Solution:** Check backend is running at http://localhost:8000

### Issue: "CORS Error"
**Solution:** Backend CORS should allow http://localhost:5173

### Issue: Form doesn't submit
**Solution:** Check all required fields are filled

### Issue: No meetings showing
**Solution:** Create a meeting first, or check API response in Network tab

---

## 📊 Success Criteria

All of these should be ✅:

- [ ] Can login successfully
- [ ] Dashboard shows quick action button
- [ ] Can navigate to create meeting page
- [ ] Can fill and submit meeting form
- [ ] Success message appears
- [ ] Redirects to meeting list
- [ ] New meeting appears in list
- [ ] Can filter meetings by status
- [ ] Can view meeting detail
- [ ] JWT token in all API requests
- [ ] No console errors
- [ ] Navigation menu works
- [ ] All Thai labels display correctly

---

## 🎉 If All Tests Pass

**Congratulations!** 🎊

Your Vue 3 frontend is fully functional with:
- ✅ Complete meeting management UI
- ✅ JWT authentication working
- ✅ All CRUD operations ready
- ✅ Responsive design
- ✅ Thai language support

**Next Steps:**
1. Test with different user roles
2. Add more features (edit, delete)
3. Enhance UI styling
4. Add more validation

---

## 📞 Quick Commands

```bash
# Start backend
cd backend && python -m uvicorn app.main:app --reload

# Start frontend
cd frontend && npm run dev

# Check backend health
curl http://localhost:8000/health

# Test login (get token)
curl -X POST http://localhost:8000/api/v1/auth/login \
  -F "username=group_admin" \
  -F "password=test"

# Test create meeting (replace TOKEN)
curl -X POST http://localhost:8000/api/v1/meetings \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "meeting_title": "Test",
    "meeting_date": "2024-11-20",
    "start_time": "14:00:00",
    "end_time": "16:00:00",
    "location": "Room A"
  }'
```

---

**Happy Testing! 🚀**

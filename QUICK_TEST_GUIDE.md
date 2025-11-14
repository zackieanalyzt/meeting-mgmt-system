# Quick Test Guide - 5 Minutes

## 🚀 Start Services

```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

---

## ✅ Test 1: React UI (2 minutes)

### Step 1: Login
- Open: http://localhost:5173
- Login: `group_admin` / any password
- ✅ Should see Dashboard

### Step 2: Create Meeting
- Click "สร้างการประชุมใหม่" button
- Fill form:
  - Title: "Test Meeting"
  - Date: Tomorrow
  - Start: "14:00"
  - End: "16:00"
  - Location: "Room A"
- Click "Create Meeting"
- ✅ Should see success message
- ✅ Should redirect to detail page

### Step 3: View List
- Navigate to "Meetings" (or back button)
- ✅ Should see new meeting in list
- Try filter dropdown
- ✅ Filter should work

### Step 4: View Detail
- Click on a meeting card
- ✅ Should see full details
- ✅ Should see created_by_fullname
- ✅ Admin buttons visible (if admin/group_admin)

---

## 🔒 Test 2: Security Features (3 minutes)

### Test A: Rate Limiting
```bash
# Try 6 login attempts rapidly
for i in {1..6}; do
  curl -X POST http://localhost:8000/api/v1/auth/login \
    -F "username=test" \
    -F "password=wrong"
  echo ""
done
```
✅ 6th attempt should return 429 Too Many Requests

### Test B: Security Headers
```bash
curl -I http://localhost:8000/
```
✅ Should see:
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- Strict-Transport-Security
- Referrer-Policy: no-referrer

### Test C: Audit Logging
```bash
# Login via UI, then check logs
cat backend/logs/audit.log
```
✅ Should see:
- LOGIN_SUCCESS entries
- MEETING_CREATE entries

### Test D: CORS Protection
```bash
# Try from unauthorized origin
curl -X GET http://localhost:8000/api/v1/meetings \
  -H "Origin: http://evil.com" \
  -H "Authorization: Bearer fake-token"
```
✅ Should be blocked (CORS error)

### Test E: Error Sanitization
```bash
# Trigger error
curl -X GET http://localhost:8000/api/v1/meetings/99999 \
  -H "Authorization: Bearer fake-token"
```
✅ Should return generic error (no stack trace)

---

## 📊 Expected Results

### Frontend
✅ Modern Tailwind UI  
✅ Responsive design  
✅ Form validation works  
✅ Success/error messages  
✅ Auto-redirect after create  
✅ Filter works  
✅ No console errors  

### Backend Security
✅ Rate limiting active  
✅ Security headers present  
✅ CORS hardened  
✅ Audit logs created  
✅ Errors sanitized  
✅ bcrypt working  

---

## 🐛 Troubleshooting

**Issue:** Can't create meeting  
**Fix:** Check you're logged in as admin or group_admin

**Issue:** 429 Too Many Requests  
**Fix:** Wait 5 minutes or restart backend

**Issue:** CORS error  
**Fix:** Verify frontend is at http://localhost:5173

**Issue:** No audit logs  
**Fix:** Check `backend/logs/` directory exists

---

## ✅ Success Criteria

All of these should be ✅:

- [ ] Can login successfully
- [ ] Dashboard shows quick action button
- [ ] Can create meeting with validation
- [ ] Meeting appears in list
- [ ] Can view meeting detail
- [ ] Filter works
- [ ] Rate limiting works (6th attempt fails)
- [ ] Security headers present
- [ ] Audit log has entries
- [ ] Tailwind styling looks good
- [ ] No breaking changes to existing features

---

## 🎉 If All Tests Pass

**Congratulations!** Your system is:
- ✅ Fully functional
- ✅ Secure
- ✅ Production ready

**Next:** Deploy to staging/production

---

**Testing Time:** ~5 minutes  
**Status:** Ready to test! 🚀

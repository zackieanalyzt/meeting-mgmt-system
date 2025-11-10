# Quick Start - Phase 9.2

## 🚀 Start in 30 Seconds

### 1. Backend
```bash
cd backend
python -m uvicorn app.main:app --reload
```
✅ Wait for: `Application startup complete`

### 2. Frontend
```bash
cd frontend
npm run dev
```
✅ Open: http://localhost:5173

---

## 🔑 Login

| User | Role | Features |
|------|------|----------|
| `admin` | Super Admin | Full access |
| `group_admin` | Group Admin | Limited admin |
| `user1` | Regular User | View only |

Password: **any**

---

## 🎯 What to Test

1. **Login** → See dashboard with your role
2. **Dashboard** → Check statistics and permissions
3. **Meetings** → View list, filter by status
4. **Create** → (Admin only) Create new meeting
5. **Details** → View meeting, try admin actions
6. **Logout** → Test logout and re-login

---

## 📍 URLs

- Frontend: http://localhost:5173
- Backend: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

---

## ✨ New Features

✅ Role-based dashboard  
✅ Meeting CRUD operations  
✅ Real-time statistics  
✅ Access control  
✅ Token persistence  

---

## 🐛 Troubleshooting

**Can't login?**
- Check backend is running
- Try: `admin` / any password

**No meetings showing?**
- Create one as admin
- Check backend logs

**Access denied?**
- Check your role
- Some features are admin-only

**CORS error?**
- Backend should allow localhost:5173
- Check backend/app/core/config.py

---

## 📖 Full Docs

- `PHASE_9.2_COMPLETE.md` - Complete docs
- `TESTING_GUIDE_9.2.md` - Testing guide
- `ROLE_PERMISSIONS_REFERENCE.md` - Roles & permissions

---

**That's it! Start testing! 🎉**

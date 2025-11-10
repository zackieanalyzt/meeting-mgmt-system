# Quick Start Guide - Phase 9.1

## Prerequisites
- Backend running at http://127.0.0.1:8000
- Node.js installed

## Step 1: Install Frontend Dependencies

```bash
cd frontend
npm install
```

## Step 2: Start Backend (if not running)

In terminal 1:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

Backend will be at: http://127.0.0.1:8000
Swagger docs: http://127.0.0.1:8000/docs

## Step 3: Start Frontend

In terminal 2:
```bash
cd frontend
npm run dev
```

Frontend will be at: http://localhost:5173

## Step 4: Test Login

1. Open http://localhost:5173
2. You'll be redirected to /login
3. Use any of these usernames (password can be anything for now):
   - `admin`
   - `group_admin`
   - `user1`
4. After login, you'll see the Dashboard with user info
5. Click Logout to test logout flow

## Troubleshooting

### CORS Issues
If you see CORS errors, ensure backend has CORS middleware configured in `backend/app/main.py`

### 401 Unauthorized
- Check backend is running
- Verify dummy users were created (check backend startup logs)
- Check browser console for error details

### Module Not Found
Run `npm install` in frontend directory

## What's Working

✅ Login form with username/password
✅ JWT token generation and storage
✅ AuthContext managing global auth state
✅ Protected routes (Dashboard, Meetings)
✅ Automatic token injection in API calls
✅ Logout functionality
✅ Redirect to login when not authenticated

## Next Phase

Phase 10 will add:
- Role-based access control (RBAC)
- Meeting CRUD operations
- UI styling
- User management

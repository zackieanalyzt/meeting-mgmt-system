# Quick Start Guide - v9.3.1

## 🚀 Start Development Server

### Option 1: With Verification (Recommended)
```bash
# Windows
cd backend
verify_startup.bat
uvicorn app.main:app --reload

# Linux/Mac
cd backend
bash verify_startup.sh
uvicorn app.main:app --reload
```

### Option 2: Direct Start
```bash
cd backend
uvicorn app.main:app --reload
```

## ✅ Expected Startup Output
```
✅ Database tables created
✅ Dummy users created
✅ Default objectives seeded
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

## 🧪 Test Endpoints

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. API Documentation
Open: `http://localhost:8000/docs`

### 3. Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=group_admin&password=any"
```

## 👥 Default Users

| Username | Role | Password |
|----------|------|----------|
| admin | Admin ใหญ่ | any |
| group_admin | Admin กลุ่มงาน | any |
| user1 | ผู้ใช้ทั่วไป | any |

## 📋 Default Objectives

1. เพื่อทราบ
2. เพื่อพิจารณา
3. เพื่ออนุมัติ
4. เพื่อสั่งการ

## 🔧 Troubleshooting

### ORM Relationship Error
```bash
python test_orm_relationships.py
```

### Database Connection Error
Check `.env` file:
```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=meeting_mgmt
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
```

### Port Already in Use
```bash
# Find process using port 8000
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000

# Kill process and restart
```

## 📚 API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/auth/me` - Get current user

### Meetings
- `POST /api/v1/meetings` - Create meeting
- `GET /api/v1/meetings` - List meetings
- `GET /api/v1/meetings/{id}` - Get meeting

### Agendas
- `POST /api/v1/meetings/{id}/agendas` - Create agenda with files
- `GET /api/v1/meetings/{id}/agendas` - Get meeting agendas

### Objectives
- `GET /api/v1/objectives` - List objectives
- `POST /api/v1/objectives` - Create objective

## 🎯 Next Steps

1. ✅ Verify server starts successfully
2. ✅ Test login in Swagger UI
3. ✅ Create a test meeting
4. ✅ Add agenda with objectives
5. 🚀 Ready for Phase 9.4 (React UI)

---
**Version:** v9.3.1  
**Backend:** FastAPI + SQLAlchemy  
**Database:** PostgreSQL 17 + MariaDB 11
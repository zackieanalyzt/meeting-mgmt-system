# System Architecture Overview
**ระบบจัดการวาระและรายงานการประชุม v3.3**

เอกสารนี้อธิบายสถาปัตยกรรมและการทำงานของระบบ Meeting Management System สำหรับนักพัฒนาใหม่

---

## 1️⃣ จุดเริ่มต้นของระบบ (System Entry Points)

### Backend (FastAPI)
```
backend/app/main.py → FastAPI app instance
├── startup_event() → สร้าง dummy users
├── CORS middleware → อนุญาต frontend เข้าถึง
└── api_router → รวม endpoints ทั้งหมด
```

**ลำดับการโหลด:**
1. `main.py` → สร้าง FastAPI app
2. `api/v1/api.py` → รวม router ทั้งหมด
3. `core/auth.py` → JWT middleware
4. `core/rbac.py` → Role-based access control

### Frontend (Vue 3 + Vite)
```
frontend/src/main.js → Vue app entry point
├── App.vue → Root component
├── router/index.js → Route definitions + auth guard
└── stores/auth.js → Pinia state management
```

**ลำดับการโหลด:**
1. `main.js` → สร้าง Vue app + Pinia + Router
2. `App.vue` → แสดง Navbar + router-view
3. `router/index.js` → ตรวจสอบ token ก่อนเข้าหน้า

---

## 2️⃣ การทำงานแบบแยกบทบาท (Role-based Flow)

### Admin ใหญ่ (Main Admin)
- **Routes:** ทุก route + `/meetings/create`, `/meetings/{id}/close`
- **Endpoints:** `require_admin` decorator
- **สิทธิ์:** สร้าง/ปิดการประชุม, อนุมัติวาระ, จัดการรายงาน

### Admin กลุ่มงาน (Group Admin)  
- **Routes:** Dashboard, CurrentMeeting, ReportsHistory, SearchReports
- **Endpoints:** `require_any_admin` decorator
- **สิทธิ์:** เพิ่ม/แก้ไขวาระ, อัปโหลดไฟล์ (ก่อนปิดประชุม)

### ผู้ใช้ทั่วไป (General User)
- **Routes:** Dashboard, CurrentMeeting (read-only), ReportsHistory, SearchReports
- **Endpoints:** `require_authenticated` decorator
- **สิทธิ์:** ดูวาระ, ค้นหารายงาน

**การตรวจสอบสิทธิ์:**
```
frontend/router/index.js → ตรวจ localStorage.token
backend/core/rbac.py → RoleChecker class
backend/core/auth.py → get_current_user() + JWT decode
```

---

## 3️⃣ เส้นทางข้อมูล (Data Flow)

### ตัวอย่าง: เพิ่มวาระการประชุม
```
1. CurrentMeeting.vue → showAddAgenda = true
2. AgendaForm.vue → axios.post('/api/v1/agendas')
3. api/index.js → แนบ JWT token ใน header
4. endpoints/agendas.py → create_agenda() + require_any_admin
5. core/rbac.py → ตรวจสอบ role ผู้ใช้
6. models/agenda.py → SQLAlchemy ORM
7. PostgreSQL → บันทึกข้อมูล
8. Response JSON → กลับไป frontend
```

### Authentication Flow
```
Login.vue → auth/login → authenticate_user() → JWT token → localStorage
↓
router guard → ตรวจ token → redirect ตาม role
↓
API calls → Authorization header → verify_token() → get_user_roles()
```

---

## 4️⃣ โครงสร้างโฟลเดอร์ (Folder/Module Overview)

### Backend Structure
```
backend/
├── app/
│   ├── main.py                 # FastAPI entry point
│   ├── core/
│   │   ├── config.py          # Environment variables
│   │   ├── database.py        # PostgreSQL + MariaDB connections
│   │   ├── auth.py            # JWT token management
│   │   └── rbac.py            # Role-based access control
│   ├── models/                # SQLAlchemy ORM models
│   │   ├── user.py            # users_local table
│   │   ├── meeting.py         # meetings table
│   │   └── agenda.py          # agendas table
│   ├── schemas/               # Pydantic request/response models
│   ├── api/v1/endpoints/      # REST API routes
│   │   ├── auth.py            # /auth/login, /auth/me
│   │   ├── meetings.py        # /meetings CRUD
│   │   └── agendas.py         # /agendas CRUD
│   └── services/
│       └── auth_service.py    # Dummy user creation
├── alembic/                   # Database migrations
└── requirements.txt           # Python dependencies
```

### Frontend Structure
```
frontend/
├── src/
│   ├── main.js               # Vue app entry
│   ├── App.vue               # Root component
│   ├── router/index.js       # Route definitions + guards
│   ├── views/                # Page components
│   │   ├── Login.vue         # Login form
│   │   ├── Dashboard.vue     # Stats overview
│   │   ├── CurrentMeeting.vue # Meeting agendas
│   │   └── ReportsHistory.vue # Historical reports
│   ├── components/
│   │   └── Navbar.vue        # Navigation bar
│   ├── stores/
│   │   └── auth.js           # Pinia auth state
│   └── api/
│       └── index.js          # Axios configuration
├── package.json              # Node dependencies
└── vite.config.js            # Vite dev server config
```

### Configuration Files
- **`.env`** → Database credentials, JWT secret
- **`docker-compose.yml`** → Services orchestration
- **`alembic.ini`** → Database migration config
- **`tailwind.config.js`** → CSS framework config

---

## 5️⃣ ลำดับการทำงาน (Execution Sequence)

### 1. System Startup
```bash
docker-compose up
├── PostgreSQL + MariaDB → Database ready
├── Backend → main.py → create_dummy_users()
└── Frontend → Vite dev server → http://localhost:5173
```

### 2. User Login Process
```
1. เข้า http://localhost:5173 → redirect /login
2. Login.vue → handleLogin() → form validation
3. axios.post('/api/v1/auth/login') → JWT token
4. localStorage.setItem('token') → บันทึก token
5. router.push('/dashboard') → เข้าหน้าหลัก
```

### 3. Dashboard Loading
```
1. Dashboard.vue → onMounted() → loadDashboardData()
2. api/index.js → แนบ Authorization header
3. Multiple API calls → /meetings, /agendas, /reports
4. Backend → verify JWT → get user roles
5. Return filtered data → แสดงตาม role
```

### 4. Meeting Management Flow
```
Admin ใหญ่:
1. Dashboard → "สร้างการประชุม" → MeetingForm
2. POST /api/v1/meetings → require_admin
3. Database → INSERT meetings table
4. Redirect → CurrentMeeting.vue

Admin กลุ่มงาน:
1. CurrentMeeting → "เพิ่มวาระ" → AgendaForm  
2. POST /api/v1/agendas → require_any_admin
3. File upload → POST /api/v1/files/upload
4. Real-time update → agenda list refresh
```

---

## 6️⃣ สรุปการทำงานของระบบโดยรวม (System Summary)

### Technology Stack Flow
```
Vue 3 Frontend → Axios HTTP Client → FastAPI Backend → SQLAlchemy ORM → PostgreSQL Database
     ↓              ↓                    ↓                ↓              ↓
TailwindCSS    JWT Token         Pydantic Schemas    Alembic        MariaDB (Auth)
```

### Role-based Access Summary
| บทบาท | หน้าที่เข้าถึงได้ | API Endpoints |
|--------|------------------|---------------|
| **Admin ใหญ่** | ทุกหน้า + การจัดการ | ทุก endpoint + admin-only |
| **Admin กลุ่มงาน** | Dashboard, Meeting, Reports | CRUD agendas/files |
| **ผู้ใช้ทั่วไป** | Dashboard, Reports (read-only) | GET endpoints only |

### Data Architecture
```
Frontend State (Pinia) ←→ API Layer (Axios) ←→ FastAPI Routes ←→ Business Logic ←→ Database
     ↓                        ↓                    ↓                ↓            ↓
- User info              - JWT tokens        - RBAC middleware   - ORM models  - PostgreSQL
- Meeting data           - Error handling    - Input validation  - Services    - MariaDB
- UI state               - Request/Response  - Response schemas  - Auth logic  - File storage
```

### Security Flow
1. **Authentication:** Username/Password → JWT Token → localStorage
2. **Authorization:** JWT decode → User roles → Permission check
3. **API Protection:** Every request → Token validation → Role verification
4. **Route Guards:** Frontend router → Token check → Role-based redirect

---

## 7️⃣ Quick Start สำหรับ Developer ใหม่

### 1. Setup Environment
```bash
# Clone และ setup
cp .env.example .env
docker-compose up -d

# ตรวจสอบ services
curl http://localhost:8000/health    # Backend health
curl http://localhost:5173           # Frontend
```

### 2. Test Login
```
Username: admin, group_admin, user1
Password: อะไรก็ได้ (dummy auth)
```

### 3. Key Files to Understand
- **`backend/app/main.py`** → เริ่มต้น backend
- **`frontend/src/router/index.js`** → Route + auth guard
- **`backend/app/core/rbac.py`** → Role permissions
- **`backend/app/models/`** → Database schema

### 4. Development Workflow
```
1. แก้ไข backend → Auto reload (uvicorn --reload)
2. แก้ไข frontend → Hot reload (Vite HMR)  
3. Database changes → alembic revision --autogenerate
4. Test API → http://localhost:8000/docs (Swagger UI)
```

---

**🎯 สรุป:** ระบบนี้เป็น Full-stack application ที่ใช้ JWT authentication + RBAC authorization โดย Frontend (Vue 3) เรียก Backend (FastAPI) ผ่าน REST API และจัดเก็บข้อมูลใน PostgreSQL พร้อม Role-based access control ตามสเปคของโรงพยาบาล
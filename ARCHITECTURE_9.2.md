# Architecture Overview - Phase 9.2

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                     │
│                    http://localhost:5173                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  LoginForm   │  │  Dashboard   │  │ MeetingList  │      │
│  │              │  │              │  │              │      │
│  │ - Username   │  │ - Stats      │  │ - Filter     │      │
│  │ - Password   │  │ - Roles      │  │ - Cards      │      │
│  │ - Submit     │  │ - Actions    │  │ - Status     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │MeetingDetail │  │CreateMeeting │  │  RoleGuard   │      │
│  │              │  │              │  │              │      │
│  │ - Info       │  │ - Form       │  │ - Check Role │      │
│  │ - Actions    │  │ - Validate   │  │ - Allow/Deny │      │
│  │ - Admin Btns │  │ - Submit     │  │ - Fallback   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                            │
│  ┌─────────────────────────────────────────────────┐       │
│  │            AuthContext (Global State)           │       │
│  │  - user, token, isAuthenticated                 │       │
│  │  - login(), logout()                            │       │
│  │  - isAdmin(), isGroupAdmin(), hasRole()         │       │
│  └─────────────────────────────────────────────────┘       │
│                                                            │
│  ┌─────────────────────────────────────────────────┐       │
│  │         API Service (Axios Instance)            │       │
│  │  - baseURL: http://127.0.0.1:8000               │       │
│  │  - Request Interceptor: Inject JWT              │       │
│  │  - Response Interceptor: Handle 401             │       │
│  └─────────────────────────────────────────────────┘       │
│                                                            │
└───────────────────────┬────────────────────────────────────┘
                        │
                        │ HTTP/REST API
                        │ JWT Bearer Token
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                     Backend (FastAPI)                        │
│                  http://127.0.0.1:8000                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────────────────────────────┐        │
│  │              API Endpoints (v1)                  │        │
│  │                                                  │        │
│  │  POST   /api/v1/auth/login                      │        │
│  │  GET    /api/v1/meetings                        │        │
│  │  GET    /api/v1/meetings/{id}                   │        │
│  │  POST   /api/v1/meetings                        │        │
│  │  PUT    /api/v1/meetings/{id}                   │        │
│  │  DELETE /api/v1/meetings/{id}                   │        │
│  │  POST   /api/v1/meetings/{id}/close             │        │
│  │                                                  │        │
│  └─────────────────────────────────────────────────┘        │
│                                                               │
│  ┌─────────────────────────────────────────────────┐        │
│  │           RBAC (Role-Based Access)               │        │
│  │                                                  │        │
│  │  require_admin         → Admin ใหญ่             │        │
│  │  require_group_admin   → Admin กลุ่มงาน         │        │
│  │  require_authenticated → All roles              │        │
│  │                                                  │        │
│  └─────────────────────────────────────────────────┘        │
│                                                               │
│  ┌─────────────────────────────────────────────────┐        │
│  │              JWT Authentication                  │        │
│  │                                                  │        │
│  │  - create_access_token()                        │        │
│  │  - verify_token()                               │        │
│  │  - get_current_user()                           │        │
│  │  - get_user_roles()                             │        │
│  │                                                  │        │
│  └─────────────────────────────────────────────────┘        │
│                                                               │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ SQL Queries
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                      Databases                               │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────┐  ┌──────────────────────┐    │
│  │   PostgreSQL (Primary)   │  │  MariaDB (HR Auth)   │    │
│  │   192.168.100.70:5432    │  │  192.168.100.25:3306 │    │
│  │                          │  │                      │    │
│  │  Tables:                 │  │  Tables:             │    │
│  │  - users_local           │  │  - hr.personnel      │    │
│  │  - roles                 │  │                      │    │
│  │  - user_roles            │  │  Used for:           │    │
│  │  - meetings              │  │  - Login validation  │    │
│  │  - agendas               │  │  - MD5 password      │    │
│  │  - files                 │  │                      │    │
│  │  - reports               │  │                      │    │
│  │  - search_log            │  │                      │    │
│  │                          │  │                      │    │
│  └──────────────────────────┘  └──────────────────────┘    │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. Login Flow
```
User Input (LoginForm)
    ↓
FormData (username, password)
    ↓
POST /api/v1/auth/login
    ↓
verify_hr_user() → MariaDB
    ↓
get_user_roles() → PostgreSQL
    ↓
create_access_token() → JWT
    ↓
Response: { access_token, user: { roles } }
    ↓
localStorage.setItem('token', ...)
    ↓
AuthContext.login() → Update state
    ↓
Navigate to Dashboard
```

### 2. Protected API Call Flow
```
Component needs data
    ↓
api.get('/api/v1/meetings')
    ↓
Request Interceptor
    ↓
Add: Authorization: Bearer <token>
    ↓
Backend receives request
    ↓
Depends(require_authenticated)
    ↓
verify_token() → Extract username
    ↓
get_current_user() → PostgreSQL
    ↓
get_user_roles() → Check permissions
    ↓
Execute endpoint logic
    ↓
Return response
    ↓
Component receives data
    ↓
Update UI
```

### 3. Role-Based Access Flow
```
User navigates to /meetings/create
    ↓
ProtectedRoute checks isAuthenticated
    ↓
RoleGuard checks user.roles
    ↓
If 'Admin ใหญ่' in roles:
    → Render CreateMeeting
Else:
    → Show "Access Denied"
```

---

## Component Hierarchy

```
App
├── AuthProvider (Context)
│   └── Router
│       ├── LoginForm
│       └── ProtectedRoute
│           ├── Dashboard
│           │   ├── Stats Cards
│           │   ├── User Info
│           │   └── Quick Actions
│           │
│           ├── MeetingList
│           │   ├── Filter Dropdown
│           │   └── Meeting Cards
│           │
│           ├── MeetingDetail
│           │   ├── Meeting Info
│           │   └── Admin Actions
│           │
│           └── RoleGuard
│               └── CreateMeeting
│                   └── Meeting Form
```

---

## State Management

### Global State (AuthContext)
```javascript
{
  user: {
    username: string,
    email: string,
    fullname: string,
    department: string,
    roles: string[]
  },
  token: string,
  isAuthenticated: boolean,
  loading: boolean
}
```

### Local Storage
```javascript
{
  token: "eyJhbGc...",
  user: "{...}"  // JSON string
}
```

### Component State Examples
```javascript
// Dashboard
{
  stats: { totalMeetings, activeMeetings, closedMeetings },
  loading: boolean
}

// MeetingList
{
  meetings: Meeting[],
  filter: 'all' | 'active' | 'closed',
  loading: boolean,
  error: string
}

// CreateMeeting
{
  formData: { meeting_name, meeting_date, ... },
  loading: boolean,
  error: string
}
```

---

## Security Layers

### Layer 1: Frontend Route Protection
```
ProtectedRoute → Check isAuthenticated
    ↓
RoleGuard → Check user.roles
    ↓
Component renders
```

### Layer 2: API Request Protection
```
Request Interceptor → Add JWT token
    ↓
Backend receives request
    ↓
Depends(require_admin) → Verify role
    ↓
Execute if authorized
```

### Layer 3: Database Protection
```
SQLAlchemy ORM → Parameterized queries
    ↓
No SQL injection possible
    ↓
Role-based data filtering
```

---

## API Response Formats

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

### Meeting List Response
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

### Error Response
```json
{
  "detail": "Invalid username or password"
}
```

---

## Technology Stack

### Frontend
- **Framework:** React 18.2.0
- **Router:** React Router DOM 6.20.0
- **HTTP Client:** Axios 1.6.2
- **Build Tool:** Vite 5.0.0
- **State:** Context API

### Backend
- **Framework:** FastAPI 3.5.1
- **ORM:** SQLAlchemy
- **Auth:** python-jose (JWT)
- **Server:** Uvicorn
- **Validation:** Pydantic

### Databases
- **Primary:** PostgreSQL 192.168.100.70:5432
- **Auth:** MariaDB 192.168.100.25:3306

---

## File Organization

```
project/
├── backend/
│   └── app/
│       ├── api/v1/endpoints/
│       │   ├── auth.py          ← Login, JWT
│       │   └── meetings.py      ← CRUD operations
│       ├── core/
│       │   ├── auth.py          ← JWT functions
│       │   ├── rbac.py          ← Role checking
│       │   ├── config.py        ← Settings
│       │   └── database.py      ← DB connections
│       ├── models/
│       │   ├── user.py          ← User model
│       │   ├── role.py          ← Role models
│       │   └── meeting.py       ← Meeting model
│       ├── schemas/
│       │   ├── auth.py          ← Auth schemas
│       │   └── meeting.py       ← Meeting schemas
│       └── services/
│           ├── auth_service.py  ← Dummy users
│           └── hr_auth_service.py ← HR validation
│
└── frontend/
    └── src/
        ├── components/
        │   ├── auth/
        │   │   └── LoginForm.jsx
        │   ├── common/
        │   │   └── RoleGuard.jsx
        │   ├── dashboard/
        │   │   └── Dashboard.jsx
        │   └── meetings/
        │       ├── MeetingList.jsx
        │       ├── MeetingDetail.jsx
        │       └── CreateMeeting.jsx
        ├── contexts/
        │   └── AuthContext.jsx
        ├── services/
        │   └── api.js
        └── App.jsx
```

---

## Performance Considerations

### Frontend
- Component-level state management
- Lazy loading (future)
- Memoization (future)
- Pagination support ready

### Backend
- Database indexing on key fields
- Query optimization with SQLAlchemy
- JWT token caching
- Connection pooling

### Database
- Indexed columns: meeting_date, status, created_at
- Foreign key constraints
- Cascade delete operations

---

## Scalability

### Current Capacity
- Supports multiple concurrent users
- JWT stateless authentication
- Database connection pooling
- RESTful API design

### Future Enhancements
- Redis for session management
- WebSocket for real-time updates
- CDN for static assets
- Load balancing
- Microservices architecture

---

This architecture provides a solid foundation for Phase 9.3 and beyond!

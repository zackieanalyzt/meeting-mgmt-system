# Meeting Management System - Frontend

## Phase 9.1: Auth Flow Integration

React + Vite frontend with JWT authentication.

## Setup & Run

```bash
cd frontend
npm install
npm run dev
```

Frontend will run at: http://localhost:5173

## Test Login

Use these dummy credentials (created by backend on startup):

- **Admin**: username: `admin`, password: (any password - HR auth)
- **Group Admin**: username: `group_admin`, password: (any password - HR auth)
- **User**: username: `user1`, password: (any password - HR auth)

## Structure

```
src/
├── components/
│   ├── auth/LoginForm.jsx          # Login form with JWT
│   ├── dashboard/Dashboard.jsx     # Protected dashboard
│   └── meetings/
│       ├── MeetingList.jsx         # List all meetings
│       └── MeetingDetail.jsx       # Meeting details
├── contexts/
│   └── AuthContext.jsx             # Global auth state
├── services/
│   └── api.js                      # Axios with JWT interceptor
├── App.jsx                         # Routes & protected routes
└── main.jsx                        # Entry point
```

## Auth Flow

1. User enters credentials in LoginForm
2. POST to `/api/v1/auth/login` with FormData
3. Backend returns JWT token + user data
4. Token saved to localStorage
5. AuthContext updates global state
6. Redirect to Dashboard
7. All API calls include `Authorization: Bearer <token>` header

## API Endpoints Used

- `POST /api/v1/auth/login` - Login with username/password
- `GET /api/v1/meetings` - List meetings (protected)
- `GET /api/v1/meetings/{id}` - Meeting details (protected)

## Notes

- No UI styling yet (functional only)
- JWT token auto-injected via axios interceptor
- Protected routes redirect to login if not authenticated
- Token stored in localStorage

# Meeting Management System

ระบบจัดการวาระและรายงานการประชุม v3.3

## Tech Stack
- Backend: FastAPI (Python 3.11)
- Frontend: Vue.js 3 + Vite + TailwindCSS
- Database: PostgreSQL 17 + MariaDB 11

## Quick Start
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Docker
```bash
docker-compose up -d
```
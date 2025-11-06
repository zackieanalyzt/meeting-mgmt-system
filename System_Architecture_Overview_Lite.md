ภาพรวมสถาปัตยกรรมระบบ Meeting Management System
1️⃣ จุดเริ่มต้นของระบบ
Backend (FastAPI):

เริ่มจาก backend/app/main.py → สร้าง FastAPI app
โหลด api/v1/api.py → รวม endpoints ทั้งหมด
เปิดใช้ CORS middleware และ JWT authentication
Frontend (Vue 3):

เริ่มจาก frontend/src/main.js → สร้าง Vue app + Pinia + Router
App.vue → แสดง Navbar และ router-view
router/index.js → ตรวจสอบ token ก่อนเข้าหน้า (auth guard)
2️⃣ บทบาทของผู้ใช้
| บทบาท | สิทธิ์การเข้าถึง | |--------|------------------| | Admin ใหญ่ | ทุกฟีเจอร์ + สร้าง/ปิดการประชุม + อนุมัติวาระ + จัดการรายงาน | | Admin กลุ่มงาน | เพิ่ม/แก้ไขวาระ + อัปโหลดไฟล์ + ดูรายงาน (ก่อนปิดประชุม) | | ผู้ใช้ทั่วไป | ดูวาระประชุม + ค้นหารายงาน (read-only) |

การตรวจสอบสิทธิ์ผ่าน core/rbac.py และ JWT token validation

3️⃣ เส้นทางการทำงานของข้อมูล
Login Flow: Login.vue → api/index.js → endpoints/auth.py → core/auth.py → JWT token → localStorage

Data CRUD: Views/*.vue → axios API calls → endpoints/*.py → core/rbac.py (ตรวจสิทธิ์) → models/*.py → PostgreSQL

Key Files:

core/auth.py - JWT management
core/rbac.py - Role permissions
models/meeting.py - Database schema
api/index.js - Frontend API client
4️⃣ โครงสร้างโฟลเดอร์หลัก
Backend (backend/app/):

models/ - SQLAlchemy ORM (users, meetings, agendas)
api/v1/endpoints/ - REST API routes
core/ - Authentication, RBAC, database config
schemas/ - Pydantic request/response models
Frontend (frontend/src/):

views/ - หน้าเว็บหลัก (Login, Dashboard, CurrentMeeting)
components/ - ส่วนประกอบ UI (Navbar)
router/ - Route definitions + auth guards
api/ - Axios HTTP client configuration
Database & Config:

alembic/ - Database migrations
docker-compose.yml - Services orchestration
.env - Environment variables
5️⃣ การทำงานโดยสรุป (Summary Flow)
Login: ผู้ใช้กรอก username/password → FastAPI ตรวจสอบ → สร้าง JWT token
Authorization: Frontend ส่ง token ใน header → Backend verify → ตรวจสอบ role
Dashboard: แสดงข้อมูลตามสิทธิ์ → เรียก API หลายตัว → รวมข้อมูลแสดงผล
CRUD Operations: Vue components → Axios → FastAPI endpoints → SQLAlchemy → PostgreSQL
File Management: Upload ผ่าน multipart/form-data → บันทึกใน /uploads/ directory
Tech Stack: Vue 3 + TailwindCSS → FastAPI + JWT → SQLAlchemy → PostgreSQL + MariaDB

6️⃣ สรุปประโยชน์ของระบบ
ระบบนี้ถูกออกแบบสำหรับโรงพยาบาลลี้ เพื่อจัดการวาระและรายงานการประชุมแบบรวมศูนย์ ใช้งานภายในเครือข่าย LAN/VPN อย่างปลอดภัย ด้วยระบบ Role-based Access Control ช่วยลดภาระงานเอกสาร รองรับการค้นหาข้อมูลย้อนหลัง และการอัปโหลดไฟล์ประกอบวาระ พร้อมระบบสำรองข้อมูลอัตโนมัติ

เทคโนโลジี: Full-stack modern web application ใช้ Docker สำหรับ deployment และ Alembic สำหรับ database migration
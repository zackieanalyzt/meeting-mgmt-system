# ระบบจัดการวาระและรายงานการประชุม (Meeting Management System)
**Version:** 3.3  
**สถานะ:** Stable  
**จัดทำโดย:** กลุ่มงานสุขภาพดิจิทัล โรงพยาบาลลี้  
**ประเภทเอกสาร:** Master Specification  
**ครอบคลุม:** Conceptual → Logical → Physical → PRD → Tech Stack  

---

## 1. แนวคิดหลักของระบบ
เจ้าหน้าที่แต่ละกลุ่มงานจะเข้าสู่ระบบ (Login) เพื่อดูวาระการประชุมครั้งปัจจุบัน (Current Meeting Agenda)  
และรายงานการประชุมครั้งที่ผ่านมา (Meeting Report History) หากกลุ่มงานของตนมีวาระที่จะนำเสนอ  
สามารถอัปโหลดเอกสารประกอบได้ เช่น PDF, DOCX, XLSX, PNG, JPEG, TXT เป็นต้น

---

## 2. Requirement เบื้องต้น
1. เจ้าหน้าที่ทุกกลุ่มงานสามารถเข้าดูรายงานการประชุมได้  
2. หากมีเรื่องเสนอ สามารถเพิ่มเรื่องใหม่ได้ไม่จำกัด พร้อมแนบไฟล์ประกอบ  
3. ระบุประเภทของเรื่องได้ เช่น เพื่อทราบ / เพื่อพิจารณา / เพื่อสั่งการ  
4. ดูรายงานการประชุมย้อนหลังได้ทุกครั้ง  
5. ค้นหารายงานการประชุมด้วยคำ (FreeText Search) จากทุกการประชุมได้  
6. ใช้งานเฉพาะภายในเครือข่ายของหน่วยงาน (LAN / VPN)  
7. แก้ไขหรือลบเอกสารได้จนกว่าจะปิดการประชุมนั้น ๆ  

---

## 3. บทบาทผู้ใช้ (User Roles)
| บทบาท | สิทธิ์หลัก |
|--------|-------------|
| Admin ใหญ่ | สร้าง/จัดการรอบการประชุม ตรวจสอบ อนุมัติ ปิดการประชุม ดู/ค้นรายงานทั้งหมด |
| Admin กลุ่มงาน | เสนอเรื่องเข้าวาระ อัปโหลด/แก้ไขไฟล์ก่อนปิดประชุม ดู/ค้นรายงานได้ |
| ผู้ใช้ทั่วไป | เข้าดูวาระประชุม ดูรายงานย้อนหลัง และค้นหารายงานได้ |

---

## 4. System Flow (Vertical Role-Based)
```mermaid
flowchart TB
subgraph R1["Admin ใหญ่"]
    A1["สร้าง/แก้ไขรอบการประชุม"]
    A2["ตรวจสอบและอนุมัติวาระ"]
    A3["จัดการรายงานการประชุม"]
    A4["ปิดการประชุม"]
    A5["ดู/ค้นรายงานย้อนหลัง"]
end

subgraph R2["Admin กลุ่มงาน"]
    B1["เสนอเรื่องเข้าวาระ"]
    B2["อัปโหลดไฟล์ประกอบ"]
    B3["แก้ไข/ลบไฟล์ได้ก่อนปิดประชุม"]
    B4["ดู/ค้นรายงานย้อนหลัง"]
end

subgraph R3["ผู้ใช้ทั่วไป"]
    C1["เข้าสู่ระบบ"]
    C2["ดูวาระประชุมปัจจุบัน"]
    C3["ดูรายงานการประชุมย้อนหลัง"]
    C4["ค้นหารายงานการประชุม"]
end
```

---

## 5. Use Case Diagram
```mermaid
flowchart TB
actorAdminMain["Admin ใหญ่"]
actorAdminGroup["Admin กลุ่มงาน"]
actorUser["ผู้ใช้ทั่วไป"]

subgraph SYSTEM["ระบบจัดการวาระและรายงานการประชุม"]
    UC_Create["สร้าง/แก้ไขรอบประชุม"]
    UC_Approve["อนุมัติวาระ"]
    UC_Add["เสนอเรื่องเข้าวาระ"]
    UC_Upload["อัปโหลดไฟล์"]
    UC_Edit["แก้ไข/ลบไฟล์"]
    UC_Report["จัดการรายงาน"]
    UC_View["ดูวาระและรายงาน"]
    UC_Search["ค้นหารายงาน"]
    UC_Close["ปิดการประชุม"]
end

actorAdminMain --> UC_Create
actorAdminMain --> UC_Approve
actorAdminMain --> UC_Add
actorAdminMain --> UC_Upload
actorAdminMain --> UC_Edit
actorAdminMain --> UC_Report
actorAdminMain --> UC_Close
actorAdminMain --> UC_View
actorAdminMain --> UC_Search

actorAdminGroup --> UC_Add
actorAdminGroup --> UC_Upload
actorAdminGroup --> UC_Edit
actorAdminGroup --> UC_View
actorAdminGroup --> UC_Search

actorUser --> UC_View
actorUser --> UC_Search
```

---

## 6. ER Diagram (v3.3)
```mermaid
erDiagram
    USERS {
        int user_id PK
        varchar username
        varchar fullname
        varchar department
        varchar email
    }
    ROLES {
        int role_id PK
        varchar role_name
    }
    USER_ROLES {
        int user_id FK
        int role_id FK
        timestamp assigned_at
    }
    MEETINGS {
        int meeting_id PK
        varchar meeting_name
        date meeting_date
        varchar meeting_time
        varchar location
        varchar status
    }
    AGENDAS {
        int agenda_id PK
        int meeting_id FK
        int user_id FK
        varchar agenda_title
        text agenda_detail
        varchar agenda_type
    }
    FILES {
        int file_id PK
        int agenda_id FK
        varchar file_name
        varchar file_path
        varchar file_type
        int uploaded_by
    }
    REPORTS {
        int report_id PK
        int meeting_id FK
        varchar report_title
        text report_summary
        varchar file_path
    }
    SEARCH_LOG {
        int log_id PK
        int user_id FK
        varchar search_text
        varchar search_target
        timestamp search_time
    }

    USERS ||--o{ USER_ROLES : "has"
    ROLES ||--o{ USER_ROLES : "assigned"
    USERS ||--o{ AGENDAS : "created"
    MEETINGS ||--o{ AGENDAS : "contains"
    AGENDAS ||--o{ FILES : "attached"
    MEETINGS ||--o{ REPORTS : "documented"
    USERS ||--o{ SEARCH_LOG : "performed"
```

---

## 7. เอกสาร PRD (Product Requirement Document)
รวมเนื้อหา PRD v1.0 ไว้เต็มฉบับ  
- ระบบตรวจสอบ login จาก MariaDB.users (MD5)  
- โหลดสิทธิ์จาก PostgreSQL.user_roles  
- แสดง Dashboard การประชุมล่าสุด  
- เสนอเรื่องเข้าวาระ, แนบไฟล์, แก้ไข/ลบก่อนปิดประชุม  
- จัดการรายงาน, ปิดรอบประชุม, ค้นหาแบบ FreeText  
- มี Search Log เก็บพฤติกรรมการค้นหาและ login  

**Non-Functional Requirement:**  
- รองรับ 50 concurrent users  
- read-only DB connections  
- รองรับ offline mode (MariaDB down ชั่วคราว)  
- Logging ครบทุกกิจกรรม  
- สำรองข้อมูลอัตโนมัติผ่าน cron  

**Roles & Permissions:**  
| กิจกรรม | Admin ใหญ่ | Admin กลุ่มงาน | ผู้ใช้ทั่วไป |
|----------|-------------|-----------------|---------------|
| เข้าสู่ระบบ | ✅ | ✅ | ✅ |
| ดูวาระประชุม | ✅ | ✅ | ✅ |
| เสนอเรื่อง | ✅ | ✅ | ❌ |
| อัปโหลดไฟล์ | ✅ | ✅ | ❌ |
| แก้ไข/ลบ | ✅ | ✅ (ก่อนปิด) | ❌ |
| ปิดรอบประชุม | ✅ | ❌ | ❌ |
| จัดการรายงาน | ✅ | ❌ | ❌ |
| ค้นหา | ✅ | ✅ | ✅ |

---

## 8. Tech Stack (ฉบับเต็ม)
**Backend:** FastAPI (Python 3.11), SQLAlchemy, Uvicorn, psycopg2, pymysql  
**Frontend:** Vue.js 3 + TailwindCSS + Axios  
**Database:** PostgreSQL 17 (หลัก), MariaDB 11 (Auth)  
**Deployment:** Docker Compose / Physical Server  
**Security:** MD5 auth check, HTTPS (Nginx), RBAC Middleware  
**Structure:** models / routes / services / schemas / utils  
**API Prefix:** `/api/v1/`  
**Testing:** pytest, flake8  
**Backup:** pg_dump + cron job  
**Volume Path:** `/uploads/<year>/<meeting_id>/`  

---

## 9. การติดตั้งระบบบนเครื่องจริง
1. ติดตั้ง PostgreSQL และ MariaDB  
2. ตั้งฐานข้อมูล meeting_mgmt / authdb  
3. ติดตั้ง FastAPI และ dependencies  
4. รัน backend ด้วย Uvicorn  
5. ติดตั้ง Vue.js และ build frontend  
6. ตั้งค่า Nginx reverse proxy  
7. ทดสอบระบบผ่าน LAN  

---

## 10. สรุป
ระบบนี้ออกแบบเพื่อให้หน่วยงานสามารถบริหารวาระการประชุมได้แบบรวมศูนย์  
รองรับการอัปโหลดไฟล์ การบันทึกการประชุมย้อนหลัง และการค้นหาด้วยคำสำคัญ  
ใช้เทคโนโลยีโอเพนซอร์สทั้งหมดและพร้อมต่อยอดสู่ Container Deployment ได้ในอนาคต

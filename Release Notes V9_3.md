# 🧾 RELEASE NOTES — Meeting Management System v9.3

**Version:** v9.3
**Phase:** Group Admin Functional Foundation
**Date:** 2025-11-10
**Author:** Digital Health Dev Team

---

## 🚀 Overview

This version introduces the foundation for **Agenda Objectives Management**, enabling agenda items to have clear and structured purposes (objectives) — a key requirement before implementing group admin features for creating and managing meetings.

---

## ✨ New Features

### 1. **Agenda Objectives Table** (`agenda_objectives`)

Stores the defined purposes or goals for agenda items.

**Schema:**

* `objective_id` — Primary key (int)
* `objective_name` — Short name of the objective (varchar)
* `description` — Detailed purpose
* `created_at` — Timestamp (default current time)

**Seed Data:**

| objective_id | objective_name                     | description                                       |
| ------------ | ---------------------------------- | ------------------------------------------------- |
| 1            | เพื่อทราบ                          | จัดประชุมเพื่อแจ้งข้อมูลที่สำคัญให้รับทราบ        |
| 2            | เพื่อทราบและพิจารณามอบหมาย/สั่งการ | ใช้เพื่อให้คณะกรรมการพิจารณาและสั่งการต่อยอด      |
| 3            | เพื่อพิจารณาอนุมัติ/อนุญาต         | สำหรับเรื่องที่ต้องอนุมัติหรืออนุญาตจากผู้มีอำนาจ |

---

### 2. **Mapping Table: `agenda_objective_map`**

A many-to-many relationship table linking `agendas` and `agenda_objectives`.

**Columns:**

* `agenda_id` → FK → `agendas.agenda_id`
* `objective_id` → FK → `agenda_objectives.objective_id`

This structure allows each agenda item to have multiple purposes.

---

## 🧩 Model Updates

### `app/models/agenda.py`

* Added relationship between `Agenda` ↔ `AgendaObjective`
* Updated indices to optimize queries

```python
objectives = relationship(
    "AgendaObjective",
    secondary="agenda_objective_map",
    backref="agendas"
)
```

### `app/models/__init__.py`

Ensures all related models are imported at startup to avoid `NameError`.

```python
from app.models.agenda_objective import AgendaObjective
from app.models.agenda_objective_map import AgendaObjectiveMap
```

---

## 🌐 API Enhancements

### `/api/v1/agenda-objectives/`

* `GET`: Retrieve all defined objectives
* `POST`: Create a new objective (Admin only)

**Example Response:**

```json
[
  {"objective_id": 1, "objective_name": "เพื่อทราบ", "description": "แจ้งข้อมูลสำคัญ"},
  {"objective_id": 2, "objective_name": "เพื่อทราบและพิจารณามอบหมาย/สั่งการ"},
  {"objective_id": 3, "objective_name": "เพื่อพิจารณาอนุมัติ/อนุญาต"}
]
```

---

## ✅ Testing Summary

| Test                                | Result                  |
| ----------------------------------- | ----------------------- |
| ORM relationship Agenda ↔ Objective | ✅ Passed                |
| API `/api/v1/agenda-objectives/`    | ✅ Working               |
| System startup                      | ✅ No ORM mapping errors |

---

## 🧠 Technical Context

This version sets up backend logic required for:

* Creating meetings and attaching agenda items
* Associating each agenda with one or more objectives
* Uploading documents for each agenda item (planned in v9.3.1)

---

## 🔮 Next Phase (v9.3.1 Preview)

### Focus: **Group Admin Functional Module**

1. Enable **Admin Group** to create meetings (meeting title, date, time, venue)
2. Allow adding agenda items with multiple objectives
3. Implement file attachments (≤10 files, ≤10MB each, allowed: `.pdf`, `.doc`, `.jpg`, `.png`, `.md`)
4. Extend API endpoints for agenda creation and linking objectives

---

## 📦 Deployment Notes

* Requires `agenda_objectives` and `agenda_objective_map` tables to be migrated/created.
* Confirm existing migrations are up-to-date before applying new schema.
* Backend tested and verified on PostgreSQL (v16) and FastAPI (v0.115+).

---

**Status:** ✅ Stable
**Next:** Implement functional UI integration for Group Admin module in v9.3.1.
# Implementation Plan: Student Management System

**Branch**: `001-student-management-system` | **Date**: 2026-10-11 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-student-management-system/spec.md`

---

## Summary

Build a mini full-stack Student Management System: a FastAPI backend exposing five CRUD
endpoints for student records, and a Streamlit frontend with five matching sections. All
input is validated by Pydantic. Storage uses a local `backend/data.json` file (seeded from
root `data.json`). The backend is split into `schema.py` / `utils.py` / `routes.py` /
`backend/api/main.py`; the frontend lives in `frontend/app.py`. A thin root `main.py`
re-exports `app` so `uvicorn main:app --reload` still works unchanged.

---

## Technical Context

**Language/Version**: Python 3.10+

**Primary Dependencies**:
- Backend: FastAPI 0.110+, Uvicorn 0.29+, Pydantic v2 with `email-validator`
- Frontend: Streamlit 1.32+, `requests`
- Test: pytest, `httpx` (FastAPI `TestClient` transport)
- Display: pandas (for the dataframe table on the View page)

**Storage**: `backend/data.json` — JSON file loaded into a Python dict at startup. Seeded
from root `data.json` if `backend/data.json` doesn't exist. Written back on every mutating
operation. No external database.

**Testing**: pytest + FastAPI `TestClient`. One test module per endpoint group; one module
for validation rules.

**Target Platform**: Desktop browser (Streamlit UI), localhost (FastAPI server). macOS/Linux.

**Project Type**: Full-stack web application — single-machine backend API + browser frontend.

**Performance Goals**: All API responses under 200 ms on localhost (trivially met with
in-memory storage).

**Constraints**: No external database server. Dependencies limited to the set listed above
plus their transitive dependencies. Both run commands must work unchanged from the project
root.

**Scale/Scope**: Single coaching institute, single staff user, tens to low hundreds of
student records.

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Assignment-Defined Scope | ✅ PASS | Exactly 5 endpoints, 5 fields, 5 Streamlit sections planned. Bonus features deferred. |
| II. Validated Data Contract | ✅ PASS | Pydantic model with `age > 17`, `EmailStr`, non-empty name validates all input. Duplicate ID → 409, missing ID → 404. PUT does not allow ID change. |
| III. API-First Separation | ✅ PASS | Streamlit calls FastAPI over HTTP only. Backend URL configurable via constant in `app.py`. Error responses surfaced to user. |
| IV. Simplicity | ✅ PASS | Root `main.py` re-exports `app`; `frontend/app.py` is the Streamlit entry. `backend/api/` split into schema/utils/routes/main — no ORM, no repository pattern. |
| V. Verified Behavior | ✅ PASS | pytest suite planned for every endpoint success path and all documented error cases. |

**No violations — no Complexity Tracking entries needed.**

---

## Project Structure

### Documentation (this feature)

```text
specs/001-student-management-system/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   └── student-api.md   # Phase 1 output
└── tasks.md             # Phase 2 output (created by /speckit-tasks)
```

### Source Code (repository root)

```text
studen_management/               ← project root (working directory)
├── main.py                      ← thin entry: `from backend.api.main import app`
│                                   (uvicorn main:app --reload works unchanged)
├── data.json                    ← seed data (existing sample_data.json content)
├── requirements.txt             ← pinned dependencies
├── README.md
│
├── backend/
│   ├── __init__.py              ← empty, makes backend a package
│   ├── data.json                ← live data store (loaded + saved by utils.py)
│   └── api/
│       ├── __init__.py          ← empty, makes api a package
│       ├── main.py              ← creates app = FastAPI(), registers router
│       ├── schema.py            ← Student Pydantic model (all validation rules)
│       ├── routes.py            ← all 5 route handlers (APIRouter)
│       └── utils.py             ← load_data(), save_data(), in-memory store dict
│
├── frontend/
│   └── app.py                   ← Streamlit UI (streamlit run frontend/app.py)
│
└── tests/
    ├── conftest.py
    ├── test_add_student.py
    ├── test_get_students.py
    ├── test_get_student_by_id.py
    ├── test_update_student.py
    └── test_delete_student.py
```

**Structure Decision**: Layered layout matching the project image. The backend is split into
four focused modules (`schema`, `utils`, `routes`, `main`) inside `backend/api/`. The
frontend is isolated in `frontend/`. Root `main.py` re-exports `app` so the assignment's
`uvicorn main:app --reload` command works without change.

**Run command note**: The Streamlit command becomes `streamlit run frontend/app.py`
(differs from the assignment brief's `streamlit run app.py` because `app.py` moved into
`frontend/`). This is the only deviation — it follows the image structure the user chose.

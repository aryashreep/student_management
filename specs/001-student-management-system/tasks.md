# Tasks: Student Management System

**Input**: Design documents from `specs/001-student-management-system/`

**Prerequisites**: plan.md ✅ | spec.md ✅ | research.md ✅ | data-model.md ✅ | contracts/ ✅ | quickstart.md ✅

**Tests**: Included — required by Constitution Principle V ("Every backend endpoint MUST have
automated tests for its success path and its documented error cases. Every validation rule MUST
have at least one test that rejects bad input.")

**Organization**: Tasks grouped by user story (P1→P5) to enable independent implementation and
testing of each CRUD operation.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (US1–US5)

## Path Conventions

```
main.py                      ← thin re-export (root, keeps uvicorn command unchanged)
backend/__init__.py
backend/api/__init__.py
backend/api/schema.py        ← Student Pydantic model
backend/api/utils.py         ← data store + CRUD helpers
backend/api/routes.py        ← all 5 route handlers
backend/api/main.py          ← FastAPI app instance
backend/data.json            ← live data store
data.json                    ← seed data (existing file)
frontend/app.py              ← Streamlit UI  (streamlit run frontend/app.py)
tests/conftest.py
tests/test_*.py
requirements.txt
```

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project skeleton, package init files, dependencies, and test infrastructure.
No user story work until this phase is complete.

- [x] T001 Create `requirements.txt` in project root listing: `fastapi`, `"uvicorn[standard]"`, `"pydantic[email]"`, `streamlit`, `requests`, `pandas`, `pytest`, `httpx`
- [x] T002 [P] Create `backend/__init__.py` and `backend/api/__init__.py` as empty files so Python treats both as packages (required for `from backend.api.main import app` to work)
- [x] T003 [P] Create `tests/conftest.py` with (a) a `client` fixture that imports `app` from `backend.api.main`, wraps it in FastAPI `TestClient`, and (b) a `reset_store` autouse fixture that clears `utils.students` dict and reloads seed records from `data.json` before each test

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core backend modules and frontend skeleton that EVERY user story depends on.
No user story work can begin until this phase is complete.

**⚠️ CRITICAL**: All user story phases depend on this phase being done first.

- [x] T004 Create `backend/api/schema.py`: import Pydantic `BaseModel`, `Field`, `EmailStr`, `Annotated`; define `class Student(BaseModel)` with fields: `id: int`, `name: Annotated[str, Field(min_length=1)]` (rejects empty and whitespace-only), `age: Annotated[int, Field(gt=17)]` (rejects age ≤ 17), `course: str`, `email: EmailStr` (rejects malformed email)
- [x] T005 Create `backend/api/utils.py`: define module-level `students: dict[int, dict] = {}`; implement `load_data(path: str) -> None` that reads a JSON array from the given path, converts each record to `{id: record}` entries in `students`; implement `save_data(path: str) -> None` that writes `list(students.values())` back to the JSON file; define `DATA_FILE = "backend/data.json"` and `SEED_FILE = "data.json"`
- [x] T006 Create `backend/api/routes.py`: import `APIRouter` from FastAPI and `Student` from `schema`, `students` + helpers from `utils`; create `router = APIRouter()`; add stub comments for each of the 5 routes (no implementation yet — filled in per user story)
- [x] T007 Create `backend/api/main.py`: create `app = FastAPI(title="Student Management System")`; at startup (lifespan or `@app.on_event("startup")`) call `load_data(DATA_FILE)` if `backend/data.json` exists, else call `load_data(SEED_FILE)` to seed from root `data.json`; include `router` from `routes.py`
- [x] T008 Create root `main.py` as a single line: `from backend.api.main import app  # noqa: F401` so that `uvicorn main:app --reload` works from the project root
- [x] T009 [P] Create `frontend/app.py`: set `BACKEND_URL = "http://localhost:8000"` constant at the top; add Streamlit sidebar radio selector with exactly 5 options: `"Add Student"`, `"View Students"`, `"Search Student"`, `"Update Student"`, `"Delete Student"`; render `st.info("Select a section from the sidebar")` as default placeholder for each (establishes navigation shell)

**Checkpoint**: `uvicorn main:app --reload` starts without errors and `http://localhost:8000/docs` loads. `streamlit run frontend/app.py` shows sidebar with 5 options.

---

## Phase 3: User Story 1 — Add Student (Priority: P1) 🎯 MVP

**Goal**: Staff can register a new valid student; invalid input is rejected with a clear message.

**Independent Test**: Add page works in isolation. Success shows the new student in GET /students.
Validation failures return 422 (age, email, name) or 409 (duplicate ID).

### Tests for User Story 1 ⚠️ Write first — verify they FAIL before implementing T011

- [x] T010 [P] [US1] Write `tests/test_add_student.py`: test `POST /students` with valid body → 201 and returned student matches input; test POST with duplicate `id` → 409; test POST where `age=17` → 422; test POST where `email="notvalid"` → 422; test POST where `name=""` → 422; test POST where `name="   "` (whitespace) → 422

### Implementation for User Story 1

- [x] T011 [US1] Add `POST /students` route in `backend/api/routes.py`: check `body.id` not in `students` (raise `HTTPException(status_code=409, detail="Student with this ID already exists")`); add record to `students`; call `save_data(DATA_FILE)`; return record with `status_code=201`
- [x] T012 [US1] Implement Add Student section in `frontend/app.py`: under `"Add Student"` branch render `st.number_input("ID", min_value=1, step=1)`, `st.text_input("Name")`, `st.number_input("Age", min_value=1, step=1)`, `st.text_input("Course")`, `st.text_input("Email")`; on submit button click, wrap `requests.post(BACKEND_URL + "/students", json=payload)` in `try/except requests.exceptions.ConnectionError`; show `st.success("Student added!")` on 201, `st.error(response.json()["detail"])` on 409/422, `st.error("Cannot reach backend — is uvicorn running?")` on connection failure

**Checkpoint**: POST /students happy path and all four rejection types work. Add page confirms success and shows errors. All T010 tests pass.

---

## Phase 4: User Story 2 — View All Students (Priority: P2)

**Goal**: Staff see every enrolled student in a table with all five columns.

**Independent Test**: GET /students returns full list; View page shows a DataFrame; empty store shows a friendly message.

### Tests for User Story 2 ⚠️ Write first — verify they FAIL before implementing T014

- [x] T013 [P] [US2] Write `tests/test_get_students.py`: test `GET /students` with seeded data → 200 and response is a list of 4 records with correct fields; test `GET /students` when store is empty → 200 and response is `[]`

### Implementation for User Story 2

- [x] T014 [US2] Add `GET /students` route in `backend/api/routes.py`: return `list(students.values())` with status 200
- [x] T015 [US2] Implement View Students section in `frontend/app.py`: under `"View Students"` branch, wrap `requests.get(BACKEND_URL + "/students")` in try/except; on success display `st.dataframe(pd.DataFrame(data))` if list non-empty, else `st.info("No students enrolled yet.")`; on connection failure show `st.error("Cannot reach backend — is uvicorn running?")`

**Checkpoint**: GET /students returns all seeded records. View page shows DataFrame with id/name/age/course/email columns. All T013 tests pass.

---

## Phase 5: User Story 3 — Search Student by ID (Priority: P3)

**Goal**: Staff retrieve one student's full record by entering their ID; an unknown ID shows a clear not-found message.

**Independent Test**: GET /students/{id} with a known ID returns exactly that student; unknown ID returns 404.

### Tests for User Story 3 ⚠️ Write first — verify they FAIL before implementing T017

- [x] T016 [P] [US3] Write `tests/test_get_student_by_id.py`: test `GET /students/1` (seeded) → 200 and returned record has `id=1` and all fields correct; test `GET /students/999` → 404 with `detail` field in response body

### Implementation for User Story 3

- [x] T017 [US3] Add `GET /students/{student_id}` route in `backend/api/routes.py`: if `student_id` not in `students` raise `HTTPException(status_code=404, detail="Student not found")`; else return `students[student_id]`
- [x] T018 [US3] Implement Search Student section in `frontend/app.py`: under `"Search Student"` branch render `st.number_input("Student ID", min_value=1, step=1)`; on submit button click wrap `requests.get(BACKEND_URL + f"/students/{sid}")` in try/except; on 200 display each field with `st.write`; on 404 show `st.warning("Student not found")`; on connection failure show `st.error("Cannot reach backend — is uvicorn running?")`

**Checkpoint**: Known IDs return the correct student. Unknown IDs return a friendly not-found message. All T016 tests pass.

---

## Phase 6: User Story 4 — Update Student Details (Priority: P4)

**Goal**: Staff correct a student's name/age/course/email using the student's ID; the ID cannot be changed.

**Independent Test**: PUT /students/{id} returns the modified record; missing ID returns 404; invalid fields return 422.

### Tests for User Story 4 ⚠️ Write first — verify they FAIL before implementing T020

- [x] T019 [P] [US4] Write `tests/test_update_student.py`: test `PUT /students/1` with valid updated fields → 200 and returned record reflects changes; test that path `id=1` is used as authoritative even if body sends a different id; test `PUT /students/999` → 404; test `PUT /students/1` with `age=15` → 422; test `PUT /students/1` with `email="bad"` → 422

### Implementation for User Story 4

- [x] T020 [US4] Add `PUT /students/{student_id}` route in `backend/api/routes.py`: if `student_id` not in `students` raise `HTTPException(404, detail="Student not found")`; validate body via `Student` model (FastAPI returns 422 automatically); overwrite `students[student_id]` with updated fields using `student_id` from path as the authoritative id (ignore any `id` in the body); call `save_data(DATA_FILE)`; return updated record
- [x] T021 [US4] Implement Update Student section in `frontend/app.py`: under `"Update Student"` branch render `st.number_input("Student ID")`; on lookup button click, fetch current record via `GET /students/{sid}` and pre-fill text inputs with existing values; on save button click wrap `requests.put(BACKEND_URL + f"/students/{sid}", json=payload)` in try/except; show `st.success("Student updated!")` on 200, `st.error(detail)` on 404/422, `st.error("Cannot reach backend — is uvicorn running?")` on connection failure

**Checkpoint**: Updated fields immediately visible in View Students. All T019 tests pass.

---

## Phase 7: User Story 5 — Delete Student Record (Priority: P5)

**Goal**: Staff permanently remove a student record by ID; the record disappears immediately; a second delete shows not-found.

**Independent Test**: DELETE /students/{id} removes the record; student no longer appears in GET /students; second delete of same ID returns 404.

### Tests for User Story 5 ⚠️ Write first — verify they FAIL before implementing T023

- [x] T022 [P] [US5] Write `tests/test_delete_student.py`: test `DELETE /students/1` → 200 with body `{"message": "Student deleted successfully"}`; test subsequent `GET /students/1` → 404; test `DELETE /students/999` → 404

### Implementation for User Story 5

- [x] T023 [US5] Add `DELETE /students/{student_id}` route in `backend/api/routes.py`: if `student_id` not in `students` raise `HTTPException(404, detail="Student not found")`; delete `students[student_id]`; call `save_data(DATA_FILE)`; return `{"message": "Student deleted successfully"}`
- [x] T024 [US5] Implement Delete Student section in `frontend/app.py`: under `"Delete Student"` branch render `st.number_input("Student ID", min_value=1, step=1)`; on delete button click wrap `requests.delete(BACKEND_URL + f"/students/{sid}")` in try/except; show `st.success("Student deleted.")` on 200, `st.warning("Student not found.")` on 404, `st.error("Cannot reach backend — is uvicorn running?")` on connection failure

**Checkpoint**: Deleted student disappears from View Students immediately. Second delete shows not-found. All T022 tests pass.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, error-handling audit, and quality gates from the constitution.

- [x] T025 [P] Audit every `requests.*` call in `frontend/app.py` and confirm each is wrapped in `try/except requests.exceptions.ConnectionError` with the `st.error("Cannot reach backend — is uvicorn running?")` fallback (satisfies FR-011 and quickstart step 9)
- [x] T026 Run `pytest tests/ -v` from project root and confirm 0 failures across all five test modules (`test_add_student`, `test_get_students`, `test_get_student_by_id`, `test_update_student`, `test_delete_student`)
- [x] T027 Start backend with `uvicorn main:app --reload` from project root; open `http://localhost:8000/docs`; verify all 5 endpoints are listed with correct HTTP methods and paths
- [x] T028 Start frontend with `streamlit run frontend/app.py`; step through all 10 steps in `specs/001-student-management-system/quickstart.md` and confirm every expected outcome is met

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately.
- **Foundational (Phase 2)**: Depends on Phase 1. **BLOCKS all user stories.**
- **US1–US5 (Phases 3–7)**: All depend on Phase 2 completion; can proceed in priority order.
- **Polish (Phase 8)**: Depends on all user story phases (3–7) complete.

### User Story Dependencies

| Story | Depends on | Notes |
|-------|-----------|-------|
| US1 (Add)    | Phase 2 done | MVP — implement first |
| US2 (View)   | Phase 2 done | Depends on route stub in routes.py, not on US1 |
| US3 (Search) | Phase 2 done | Same |
| US4 (Update) | Phase 2 done | Same |
| US5 (Delete) | Phase 2 done | Same |

### Within Each User Story

1. Write test file first → run `pytest` → confirm tests FAIL (no route yet)
2. Add route to `backend/api/routes.py`
3. Add UI section to `frontend/app.py`
4. Re-run `pytest` → confirm tests PASS

### Parallel Opportunities

- T002 and T003 (different files) can run alongside T001.
- T004 → T005 → T006 → T007 → T008 are sequential (each builds on the previous in `backend/api/`).
- T009 (`frontend/app.py`) can run in parallel with T004–T008 (different directory).
- All test-writing tasks (T010, T013, T016, T019, T022) are different files — can run in parallel after Phase 2.

---

## Parallel Example: Foundation Phase

```bash
# Independent — run together:
Task T009: "Create frontend/app.py skeleton"      ← frontend/app.py
# Sequential — run in order:
Task T004: "Create backend/api/schema.py"
Task T005: "Create backend/api/utils.py"
Task T006: "Create backend/api/routes.py stub"
Task T007: "Create backend/api/main.py"
Task T008: "Create root main.py (one-liner)"
```

## Parallel Example: Test Files (after Phase 2 done)

```bash
Task T010: tests/test_add_student.py
Task T013: tests/test_get_students.py
Task T016: tests/test_get_student_by_id.py
Task T019: tests/test_update_student.py
Task T022: tests/test_delete_student.py
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete **Phase 1**: Setup (T001–T003)
2. Complete **Phase 2**: Foundational (T004–T009) — CRITICAL GATE
3. Complete **Phase 3**: Add Student (T010–T012)
4. **STOP and VALIDATE**: `pytest tests/test_add_student.py -v` + manual Add page test
5. Demo / show to instructor

### Incremental Delivery (Recommended)

1. Phase 1 + 2 → skeleton + both run commands work
2. Phase 3 (Add) → register students, all validation tested
3. Phase 4 (View) → see the list, empty-state works
4. Phase 5 (Search) → targeted lookup
5. Phase 6 (Update) → correct records
6. Phase 7 (Delete) → remove records
7. Phase 8 → full `pytest` pass + quickstart walkthrough

### Quality Gates (from constitution)

All five gates must pass before submission:

1. All 5 core endpoints match the API contract (`contracts/student-api.md`)
2. `pytest tests/ -v` → 0 failures
3. All 5 frontend sections work against a running backend
4. `uvicorn main:app --reload` starts cleanly
5. `streamlit run frontend/app.py` starts cleanly

Bonus features (course filter, dashboard) start **only after all 5 gates pass**.

---

## Notes

- `[P]` tasks work on different files — safe to run concurrently.
- `[USn]` label traces each task back to its user story in spec.md.
- All endpoint tasks go into `backend/api/routes.py`, not into `backend/api/main.py`.
- `save_data()` is called after every mutating operation (POST, PUT, DELETE) so data survives a restart.
- The `reset_store` fixture in `conftest.py` clears `utils.students` before each test — keeps tests independent.
- Commit after each Checkpoint to preserve working increments.

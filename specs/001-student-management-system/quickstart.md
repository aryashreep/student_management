# Quickstart Validation Guide: Student Management System

**Date**: 2026-10-11
**Purpose**: Step-by-step scenarios to prove the system works end-to-end after implementation.

---

## Prerequisites

```bash
# From the project root, install dependencies:
pip install fastapi uvicorn[standard] "pydantic[email]" streamlit requests pandas pytest httpx
```

`sample_data.json` is already in the project root and will be loaded automatically.

---

## Step 1 — Start the Backend

```bash
uvicorn main:app --reload
```

**Expected**: Server starts on `http://localhost:8000`. Open
`http://localhost:8000/docs` in a browser — you should see the FastAPI Swagger UI listing
5 endpoints.

---

## Step 2 — Start the Frontend (second terminal)

```bash
streamlit run app.py
```

**Expected**: Streamlit opens in the browser (typically `http://localhost:8501`). Five
navigation sections are visible: Add Student, View Students, Search Student, Update Student,
Delete Student.

---

## Step 3 — Smoke Test: View Students

1. Click **View Students**.
2. **Expected**: Table shows the 4 seeded students (Rahul, Priya, Aman, Sneha) with all 5
   columns (id, name, age, course, email).

---

## Step 4 — Add a Valid Student

1. Click **Add Student**.
2. Fill in: id=10, name="Alice", age=22, course="AI", email="alice@example.com".
3. Submit.
4. **Expected**: Success confirmation message. Switch to View Students — Alice appears in
   the table.

---

## Step 5 — Validation Rejections

Perform each sub-test from the Add Student page. Each MUST show an error message (not crash):

| Sub-test | Input | Expected message contains |
|----------|-------|--------------------------|
| Age too low | age=17 | age / greater than 17 |
| Invalid email | email="notvalid" | email |
| Empty name | name="" | name / empty |
| Duplicate ID | id=10 (already added) | already exists / duplicate |

---

## Step 6 — Search Student

1. Click **Search Student**.
2. Enter id=10.
3. **Expected**: Alice's full record is displayed.
4. Enter id=99.
5. **Expected**: "Not found" message (no crash).

---

## Step 7 — Update Student

1. Click **Update Student**.
2. Enter id=10, change course to "Data Science". Keep other fields the same.
3. Submit.
4. **Expected**: Confirmation of update. View Students shows Alice with course "Data Science".

---

## Step 8 — Delete Student

1. Click **Delete Student**.
2. Enter id=10 and confirm.
3. **Expected**: Deletion confirmation. View Students no longer shows id=10.
4. Try to delete id=10 again.
5. **Expected**: "Not found" message.

---

## Step 9 — Backend Down Test

1. Stop the backend (Ctrl-C in its terminal).
2. Try any action in the Streamlit frontend.
3. **Expected**: Friendly connection-error message. No unhandled Python exception shown.

---

## Step 10 — Run Automated Tests

```bash
pytest tests/ -v
```

**Expected**: All tests pass (0 failures). Test coverage includes every endpoint's success
path, 404/409 error paths, and every validation rule (age, email, name, duplicate ID).

---

## Artifacts Referenced

- Data model and field constraints: [data-model.md](data-model.md)
- Full HTTP contract (status codes, request/response shapes): [contracts/student-api.md](contracts/student-api.md)
- Constitution (principles and quality gates): [../../.specify/memory/constitution.md](../../.specify/memory/constitution.md)

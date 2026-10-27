<!--
Sync Impact Report
==================
Version change: (unversioned template) → 1.0.0
Rationale: Initial ratification. All placeholders replaced with project-specific content
derived from "Student Management System Assignm.txt".

Modified principles (template placeholder → new title):
- [PRINCIPLE_1_NAME] → I. Assignment-Defined Scope
- [PRINCIPLE_2_NAME] → II. Validated Data Contract
- [PRINCIPLE_3_NAME] → III. API-First Separation
- [PRINCIPLE_4_NAME] → IV. Simplicity
- [PRINCIPLE_5_NAME] → V. Verified Behavior

Added sections:
- Technology & Interface Constraints (was [SECTION_2_NAME])
- Development Workflow & Quality Gates (was [SECTION_3_NAME])

Removed sections: none

Rules added beyond the assignment brief (inferred, confirm or amend):
- Student IDs are unique; duplicate create → 409 Conflict.
- Missing student → 404 Not Found.
- The ID in the PUT path is authoritative; the ID is not changed by an update.
- No external database server; in-memory or JSON-file storage only.

Follow-up TODOs: none
-->

# Student Management System Constitution

## Core Principles

### I. Assignment-Defined Scope

The assignment brief is the source of truth for scope.

- The backend MUST expose exactly these five core endpoints: `POST /students`,
  `GET /students`, `GET /students/{student_id}`, `PUT /students/{student_id}`,
  `DELETE /students/{student_id}`.
- A student record MUST have exactly these fields: `id` (int), `name` (str), `age` (int),
  `course` (str), `email` (str).
- The frontend MUST provide five sections: Add, View, Search, Update, Delete.
- Bonus features (course filtering via `GET /students?course=<name>`, and a statistics
  dashboard) are OPTIONAL and MUST NOT be started until all core features work.
- Features not in the brief MUST NOT be added without amending this constitution or the spec.

Rationale: This is a graded assignment. Meeting the stated requirements completely matters
more than adding extras.

### II. Validated Data Contract

All input validation MUST be done with Pydantic models in the backend. The backend is the
only authority on what counts as valid data.

- `age` MUST be greater than 17.
- `email` MUST be a syntactically valid email address (for example, Pydantic `EmailStr`).
- `name` MUST NOT be empty or whitespace-only.
- Invalid input MUST be rejected with HTTP 422 and a message that names the failing field.
- `id` MUST be unique. Creating a duplicate ID MUST return 409 Conflict.
- Operations on an ID that does not exist MUST return 404 Not Found.
- On `PUT`, the `student_id` in the path is authoritative; an update MUST NOT change the ID.

Rationale: Rules enforced in one place cannot drift. Clear status codes let the frontend show
meaningful messages.

### III. API-First Separation

The Streamlit frontend MUST communicate with the data only through the FastAPI HTTP API.

- The frontend MUST NOT read or write the data store directly.
- The backend base URL MUST be configurable (default `http://localhost:8000`).
- The frontend MUST show backend error messages (404, 409, 422, connection failure) to the
  user, and MUST NOT crash on them.

Rationale: This keeps the two layers independent, which is the point of a full-stack exercise,
and lets each layer be tested on its own.

### IV. Simplicity

- The backend entrypoint MUST be `main.py` exposing `app`. The frontend entrypoint MUST be
  `app.py`.
- Storage MUST be in-memory or a local JSON file. An external database server MUST NOT be
  used. `sample_data.json` MAY be used to seed initial data.
- Dependencies SHOULD be limited to FastAPI, Uvicorn, Pydantic (with email support),
  Streamlit, an HTTP client (such as `requests`), pandas and pytest. Any other dependency
  needs a stated reason in the plan.
- Do not build abstractions (repositories, service layers, ORMs) unless the plan shows a
  concrete need for them.

Rationale: A small assignment is best served by code that is short and easy to read.

### V. Verified Behavior

- Every backend endpoint MUST have automated tests (pytest with FastAPI `TestClient`) for
  its success path and its documented error cases.
- Every validation rule in Principle II MUST have at least one test that rejects bad input.
- All tests MUST pass before a feature is considered done.
- Frontend behavior MUST be checked manually against both run commands before submission.

Rationale: Tests make it possible to show that the requirements are met, and to change code
without breaking it.

## Technology & Interface Constraints

- Language: Python 3.
- Backend: FastAPI, served by Uvicorn. Start command: `uvicorn main:app --reload`.
- Frontend: Streamlit. Start command: `streamlit run app.py`.
- The View page MUST display students as a table or dataframe.
- Requests and responses are JSON, using the field names from Principle I.
- Both run commands from the brief MUST work unchanged from the project root.

## Development Workflow & Quality Gates

- Work follows the Spec Kit flow: specify → (clarify) → plan → tasks → implement.
- Every plan MUST include a Constitution Check against Principles I–V. Any deviation MUST be
  recorded with a justification.
- Gates for completion:
  1. All five core endpoints behave as specified, including error codes.
  2. All tests pass.
  3. All five frontend sections work against a running backend.
  4. Both run commands start cleanly.
- Bonus work begins only after gates 1–4 pass.

## Governance

- This constitution overrides other practices for this project. Where a spec, plan or task
  conflicts with it, the constitution wins until it is amended.
- Amendments MUST be made by editing this file, updating the Sync Impact Report, and bumping
  the version.
- Versioning follows semantic versioning:
  - MAJOR: removing or redefining a principle.
  - MINOR: adding a principle or section, or materially expanding guidance.
  - PATCH: clarifications and wording fixes.
- Compliance is checked at the plan stage (Constitution Check) and at implementation review
  (the quality gates above).

**Version**: 1.0.0 | **Ratified**: 2026-10-11 | **Last Amended**: 2026-10-11

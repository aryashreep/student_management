# Research: Student Management System

**Date**: 2026-10-11
**Phase**: 0 — Resolves all NEEDS CLARIFICATION items from Technical Context

No NEEDS CLARIFICATION markers were present in the spec or plan template. The technology
choices are fully determined by the assignment brief and constitution. This file records the
rationale for each decision.

---

## Decision Log

### D-001: Storage Strategy

**Decision**: In-memory Python dict (`dict[int, dict]`) keyed by student `id`. Load
`sample_data.json` at FastAPI startup if the file exists.

**Rationale**: The assignment explicitly prohibits an external database server (constitution
Principle IV). An in-memory dict is the simplest structure that supports all five CRUD
operations with O(1) lookup by ID. Seeding from `sample_data.json` means the four example
students are available immediately on first run, satisfying the quickstart demo.

**Alternatives considered**:
- SQLite via `sqlite3` stdlib: More durable but adds setup complexity and contradicts the
  "simplicity" principle for this scope.
- JSON file as persistent store: Adds file I/O error handling; unnecessary for an assignment.
- TinyDB: Third-party dependency with no benefit over a plain dict for this scale.

---

### D-002: Pydantic Validation for Email

**Decision**: Use Pydantic v2 with `email-validator` installed (adds `EmailStr` support).

**Rationale**: The assignment requires email validation. `EmailStr` in Pydantic v2 provides
RFC-5322-compliant validation with a single field annotation. FastAPI returns a structured
422 response automatically when validation fails, satisfying FR-007 without extra code.

**Alternatives considered**:
- Manual regex in a `@validator`: More code, harder to maintain, easy to get wrong.
- `pydantic[email]` extra: Same package, just installed via `pip install pydantic[email]`
  or `email-validator` separately — functionally identical.

---

### D-003: Duplicate ID and Missing ID Handling

**Decision**: Return HTTP 409 Conflict for duplicate ID on create. Return HTTP 404 Not Found
for any operation on an unknown ID. These are checked in the route handlers before
modifying the data store.

**Rationale**: 409 is the correct semantic for a uniqueness conflict. 404 is the standard
for a missing resource. FastAPI's `HTTPException` is used to return both. This satisfies
FR-009 and FR-010.

**Alternatives considered**:
- Return 400 Bad Request for duplicates: Less precise; 409 is the correct code per RFC 9110.

---

### D-004: Frontend–Backend Communication

**Decision**: Streamlit calls FastAPI over `requests`. The backend base URL is a constant
at the top of `app.py` (default `http://localhost:8000`). All `requests` calls are wrapped
in try/except to catch `ConnectionError` and surface a user-friendly message (FR-011).

**Rationale**: The `requests` library is the simplest synchronous HTTP client compatible
with Streamlit's execution model. Streamlit reruns the entire script on each interaction,
so async clients (httpx async) would require extra scaffolding.

**Alternatives considered**:
- `httpx` (sync): Works equally well, but `requests` is more familiar and already listed
  in the constitution's preferred dependency set.
- Direct data-store access from the frontend: Violates constitution Principle III.

---

### D-005: Test Client

**Decision**: Use FastAPI's `TestClient` (backed by `httpx`) for all backend tests. No
running server required; tests import `app` from `main.py` directly.

**Rationale**: `TestClient` is the standard approach for testing FastAPI apps without
network overhead. pytest discovers tests in `tests/` automatically. Each test module
resets the in-memory store to a known state using a `@pytest.fixture`.

**Alternatives considered**:
- Starting a live Uvicorn process in tests: Slow, flaky, unnecessary.
- `unittest`: No advantage over pytest for this scope.

---

### D-006: Age Validation Implementation

**Decision**: Use a Pydantic v2 field validator: `age: Annotated[int, Field(gt=17)]`.

**Rationale**: `Field(gt=17)` maps directly to "age must be greater than 17". FastAPI
automatically documents this constraint in the OpenAPI schema. The error message from a 422
response names the field and the constraint.

**Alternatives considered**:
- `age >= 18` in a `@field_validator`: Equivalent semantics, slightly more verbose.
- Manual check in the route handler: Bypasses Pydantic's unified 422 response.

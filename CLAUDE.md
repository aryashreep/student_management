# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A graded assignment: a Student Management System with a FastAPI backend and a Streamlit frontend. The brief is in `Student Management System Assignm.txt`. Design docs are in `specs/001-student-management-system/` (spec, plan, data model, API contract in `contracts/student-api.md`, and tasks).

## Commands

```bash
docker compose up -d postgres                  # Postgres 16 on localhost:5432
pip install -r requirements.txt                # into .venv
python -m backend.seed                         # create tables + insert 100 Faker students (skips if table non-empty)
uvicorn main:app --reload                      # backend on :8000, Swagger at /docs
streamlit run frontend/app.py                  # frontend on :8501
pytest tests/ -v                               # all tests
pytest tests/test_add_student.py::test_add_student_success -v   # single test
```

`DATABASE_URL` is read from `.env` (asyncpg URL). The default in `backend/database.py` matches the credentials in `docker-compose.yml`.

## Architecture

- **Entrypoint indirection**: the root `main.py` only re-exports `app` from `backend/api/main.py`, so that `uvicorn main:app` works from the project root as the brief requires.
- **Two `Student` classes**: `backend/api/schema.py` is the Pydantic request model. `backend/models.py` is the SQLAlchemy ORM model. `routes.py` imports the ORM one as `StudentModel`. Validation rules (age > 17, non-blank name, valid email) are defined in both places, so change them together.
- **Async DB**: SQLAlchemy async engine + asyncpg (`backend/database.py`). Routes get a session through `Depends(get_db)`. Tables are created by `Base.metadata.create_all` in the FastAPI lifespan. Alembic is listed in `requirements.txt` but has no migrations set up.
- **IDs are client-supplied**, not auto-generated. `POST` returns 409 for a duplicate id or email. `PUT` keeps the path id and ignores `id` in the body. Missing ids return 404. Responses come from `StudentModel.to_dict()`, which omits the timestamp columns.
- **Frontend** (`frontend/app.py`) is a single Streamlit script. It talks to the backend only over HTTP (`requests`), uses a hardcoded `BACKEND_URL = "http://localhost:8000"`, and switches sections through `st.session_state.current_section`.

## Known drift — read before relying on docs or tests

- **Tests need the Postgres container running.** `tests/conftest.py` creates a separate `student_management_test` database, overrides `get_db` with a session on that database, and before each test truncates `students` and inserts 4 fixed rows (Rahul Sharma is id 1). Use the `empty_db` fixture for an empty table. The test engine uses `NullPool` because `TestClient` and `asyncio.run` run on different event loops.
- **The constitution is out of date.** `.specify/memory/constitution.md` (Principle IV) forbids an external database and ORMs and expects `app.py` at the root. The code now uses PostgreSQL + SQLAlchemy and keeps the frontend at `frontend/app.py`. `specs/.../quickstart.md` has the same old assumptions (`sample_data.json`, 4 seeded students). Amend the constitution or record the deviation before doing more Spec Kit work.
- The core rules in the constitution still apply: exactly 5 endpoints, exactly 5 fields, 422/409/404 semantics, and no bonus features until the core works.

## Workflow

The project uses Spec Kit (`.specify/`, with `/speckit-*` skills in `.claude/skills/`): specify → clarify → plan → tasks → implement. Plans must include a Constitution Check.

# Student Management System

A small full-stack app for managing student records: a **FastAPI** backend with **PostgreSQL** storage, and a **Streamlit** frontend. You can add, view, search, update and delete students.

It was built with **[Spec Kit](https://github.com/github/spec-kit)** (spec-driven development) and **Claude Code**. See [How this project was built](#how-this-project-was-built-spec-kit).

## Tech stack

| Layer    | Tools |
| -------- | ----- |
| Backend  | FastAPI, Uvicorn, Pydantic (with email validation) |
| Database | PostgreSQL 16 (Docker), SQLAlchemy 2 async, asyncpg |
| Frontend | Streamlit, pandas, requests |
| Tests    | pytest, FastAPI `TestClient` |
| Process  | Spec Kit 1.1.4 with the Claude Code integration |

## Project structure

```
├── main.py                     # Backend entrypoint (re-exports the FastAPI app)
├── backend/
│   ├── api/
│   │   ├── main.py             # App factory, CORS, DB startup/shutdown
│   │   ├── routes.py           # The 5 /students endpoints
│   │   └── schema.py           # Pydantic request model and validation
│   ├── database.py             # Async engine, sessions, get_db dependency
│   ├── models.py               # SQLAlchemy Student table
│   └── seed.py                 # Inserts 100 sample students
├── frontend/app.py             # Streamlit UI
├── tests/                      # pytest suite (runs against a separate test DB)
├── docker-compose.yml          # PostgreSQL service
├── specs/001-student-management-system/   # Spec Kit outputs (spec, plan, tasks…)
└── .specify/                   # Spec Kit config, templates, constitution
```

## Prerequisites

- Python 3.12 or newer (developed on 3.14)
- Docker, with Docker Compose
- Optional: [uv](https://docs.astral.sh/uv/), for installing packages and the Spec Kit CLI

## Installation

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt      # or: uv pip install -r requirements.txt

# 3. Start PostgreSQL
docker compose up -d postgres
```

Create a `.env` file in the project root. Its values must match `docker-compose.yml`:

```env
DATABASE_URL=postgresql+asyncpg://student_user:student_password@localhost:5432/student_management
```

If `.env` is missing, the backend falls back to this same URL.

```bash
# 4. Optional: load 100 sample students (skipped if the table already has data)
python -m backend.seed
```

## Running the app

Run each command in its own terminal, from the project root:

```bash
uvicorn main:app --reload            # Backend:  http://localhost:8000  (API docs at /docs)
streamlit run frontend/app.py        # Frontend: http://localhost:8501
```

The database tables are created automatically when the backend starts.

## API

| Method | Endpoint                 | Description          | Success | Errors   |
| ------ | ------------------------ | -------------------- | ------- | -------- |
| POST   | `/students`              | Add a student        | 201     | 409, 422 |
| GET    | `/students`              | List all students    | 200     | –        |
| GET    | `/students/{student_id}` | Get one student      | 200     | 404      |
| PUT    | `/students/{student_id}` | Update a student     | 200     | 404, 409, 422 |
| DELETE | `/students/{student_id}` | Delete a student     | 200     | 404      |

Example student:

```json
{ "id": 1, "name": "Rahul Sharma", "age": 21, "course": "AI", "email": "rahul@gmail.com" }
```

**Validation rules**
- `age` must be greater than 17.
- `email` must be a valid email address.
- `name` must not be empty or only spaces.

Invalid input returns **422**. A duplicate `id` or `email` returns **409**. On `PUT`, the id in the URL is used and any `id` in the request body is ignored.

The full contract is in [specs/001-student-management-system/contracts/student-api.md](specs/001-student-management-system/contracts/student-api.md).

## Running tests

PostgreSQL must be running (`docker compose up -d postgres`).

```bash
pytest tests/ -v                                                  # all tests
pytest tests/test_add_student.py::test_add_student_success -v     # one test
```

The tests create and use a separate database, `student_management_test`, so your development data is never changed. Before each test the table is cleared and 4 known students are inserted.

## How this project was built (Spec Kit)

This project follows **Spec-Driven Development** using GitHub's [Spec Kit](https://github.com/github/spec-kit). The specification is written and reviewed first. A technical plan and a task list are then generated from it, and only then is code written. Claude Code was the AI agent at each step.

### Install Spec Kit

```bash
# Install the `specify` CLI (requires uv)
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# Set up Spec Kit in an existing folder, using Claude Code
specify init --here --ai claude
```

This creates:
- `.specify/`: templates, helper scripts and the project constitution
- `.claude/skills/speckit-*`: slash commands for Claude Code

This repository already has both, so you only need the CLI if you want to set up Spec Kit in a new project.

### The workflow

Inside Claude Code, the steps were run in this order:

| Step | Command | Output |
| ---- | ------- | ------ |
| 1. Principles | `/speckit-constitution` | `.specify/memory/constitution.md`: the project's rules (scope, validation, API-first, simplicity, tests) |
| 2. Specify | `/speckit-specify` | `specs/001-…/spec.md`: user stories and requirements, from the assignment brief |
| 3. Clarify | `/speckit-clarify` | Fixes unclear points in the spec |
| 4. Plan | `/speckit-plan` | `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md` |
| 5. Tasks | `/speckit-tasks` | `tasks.md`: an ordered list of implementation tasks |
| 6. Analyze | `/speckit-analyze` | A consistency check across the spec, plan and tasks |
| 7. Implement | `/speckit-implement` | Writes the code by working through `tasks.md` |

Other commands available: `/speckit-checklist` (quality checklists, see `specs/001-…/checklists/`), `/speckit-converge`, and `/speckit-taskstoissues` (turns tasks into GitHub issues).

### Note on the constitution

The first version of the constitution called for in-memory or JSON storage. The project later moved to PostgreSQL with SQLAlchemy. `constitution.md` and `quickstart.md` still describe the original design and should be updated before more Spec Kit work. The core rules still apply: 5 endpoints, 5 fields, and the 422/409/404 error codes.

## Assignment brief

The original requirements are in [`Student Management System Assignm.txt`](Student%20Management%20System%20Assignm.txt).

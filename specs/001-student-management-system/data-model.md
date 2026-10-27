# Data Model: Student Management System

**Date**: 2026-10-11

---

## Entities

### Student

Represents a single enrolled learner at the coaching institute.

| Field  | Type    | Constraints                                    | Notes                          |
|--------|---------|------------------------------------------------|--------------------------------|
| id     | integer | unique, positive, assigned at creation         | Serves as primary key          |
| name   | string  | non-empty, not whitespace-only                 | Full name                      |
| age    | integer | greater than 17 (i.e., 18 or older)            | Age in years                   |
| course | string  | non-empty                                      | Programme name, free text      |
| email  | string  | valid email address format (RFC 5321/5322)     | Contact address                |

There is only one entity. No relationships to other entities exist in the core scope.

---

## Validation Rules

These rules are enforced at the backend boundary (not just in the UI) and apply to both
Create and Update operations unless noted.

| Rule        | Field  | Condition                       | Rejection code | Message type                  |
|-------------|--------|---------------------------------|----------------|-------------------------------|
| Unique ID   | id     | Must not match any existing id  | 409 Conflict   | Business-level error          |
| Age minimum | age    | Must be greater than 17         | 422 Unproc.    | Pydantic field validation     |
| Email valid | email  | Must be a valid email address   | 422 Unproc.    | Pydantic field validation     |
| Name filled | name   | Must not be empty or whitespace | 422 Unproc.    | Pydantic field validation     |
| ID exists   | id     | Must exist for GET/PUT/DELETE   | 404 Not Found  | Route-handler check           |
| ID immutable| id     | Must not change on PUT          | (by design)    | PUT path id is authoritative  |

---

## State Transitions

Student records have a simple three-state lifecycle:

```
[not present] --POST /students--> [active]
[active]      --PUT  /students/{id}--> [active]   (fields updated)
[active]      --DELETE /students/{id}--> [not present]
```

No soft-delete, no archiving, no status flags — deletion is permanent.

---

## Storage Representation

In-memory store at runtime:

```
data_store: dict[int, Student]  # key = student id
```

Seed format (`sample_data.json`):

```json
[
  { "id": 1, "name": "Rahul Sharma", "age": 21, "course": "AI",              "email": "rahul@gmail.com" },
  { "id": 2, "name": "Priya Verma",  "age": 22, "course": "Data Science",    "email": "priya@gmail.com" },
  { "id": 3, "name": "Aman Singh",   "age": 20, "course": "Web Development", "email": "aman@gmail.com"  },
  { "id": 4, "name": "Sneha Reddy",  "age": 23, "course": "AI",              "email": "sneha@gmail.com" }
]
```

The seed file is already present as `sample_data.json` in the project root.

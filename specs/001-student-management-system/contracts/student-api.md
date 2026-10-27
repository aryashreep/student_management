# API Contract: Student Management System

**Date**: 2026-10-11
**Base URL**: `http://localhost:8000`
**Format**: JSON request/response bodies. All errors return a JSON body.

---

## Shared Schemas

### Student (full record)

```json
{
  "id":     1,
  "name":   "Rahul Sharma",
  "age":    21,
  "course": "AI",
  "email":  "rahul@gmail.com"
}
```

### StudentInput (create / update body)

Same fields as Student. On create, `id` is supplied by the caller. On update, the `id` in
the path is authoritative; any `id` in the body MUST be ignored.

### Validation error (HTTP 422)

FastAPI / Pydantic standard format:

```json
{
  "detail": [
    {
      "loc":  ["body", "age"],
      "msg":  "Input should be greater than 17",
      "type": "greater_than"
    }
  ]
}
```

### Business error (HTTP 404 / 409)

```json
{ "detail": "Student not found" }
{ "detail": "Student with this ID already exists" }
```

---

## Endpoints

### POST /students — Add Student

**Request**

```
POST /students
Content-Type: application/json

{
  "id":     10,
  "name":   "Alice",
  "age":    22,
  "course": "AI",
  "email":  "alice@example.com"
}
```

**Responses**

| Status | Condition                         | Body                        |
|--------|-----------------------------------|-----------------------------|
| 201    | Student created                   | Full Student record         |
| 409    | `id` already exists               | `{ "detail": "..." }`       |
| 422    | Validation failure (age/email/name)| Standard Pydantic error     |

---

### GET /students — Get All Students

**Request**

```
GET /students
```

**Responses**

| Status | Condition       | Body                        |
|--------|-----------------|-----------------------------|
| 200    | Always          | Array of Student records (may be empty `[]`) |

---

### GET /students/{student_id} — Get Student by ID

**Request**

```
GET /students/1
```

Path parameter: `student_id` — integer.

**Responses**

| Status | Condition            | Body                        |
|--------|----------------------|-----------------------------|
| 200    | Student found        | Full Student record         |
| 404    | ID does not exist    | `{ "detail": "..." }`       |

---

### PUT /students/{student_id} — Update Student

**Request**

```
PUT /students/1
Content-Type: application/json

{
  "id":     1,
  "name":   "Rahul Sharma",
  "age":    22,
  "course": "Data Science",
  "email":  "rahul@gmail.com"
}
```

Path parameter: `student_id` — integer. Any `id` field in the body is ignored; the path
value is used.

**Responses**

| Status | Condition                         | Body                        |
|--------|-----------------------------------|-----------------------------|
| 200    | Student updated                   | Updated Student record      |
| 404    | ID does not exist                 | `{ "detail": "..." }`       |
| 422    | Validation failure (age/email/name)| Standard Pydantic error     |

---

### DELETE /students/{student_id} — Delete Student

**Request**

```
DELETE /students/1
```

Path parameter: `student_id` — integer.

**Responses**

| Status | Condition            | Body                                      |
|--------|----------------------|-------------------------------------------|
| 200    | Student deleted      | `{ "message": "Student deleted successfully" }` |
| 404    | ID does not exist    | `{ "detail": "..." }`                     |

---

## Bonus Endpoint (out of scope until core is complete)

### GET /students?course={course} — Filter by Course

```
GET /students?course=AI
```

Returns only students whose `course` matches (case-insensitive). Same 200 response shape
as GET /students. Implement only after all core endpoints and tests pass.

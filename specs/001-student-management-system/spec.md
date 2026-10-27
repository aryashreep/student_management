# Feature Specification: Student Management System

**Feature Branch**: `001-student-management-system`

**Created**: 2026-10-11

**Status**: Draft

**Input**: User description: "Student Management System per the assignment brief"

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add a New Student (Priority: P1)

A staff member at the coaching institute wants to register a new student by entering their
personal and course details into the system. The system must validate the data and confirm
successful registration, or explain exactly what is wrong if validation fails.

**Why this priority**: This is the entry point for all other operations. Without at least
one student in the system, View, Search, Update and Delete have nothing to act on.

**Independent Test**: The add form can be shown and submitted in isolation. Success is
confirmed when the new student immediately appears in the View page with the correct details.

**Acceptance Scenarios**:

1. **Given** a blank Add Student form, **When** the staff member enters valid data (id=10,
   name="Alice", age=22, course="AI", email="alice@example.com") and submits, **Then** the
   system confirms the student was added and the student appears in the full student list.
2. **Given** the Add Student form, **When** the staff member enters an age of 17 or younger,
   **Then** the system rejects the submission and displays a message identifying the age rule.
3. **Given** the Add Student form, **When** the staff member enters an invalid email such as
   "not-an-email", **Then** the system rejects the submission and highlights the email field.
4. **Given** the Add Student form, **When** the staff member leaves the name blank, **Then**
   the system rejects the submission and states the name is required.
5. **Given** an existing student with id=5, **When** a second submission uses id=5, **Then**
   the system rejects the duplicate and informs the staff member that the ID is already in use.

---

### User Story 2 - View All Students (Priority: P2)

A staff member wants to see the complete list of enrolled students at a glance, displayed in
a readable table that shows all fields for every student.

**Why this priority**: Visibility of the full dataset is required before targeted operations
(search, update, delete) provide additional value.

**Independent Test**: Loading the View page with at least one student in the system shows a
table; with zero students the page shows a clear empty-state message.

**Acceptance Scenarios**:

1. **Given** three students are stored, **When** the staff member opens the View page, **Then**
   a table shows all three rows with columns id, name, age, course, email.
2. **Given** no students are stored, **When** the staff member opens the View page, **Then**
   the page displays a message indicating no students are currently enrolled.

---

### User Story 3 - Search Student by ID (Priority: P3)

A staff member needs to quickly find a specific student's details using their unique ID,
without having to scroll through the full list.

**Why this priority**: Targeted lookup is more efficient than scrolling for large datasets,
but depends on students already being in the system.

**Independent Test**: Entering an existing ID shows exactly one student's details; an unknown
ID returns a clear "not found" message.

**Acceptance Scenarios**:

1. **Given** a student with id=3 exists, **When** the staff member searches for id=3, **Then**
   the system displays only that student's complete details.
2. **Given** no student with id=99 exists, **When** the staff member searches for id=99, **Then**
   the system informs the staff member that no student with that ID was found.

---

### User Story 4 - Update Student Details (Priority: P4)

A staff member wants to correct or update a student's information (name, age, course, email)
using the student's ID to identify the record. The ID itself cannot be changed.

**Why this priority**: Students' details change over time; without an update path the only
remedy is delete-and-re-add, which risks data inconsistency.

**Independent Test**: Changing the course field of an existing student and saving it produces
the new course value in the View page.

**Acceptance Scenarios**:

1. **Given** student id=2 has course="Web Development", **When** the staff member updates
   course to "Data Science" and saves, **Then** the View page shows "Data Science" for id=2.
2. **Given** an attempt to update with an invalid email, **When** the form is submitted, **Then**
   the system rejects the update and shows the same validation feedback as on Add.
3. **Given** id=99 does not exist, **When** the staff member submits an update for id=99,
   **Then** the system informs them the student was not found.

---

### User Story 5 - Delete Student Record (Priority: P5)

A staff member wants to permanently remove a student record from the system using the
student's ID.

**Why this priority**: Record removal is the least frequent operation, but it must work
cleanly and without leaving orphaned data.

**Independent Test**: Deleting an existing student by ID makes that student disappear from
the View page.

**Acceptance Scenarios**:

1. **Given** student id=4 exists, **When** the staff member enters id=4 and confirms deletion,
   **Then** the system confirms the deletion and the student is no longer in the View list.
2. **Given** id=99 does not exist, **When** the staff member attempts to delete id=99, **Then**
   the system reports that no student with that ID was found.

---

### Edge Cases

- What happens when two staff members try to add a student with the same ID simultaneously?
  (Sequential IDs help; duplicate detection must reject gracefully.)
- What happens when the backend service is unreachable from the frontend? The frontend must
  show a connection-error message rather than an unhandled crash.
- What happens when the View page is loaded and the data store is empty? An explicit
  empty-state message is required.
- What happens when a search ID is non-numeric? The system should show a user-friendly error.
- What happens when the age field receives a non-integer value? Validation must catch it.

---

## Requirements *(mandatory)*

### Functional Requirements

**Student Data Management**

- **FR-001**: The system MUST allow a staff member to create a new student record containing
  exactly these five fields: id (unique whole number), name (non-empty text), age (whole
  number greater than 17), course (text), email (valid email address).
- **FR-002**: The system MUST display all stored student records in a tabular layout showing
  all five fields.
- **FR-003**: The system MUST allow a staff member to retrieve a single student's record by
  entering the student's ID.
- **FR-004**: The system MUST allow a staff member to modify an existing student's name, age,
  course, or email using the student's ID; the ID itself MUST NOT be changeable.
- **FR-005**: The system MUST allow a staff member to permanently delete a student record
  using the student's ID.

**Validation**

- **FR-006**: The system MUST reject any student record where age is 17 or younger, and MUST
  communicate the age rule to the staff member.
- **FR-007**: The system MUST reject any student record with a malformed email address, and
  MUST communicate which field failed.
- **FR-008**: The system MUST reject any student record with a blank or whitespace-only name.
- **FR-009**: The system MUST reject creation of a student whose ID already exists in the
  system, returning a clear duplicate-ID message.

**Error Handling**

- **FR-010**: When an operation references an ID that does not exist, the system MUST inform
  the staff member that the record was not found.
- **FR-011**: When the frontend cannot reach the backend, the system MUST display a
  user-friendly connection-error message and MUST NOT crash or show a raw exception.

**Startup & Interface**

- **FR-012**: The backend MUST start with `uvicorn main:app --reload` from the project root
  without additional configuration.
- **FR-013**: The frontend MUST start with `streamlit run app.py` from the project root
  without additional configuration.
- **FR-014**: The frontend MUST provide five distinct navigation sections: Add Student, View
  Students, Search Student, Update Student, Delete Student.

### Key Entities

- **Student**: Represents a single enrolled learner. Attributes: id (unique identifier),
  name (full name), age (in years), course (enrolled programme), email (contact address).
  There is no relationship to other entities in the core scope.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A staff member can register a valid new student in under 30 seconds from
  opening the Add page to seeing the confirmation.
- **SC-002**: All five student fields appear correctly for every record displayed in the
  View table with no missing or garbled values.
- **SC-003**: Searching by a valid ID returns the correct student's details; searching by an
  unknown ID returns a clear not-found message — in both cases within 2 seconds of submission.
- **SC-004**: Every validation rule (age > 17, valid email, non-empty name, unique ID) is
  enforced: invalid submissions are rejected 100% of the time with an explanatory message.
- **SC-005**: A student record can be updated and the change is immediately visible on the
  View page without requiring a manual refresh.
- **SC-006**: A deleted student record no longer appears in the View list after deletion is
  confirmed.
- **SC-007**: Both startup commands (`uvicorn main:app --reload` and `streamlit run app.py`)
  complete successfully without errors in a clean Python environment with dependencies
  installed.

---

## Assumptions

- The system is for internal staff at a single coaching institute; there is no multi-tenancy,
  user authentication or role management in scope.
- Storage is single-process in-memory or a local JSON file. No external database server is
  used. `sample_data.json` may be used to seed initial data on startup.
- The frontend communicates with the backend over localhost; no network security (TLS, API
  keys) is required for this assignment.
- Mobile and tablet layouts are out of scope; the frontend targets desktop browsers.
- There is no requirement for bulk import/export beyond the seed file.
- Bonus features (course filtering query parameter and a statistics dashboard) are explicitly
  out of scope until all core requirements are met per the constitution.
- The ID is assigned by the staff member at creation time, not auto-generated by the system.

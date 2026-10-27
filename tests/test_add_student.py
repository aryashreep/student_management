def test_add_student_success(client):
    payload = {"id": 10, "name": "Alice", "age": 22, "course": "AI", "email": "alice@example.com"}
    r = client.post("/students", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["id"] == 10
    assert data["name"] == "Alice"
    assert data["age"] == 22
    assert data["course"] == "AI"
    assert data["email"] == "alice@example.com"


def test_add_student_duplicate_id(client):
    payload = {"id": 1, "name": "Duplicate", "age": 20, "course": "CS", "email": "dup@example.com"}
    r = client.post("/students", json=payload)
    assert r.status_code == 409
    assert "detail" in r.json()


def test_add_student_age_too_low(client):
    payload = {"id": 99, "name": "Young", "age": 17, "course": "CS", "email": "young@example.com"}
    r = client.post("/students", json=payload)
    assert r.status_code == 422


def test_add_student_invalid_email(client):
    payload = {"id": 99, "name": "Alice", "age": 22, "course": "AI", "email": "notvalid"}
    r = client.post("/students", json=payload)
    assert r.status_code == 422


def test_add_student_empty_name(client):
    payload = {"id": 99, "name": "", "age": 22, "course": "AI", "email": "alice@example.com"}
    r = client.post("/students", json=payload)
    assert r.status_code == 422


def test_add_student_whitespace_name(client):
    payload = {"id": 99, "name": "   ", "age": 22, "course": "AI", "email": "alice@example.com"}
    r = client.post("/students", json=payload)
    assert r.status_code == 422

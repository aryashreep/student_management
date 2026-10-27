def test_update_student_success(client):
    payload = {"id": 1, "name": "Rahul Sharma", "age": 25, "course": "Data Science", "email": "rahul@gmail.com"}
    r = client.put("/students/1", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["age"] == 25
    assert data["course"] == "Data Science"


def test_update_student_path_id_authoritative(client):
    payload = {"id": 999, "name": "Rahul Sharma", "age": 22, "course": "AI", "email": "rahul@gmail.com"}
    r = client.put("/students/1", json=payload)
    assert r.status_code == 200
    assert r.json()["id"] == 1


def test_update_student_not_found(client):
    payload = {"id": 999, "name": "Ghost", "age": 20, "course": "CS", "email": "ghost@example.com"}
    r = client.put("/students/999", json=payload)
    assert r.status_code == 404
    assert "detail" in r.json()


def test_update_student_age_too_low(client):
    payload = {"id": 1, "name": "Rahul Sharma", "age": 15, "course": "AI", "email": "rahul@gmail.com"}
    r = client.put("/students/1", json=payload)
    assert r.status_code == 422


def test_update_student_invalid_email(client):
    payload = {"id": 1, "name": "Rahul Sharma", "age": 21, "course": "AI", "email": "bad"}
    r = client.put("/students/1", json=payload)
    assert r.status_code == 422

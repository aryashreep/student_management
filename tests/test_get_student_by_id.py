def test_get_student_found(client):
    r = client.get("/students/1")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == 1
    assert data["name"] == "Rahul Sharma"
    assert data["age"] == 21
    assert data["course"] == "AI"
    assert data["email"] == "rahul@gmail.com"


def test_get_student_not_found(client):
    r = client.get("/students/999")
    assert r.status_code == 404
    assert "detail" in r.json()

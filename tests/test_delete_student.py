def test_delete_student_success(client):
    r = client.delete("/students/1")
    assert r.status_code == 200
    assert r.json() == {"message": "Student deleted successfully"}


def test_delete_student_gone_after_delete(client):
    client.delete("/students/1")
    r = client.get("/students/1")
    assert r.status_code == 404


def test_delete_student_not_found(client):
    r = client.delete("/students/999")
    assert r.status_code == 404
    assert "detail" in r.json()

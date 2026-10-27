def test_get_students_seeded(client):
    r = client.get("/students")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) == 4
    fields = {"id", "name", "age", "course", "email"}
    for s in data:
        assert fields.issubset(s.keys())


def test_get_students_empty(client, empty_db):
    r = client.get("/students")
    assert r.status_code == 200
    assert r.json() == []

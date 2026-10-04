import sqlite3
import pytest
import app as app_module

@pytest.fixture
def client(monkeypatch, tmp_path):
    db_path = str(tmp_path / "test.db")

    def test_db():
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    monkeypatch.setattr(app_module, "get_db", test_db)
    app_module.init_db()
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as c:
        yield c

def test_add_and_list(client):
    r = client.post("/api/tasks", json={"title": "Test task"})
    assert r.status_code == 201
    r = client.get("/api/tasks")
    assert len(r.get_json()) == 1

def test_add_without_title(client):
    r = client.post("/api/tasks", json={})
    assert r.status_code == 400

def test_update_task(client):
    client.post("/api/tasks", json={"title": "A"})
    r = client.put("/api/tasks/1", json={"done": 1})
    assert r.get_json()["done"] == 1

def test_delete_missing_task(client):
    r = client.delete("/api/tasks/999")
    assert r.status_code == 404
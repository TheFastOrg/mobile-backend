# test_main.py
from fastapi.testclient import TestClient
from tests.test import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

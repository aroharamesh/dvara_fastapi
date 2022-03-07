from fastapi.testclient import TestClient

from arthmate_lender_handoff_service.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
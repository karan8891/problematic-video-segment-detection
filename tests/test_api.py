from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_submit_video():
    response = client.post(
        "/videos",
        json={"video_url": "https://samplelib.com/lib/preview/mp4/sample-5s.mp4"}
    )

    assert response.status_code == 200
    body = response.json()
    assert "video_id" in body
    assert body["status"] == "queued"


def test_unknown_video_status_returns_404():
    response = client.get("/videos/non-existing-id/status")
    assert response.status_code == 404
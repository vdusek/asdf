from fastapi.testclient import TestClient

from asdf.main import app

client = TestClient(app)


def test_get_root() -> None:
    url = "/"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}

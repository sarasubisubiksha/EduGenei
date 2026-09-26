from fastapi.testclient import TestClient
from main import app,ai
client=TestClient(app)
def test_home():
    r=client.get("/")
    assert r.status_code==200 and "EduGenie" in r.text
def test_health():
    assert client.get("/health").json()["status"]=="ok"
def test_validation():
    assert client.post("/qa",json={"text":"x"}).status_code==422
def test_missing_key(monkeypatch):
    monkeypatch.setattr(ai,"client",None)
    assert client.post("/qa",json={"text":"What is an ocean?"}).status_code==503

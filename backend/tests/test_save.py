import pytest

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.core.database import get_session
from app.main import app

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_save_report(client: TestClient):
    response = client.post("/reports/save", json={"name": "Report_1", "start_date": "2025-03-24T15:36:15.889Z", "end_date": "2026-03-24T15:36:15.889Z", "data": []})

    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Report_1"
    assert data["date_range_start"] == "2025-03-24T15:36:15.889000"
    assert data["date_range_end"] == "2026-03-24T15:36:15.889000"
    assert data["data"] == "[]"
    assert data["id"] is not None

def test_save_empty_name(client: TestClient):
    response = client.post("/reports/save", json={"name": " ", "start_date": "2025-03-24T15:36:15.889Z", "end_date": "2026-03-24T15:36:15.889Z", "data": []})

    assert response.status_code == 422
    assert response.json() == {"detail": "Name can't be blank"}
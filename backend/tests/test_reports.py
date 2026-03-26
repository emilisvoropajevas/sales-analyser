import pytest

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.core.database import get_session
from app.main import app

@pytest.fixture(name = "session")
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

def test_get_report_history(client: TestClient):
    send_test_data = client.post("/reports/save", json={"name": "Report_1", "start_date": "2025-03-24T15:36:15.889Z", "end_date": "2026-03-24T15:36:15.889Z", "data": []})
    
    response  = client.get("/reports/")

    assert response.status_code == 200
    assert response.json()[0]["name"] == "Report_1" 
    assert "data" not in response.json()[0]
    
def test_get_report(client: TestClient):
    send_report_data = client.post("/reports/save", json={"name": "Report_2", "start_date": "2025-03-24T15:36:15.889Z", "end_date": "2026-03-24T15:36:15.889Z", "data": []})
    
    response = client.get("/reports/1")

    assert response.status_code == 200
    assert response.json()["name"] == "Report_2"
    assert "data" in response.json()

    not_found_response = client.get("/reports/2")
    assert not_found_response.status_code == 404
    assert not_found_response.json() == {"detail": "Report not found"}

def test_update_report(client: TestClient):
    send_report_data = client.post("/reports/save", json={"name": "Report_3", "start_date": "2025-03-24T15:36:15.889Z", "end_date": "2026-03-24T15:36:15.889Z", "data": []})

    get_wrong_report = client.get("/reports/2")
    update_report = client.put("/reports/1", json={"name": "Renamed_Report"})
    send_bad_update = client.put("/reports/1", json={"name": ""})
    
    assert get_wrong_report.status_code == 404
    assert get_wrong_report.json() == {"detail": "Report not found"}

    assert update_report.status_code == 200
    assert update_report.json()["name"] == "Renamed_Report"
    
    assert send_bad_update.status_code == 422
    assert send_bad_update.json() == {"detail": "Name can't be blank"}

def test_delete_report(client: TestClient):
    send_report_data = client.post("/reports/save", json={"name": "Report_4", "start_date": "2025-03-24T15:36:15.889Z", "end_date": "2026-03-24T15:36:15.889Z", "data": []})
    
    get_wrong_report = client.get("/reports/2")
    delete_report = client.delete("/reports/1")

    assert get_wrong_report.status_code == 404
    assert get_wrong_report.json() == {"detail": "Report not found"}

    assert delete_report.status_code == 200
    assert delete_report.json() == {"message": "Report deleted"}
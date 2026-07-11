def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_api_v1_check(client):
    response = client.get("/api/v1")
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_system_status(client):
    response = client.get("/api/v1/system/status")
    assert response.status_code == 200
    data = response.json()["data"]
    assert "sqlite" in data
    assert "neo4j" in data
    assert "gemini" in data

def test_documents_list_empty(client):
    response = client.get("/api/v1/documents")
    assert response.status_code == 200
    assert "documents" in response.json()["data"]
    
def test_analytics_dashboard(client):
    response = client.get("/api/v1/analytics/dashboard")
    assert response.status_code == 200
    assert response.json()["success"] is True

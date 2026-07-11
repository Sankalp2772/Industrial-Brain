# tests/test_critical_path.py
import pytest

@pytest.mark.skip(reason="Requires a valid PDF in sample-data and live Gemini API key")
def test_end_to_end_critical_path(client):
    # 1. Upload
    with open("../sample-data/dummy.pdf", "rb") as f:
        res = client.post("/api/v1/documents/upload", files={"file": ("dummy.pdf", f, "application/pdf")})
    assert res.status_code == 200
    doc_id = res.json()["data"]["id"]
    
    # 2. Text Extraction
    res = client.post(f"/api/v1/extraction/document/{doc_id}/extract")
    assert res.status_code == 200
    
    # 3. Knowledge Extraction
    res = client.post(f"/api/v1/extraction/document/{doc_id}/knowledge")
    assert res.status_code == 200
    
    # 4. Graph Build
    res = client.post(f"/api/v1/graph/documents/{doc_id}/graph")
    assert res.status_code == 200
    
    # 5. Embeddings
    res = client.post(f"/api/v1/embeddings/documents/{doc_id}/embeddings")
    assert res.status_code == 200
    
    # 6. Copilot Query
    res = client.post("/api/v1/copilot/query", json={"question": "What is in the dummy document?"})
    assert res.status_code == 200
    assert "data" in res.json()

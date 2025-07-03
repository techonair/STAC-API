import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_search_bbox_datetime():
    response = client.post("/v1/stac/search?bbox=77.5,12.9,77.7,13.1&datetime=2023-11-01T00:00:00Z/2023-11-30T23:59:59Z")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert "features" in data
    assert isinstance(data["features"], list)

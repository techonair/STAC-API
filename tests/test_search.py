import pytest
from fastapi.testclient import TestClient
from stac_api.api.main import app

client = TestClient(app)

def test_search_endpoint_valid_bbox_and_datetime():
    response = client.post(
        "/search",
        json={
            "bbox": [77.5, 12.9, 77.7, 13.1],
            "datetime": "2023-11-01"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert "features" in data
    assert len(data["features"]) > 0

def test_search_endpoint_invalid_bbox():
    response = client.post(
        "/search",
        json={
            "bbox": [200.0, 12.9, 77.7, 13.1],  # Invalid bbox
            "datetime": "2023-11-01"
        }
    )
    assert response.status_code == 400  # Assuming the API returns 400 for invalid requests

def test_search_endpoint_no_results():
    response = client.post(
        "/search",
        json={
            "bbox": [77.5, 12.9, 77.7, 13.1],
            "datetime": "2020-01-01"  # Date with no results
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) == 0

def test_search_endpoint_missing_parameters():
    response = client.post("/search", json={})
    assert response.status_code == 422  # Assuming the API returns 422 for validation errors
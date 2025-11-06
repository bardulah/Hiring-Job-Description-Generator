"""
Integration tests for the API.
"""

import pytest
from fastapi.testclient import TestClient
from src.api.server import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def sample_job_descriptions():
    """Sample job descriptions for testing."""
    return [
        {
            "title": "Product Manager",
            "company": "TestCorp",
            "description": " ".join(["test"] * 100)  # Meet minimum word count
        },
        {
            "title": "Senior PM",
            "company": "TestCo",
            "description": " ".join(["test"] * 100)
        },
        {
            "title": "Lead PM",
            "company": "TestInc",
            "description": " ".join(["test"] * 100)
        }
    ]


class TestAPIEndpoints:
    """Tests for API endpoints."""

    def test_root_endpoint(self, client):
        """Test root endpoint returns API info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_analyze_endpoint_with_valid_data(self, client, sample_job_descriptions):
        """Test analyze endpoint with valid data."""
        response = client.post("/api/v1/analyze", json=sample_job_descriptions)
        assert response.status_code == 200
        data = response.json()
        assert "total_analyzed" in data
        assert data["total_analyzed"] == 3

    def test_analyze_endpoint_with_insufficient_data(self, client):
        """Test analyze endpoint rejects insufficient data."""
        insufficient_data = [
            {
                "title": "PM",
                "company": "TestCorp",
                "description": " ".join(["test"] * 100)
            }
        ]
        response = client.post("/api/v1/analyze", json=insufficient_data)
        assert response.status_code in [400, 422]  # Validation error

    def test_stats_endpoint(self, client):
        """Test statistics endpoint."""
        response = client.get("/api/v1/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_jobs" in data

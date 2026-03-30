"""Tests for health endpoint."""
from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Test health check endpoint returns 200."""
    response = client.get("/api/v1/health")
    
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert "timestamp" in data
    assert data["service"] == "API Santander Espelhamento"
    assert "rabbitmq" in data


def test_health_check_structure(client: TestClient):
    """Test health check response structure."""
    response = client.get("/api/v1/health")
    
    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "service" in data
    assert "rabbitmq" in data
    
    # Check RabbitMQ health structure
    rabbitmq = data["rabbitmq"]
    assert "rabbitmq_connected" in rabbitmq
    assert "host" in rabbitmq
    assert "port" in rabbitmq
    assert isinstance(rabbitmq["rabbitmq_connected"], bool)


def test_health_check_rabbitmq_info(client: TestClient):
    """Test health check includes RabbitMQ information."""
    response = client.get("/api/v1/health")
    
    data = response.json()
    rabbitmq = data["rabbitmq"]
    
    assert rabbitmq["host"] is not None
    assert rabbitmq["port"] is not None
    assert isinstance(rabbitmq["port"], int)

"""Tests for document endpoints."""
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def sample_document():
    """Sample document data for testing."""
    return {
        "numero_acordo": "ACC-2026-001",
        "documento": "Boleto",
        "arquivo": {
            "filename": "boleto.pdf",
            "base64": "aGVsbG8gd29ybGQ="  # "hello world" in base64
        }
    }


def test_create_document_without_api_key(client: TestClient, sample_document):
    """Test that document creation fails without API key."""
    response = client.post("/api/v1/document", json=sample_document)
    
    assert response.status_code == 401
    assert "API Key não fornecida" in response.json()["detail"]


def test_create_document_with_invalid_api_key(client: TestClient, sample_document):
    """Test that document creation fails with invalid API key."""
    response = client.post(
        "/api/v1/document",
        json=sample_document,
        headers={"X-Api-Key": "invalid-key"}
    )
    
    assert response.status_code == 401
    assert "API Key inválida" in response.json()["detail"]


def test_create_document_success(
    client: TestClient,
    sample_document,
    api_key: str,
    mock_rabbitmq
):
    """Test successful document creation."""
    response = client.post(
        "/api/v1/document",
        json=sample_document,
        headers={"X-Api-Key": api_key}
    )
    
    assert response.status_code == 201
    
    data = response.json()
    assert data["message"] == "Documento recebido com sucesso"
    assert data["numero_acordo"] == "ACC-2026-001"
    assert data["filename"] == "boleto.pdf"
    
    # Verify RabbitMQ was called
    mock_rabbitmq.publish_document.assert_called_once()


def test_create_document_invalid_data(client: TestClient, api_key: str):
    """Test document creation with invalid data."""
    invalid_data = {
        "numero_acordo": "ACC-2026-001",
        # Missing required fields
    }
    
    response = client.post(
        "/api/v1/document",
        json=invalid_data,
        headers={"X-Api-Key": api_key}
    )
    
    assert response.status_code == 422  # Validation error

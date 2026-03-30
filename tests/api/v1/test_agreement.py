"""Tests for agreement endpoints."""
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def sample_agreement():
    """Sample agreement data for testing."""
    return {
        "operador": "OPERATOR123",
        "iniciado_em": "2026-03-30T10:00:00",
        "finalizado_em": "2026-03-30T10:30:00",
        "dados": {
            "nome": "João Silva",
            "documento": "12345678900",
            "numero_acordo": "ACC-2026-001",
            "meio_de_pagamento": "Boleto",
            "iof": "50.00",
            "taxa_de_juros": "2.5",
            "taxa_cet": "3.2",
            "modalidade_do_desconto": "à vista",
            "data_da_primeira_parcela": "2026-04-30",
            "vencimento_demais_parcelas": "Todo dia 30",
            "valor_total_da_divida": "10000.00",
            "valor_do_desconto": "1000.00",
            "valor_para_pagamento": "9000.00",
            "valor_negociado": "9000.00",
            "quantidade_de_parcelas": "12",
            "valor_das_parcelas": "750.00",
            "data_da_entrada": "2026-03-30",
            "valor_da_entrada": "0.00"
        }
    }


def test_create_agreement_without_api_key(client: TestClient, sample_agreement):
    """Test that agreement creation fails without API key."""
    response = client.post("/api/v1/agreement", json=sample_agreement)
    
    assert response.status_code == 401
    assert "API Key não fornecida" in response.json()["detail"]


def test_create_agreement_with_invalid_api_key(client: TestClient, sample_agreement):
    """Test that agreement creation fails with invalid API key."""
    response = client.post(
        "/api/v1/agreement",
        json=sample_agreement,
        headers={"X-Api-Key": "invalid-key"}
    )
    
    assert response.status_code == 401
    assert "API Key inválida" in response.json()["detail"]


def test_create_agreement_success(
    client: TestClient,
    sample_agreement,
    api_key: str,
    mock_rabbitmq
):
    """Test successful agreement creation."""
    response = client.post(
        "/api/v1/agreement",
        json=sample_agreement,
        headers={"X-Api-Key": api_key}
    )
    
    assert response.status_code == 201
    
    data = response.json()
    assert data["message"] == "Acordo recebido com sucesso"
    assert data["numero_acordo"] == "ACC-2026-001"
    assert data["operador"] == "OPERATOR123"
    
    # Verify RabbitMQ was called
    mock_rabbitmq.publish_agreement.assert_called_once()


def test_create_agreement_invalid_data(client: TestClient, api_key: str):
    """Test agreement creation with invalid data."""
    invalid_data = {
        "operador": "OPERATOR123",
        # Missing required fields
    }
    
    response = client.post(
        "/api/v1/agreement",
        json=invalid_data,
        headers={"X-Api-Key": api_key}
    )
    
    assert response.status_code == 422  # Validation error

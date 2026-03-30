"""Test configuration and fixtures."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from main import app
from app.core.config import get_settings


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def mock_rabbitmq(monkeypatch):
    """Mock RabbitMQ client for testing."""
    mock_client = MagicMock()
    mock_client.publish_agreement.return_value = True
    mock_client.publish_document.return_value = True
    
    from app.core import rabbitmq
    monkeypatch.setattr(rabbitmq, "rabbitmq_client", mock_client)
    
    return mock_client


@pytest.fixture
def api_key():
    """Get API key from settings."""
    settings = get_settings()
    return settings.API_KEY

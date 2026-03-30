"""Health check schema."""
from pydantic import BaseModel, Field
from typing import Optional


class RabbitMQHealth(BaseModel):
    """RabbitMQ connection health."""
    rabbitmq_connected: bool = Field(..., description="Status de conexão com RabbitMQ")
    host: str = Field(..., description="Host do RabbitMQ")
    port: int = Field(..., description="Porta do RabbitMQ")


class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str = Field(..., description="Status da API")
    timestamp: str = Field(..., description="Timestamp da verificação")
    service: str = Field(..., description="Nome do serviço")
    rabbitmq: Optional[RabbitMQHealth] = Field(None, description="Status do RabbitMQ")

"""Health check endpoint."""
from fastapi import APIRouter
from datetime import datetime
from app.schemas.health import HealthResponse, RabbitMQHealth
from app.core.rabbitmq import rabbitmq_client

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify API status and dependencies.
    
    Returns:
        HealthResponse with current status, timestamp, and RabbitMQ status
    """
    # Check RabbitMQ health
    rabbitmq_health_dict = rabbitmq_client.health_check()
    rabbitmq_health = RabbitMQHealth(**rabbitmq_health_dict)
    
    # Determine overall status
    status = "healthy" if rabbitmq_health.rabbitmq_connected else "degraded"
    
    return HealthResponse(
        status=status,
        timestamp=datetime.now().isoformat(),
        service="API Santander Espelhamento",
        rabbitmq=rabbitmq_health
    )

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Endpoint de health check para verificar se a API está funcionando
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "API Santander Espelhamento"
    }

"""FastAPI application entry point."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

from app.core.config import get_settings
from app.core.rabbitmq import rabbitmq_client
from app.api.v1.router import api_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.
    Fails fast if RabbitMQ connection cannot be established.
    """
    # Startup: connect to RabbitMQ (required)
    logger.info("Iniciando conexão com RabbitMQ...")
    try:
        rabbitmq_client.connect()
        logger.info("RabbitMQ conectado com sucesso")
    except Exception as e:
        logger.error(f"Erro crítico ao conectar ao RabbitMQ: {str(e)}")
        logger.error("A API não pode iniciar sem conexão com RabbitMQ")
        raise  # Re-raise to prevent application startup
    
    yield
    
    # Shutdown: disconnect from RabbitMQ
    logger.info("Encerrando conexão com RabbitMQ...")
    try:
        rabbitmq_client.disconnect()
        logger.info("RabbitMQ desconectado")
    except Exception as e:
        logger.error(f"Erro ao desconectar do RabbitMQ: {str(e)}")


# Create FastAPI application
app = FastAPI(
    title="API Santander Espelhamento",
    version="1.0.0",
    description="API para receber dados de acordos e documentos",
    lifespan=lifespan
)

# CORS middleware (customize as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        loop="asyncio"
    )

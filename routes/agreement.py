from fastapi import APIRouter, HTTPException, status, Depends
from models.agreement import Agreement
from security import verify_api_key
from rabbitmq import rabbitmq_client
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/agreement", status_code=status.HTTP_201_CREATED)
async def create_agreement(agreement: Agreement, api_key: str = Depends(verify_api_key)):
    """
    Endpoint para receber dados de acordo
    
    - **operador**: Identificador do operador
    - **iniciado_em**: Data e hora de início
    - **finalizado_em**: Data e hora de finalização
    - **dados**: Dados completos do acordo
    """
    try:
        # Publicar mensagem na fila do RabbitMQ
        rabbitmq_client.publish_agreement(agreement)
        
        logger.info(f"Acordo {agreement.dados.numero_acordo} publicado na fila")
        
        return {
            "message": "Acordo recebido com sucesso",
            "numero_acordo": agreement.dados.numero_acordo,
            "operador": agreement.operador
        }
    except Exception as e:
        logger.error(f"Erro ao processar acordo: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar acordo: {str(e)}"
        )

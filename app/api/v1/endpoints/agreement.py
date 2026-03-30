"""Agreement endpoints."""
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.agreement import Agreement, AgreementResponse
from app.services.agreement_service import agreement_service
from app.core.security import verify_api_key
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/agreement",
    response_model=AgreementResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Agreement",
    description="Receive and process agreement data, publishing it to RabbitMQ queue"
)
async def create_agreement(
    agreement: Agreement,
    api_key: str = Depends(verify_api_key)
):
    """
    Create a new agreement and publish to message queue.
    
    - **operador**: Operator identifier
    - **iniciado_em**: Start date and time
    - **finalizado_em**: End date and time
    - **dados**: Complete agreement data
    
    Returns:
        AgreementResponse with processing result
    """
    try:
        result = await agreement_service.process_agreement(agreement)
        return result
    except Exception as e:
        logger.error(f"Erro ao processar acordo: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar acordo: {str(e)}"
        )

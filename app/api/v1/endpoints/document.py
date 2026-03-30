"""Document endpoints."""
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.document import Document, DocumentResponse
from app.services.document_service import document_service
from app.core.security import verify_api_key
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/document",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Document",
    description="Receive and process document data (base64), publishing it to RabbitMQ queue"
)
async def create_document(
    document: Document,
    api_key: str = Depends(verify_api_key)
):
    """
    Create a new document and publish to message queue.
    
    - **numero_acordo**: Related agreement number
    - **documento**: Document type or name
    - **arquivo**: File data (filename and base64 content)
    
    Returns:
        DocumentResponse with processing result
    """
    try:
        result = await document_service.process_document(document)
        return result
    except Exception as e:
        logger.error(f"Erro ao processar documento: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar documento: {str(e)}"
        )

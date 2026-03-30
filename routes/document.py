from fastapi import APIRouter, HTTPException, status, Depends
from models.document import Document
from security import verify_api_key
from rabbitmq import rabbitmq_client
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/document", status_code=status.HTTP_201_CREATED)
async def create_document(document: Document, api_key: str = Depends(verify_api_key)):
    """
    Endpoint para receber documentos em base64
    
    - **numero_acordo**: Número do acordo relacionado
    - **documento**: Tipo ou nome do documento
    - **arquivo**: Dados do arquivo (filename e base64)
    """
    try:
        # Publicar mensagem na fila do RabbitMQ
        rabbitmq_client.publish_document(document)
        
        logger.info(f"Documento {document.arquivo.filename} do acordo {document.numero_acordo} publicado na fila")
        
        return {
            "message": "Documento recebido com sucesso",
            "numero_acordo": document.numero_acordo,
            "filename": document.arquivo.filename
        }
    except Exception as e:
        logger.error(f"Erro ao processar documento: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar documento: {str(e)}"
        )

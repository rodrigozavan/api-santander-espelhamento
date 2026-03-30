"""Document business logic service."""
import logging
from app.schemas.document import Document, DocumentResponse
from app.core.rabbitmq import rabbitmq_client

logger = logging.getLogger(__name__)


class DocumentService:
    """Service for handling document business logic."""
    
    def __init__(self):
        self.rabbitmq_client = rabbitmq_client
    
    async def process_document(self, document: Document) -> DocumentResponse:
        """
        Process document data and publish to RabbitMQ queue.
        
        Args:
            document: Document data to process
            
        Returns:
            DocumentResponse with processing result
            
        Raises:
            Exception: If processing or publishing fails
        """
        try:
            # Publish message to RabbitMQ queue
            self.rabbitmq_client.publish_document(document)
            
            logger.info(
                f"Documento {document.arquivo.filename} do acordo "
                f"{document.numero_acordo} processado e publicado na fila"
            )
            
            return DocumentResponse(
                message="Documento recebido com sucesso",
                numero_acordo=document.numero_acordo,
                filename=document.arquivo.filename
            )
        except Exception as e:
            logger.error(f"Erro ao processar documento: {str(e)}")
            raise


# Service instance
document_service = DocumentService()

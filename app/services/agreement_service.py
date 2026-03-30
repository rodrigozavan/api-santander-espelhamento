"""Agreement business logic service."""
import logging
from app.schemas.agreement import Agreement, AgreementResponse
from app.core.rabbitmq import rabbitmq_client

logger = logging.getLogger(__name__)


class AgreementService:
    """Service for handling agreement business logic."""
    
    def __init__(self):
        self.rabbitmq_client = rabbitmq_client
    
    async def process_agreement(self, agreement: Agreement) -> AgreementResponse:
        """
        Process agreement data and publish to RabbitMQ queue.
        
        Args:
            agreement: Agreement data to process
            
        Returns:
            AgreementResponse with processing result
            
        Raises:
            Exception: If processing or publishing fails
        """
        try:
            # Publish message to RabbitMQ queue
            self.rabbitmq_client.publish_agreement(agreement)
            
            logger.info(f"Acordo {agreement.dados.numero_acordo} processado e publicado na fila")
            
            return AgreementResponse(
                message="Acordo recebido com sucesso",
                numero_acordo=agreement.dados.numero_acordo,
                operador=agreement.operador
            )
        except Exception as e:
            logger.error(f"Erro ao processar acordo: {str(e)}")
            raise


# Service instance
agreement_service = AgreementService()

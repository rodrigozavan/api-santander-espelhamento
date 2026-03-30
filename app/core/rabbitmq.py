"""RabbitMQ client for message queue operations."""
import pika
import json
import logging
from typing import Any
from app.core.config import get_settings

logger = logging.getLogger(__name__)


class RabbitMQClient:
    """Client to manage RabbitMQ connections and publications."""
    
    def __init__(self):
        self.connection = None
        self.channel = None
        self.settings = get_settings()
        
    def connect(self) -> None:
        """Establish connection with RabbitMQ."""
        try:
            credentials = pika.PlainCredentials(
                self.settings.RABBITMQ_USER, 
                self.settings.RABBITMQ_PASSWORD
            )
            parameters = pika.ConnectionParameters(
                host=self.settings.RABBITMQ_HOST,
                port=self.settings.RABBITMQ_PORT,
                virtual_host=self.settings.RABBITMQ_VHOST,
                credentials=credentials,
                heartbeat=600,
                blocked_connection_timeout=300
            )
            
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            
            # Declare queues
            self.channel.queue_declare(
                queue=self.settings.RABBITMQ_AGREEMENT_QUEUE, 
                durable=True
            )
            self.channel.queue_declare(
                queue=self.settings.RABBITMQ_DOCUMENT_QUEUE, 
                durable=True
            )
            
            logger.info("Conectado ao RabbitMQ com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao conectar ao RabbitMQ: {str(e)}")
            raise
    
    def disconnect(self) -> None:
        """Close RabbitMQ connection."""
        try:
            if self.channel and not self.channel.is_closed:
                self.channel.close()
            if self.connection and not self.connection.is_closed:
                self.connection.close()
            logger.info("Desconectado do RabbitMQ")
        except Exception as e:
            logger.error(f"Erro ao desconectar do RabbitMQ: {str(e)}")
    
    def is_connected(self) -> bool:
        """
        Check if RabbitMQ connection is active.
        
        Returns:
            True if connected and channel is open
        """
        try:
            return (
                self.connection is not None 
                and not self.connection.is_closed
                and self.channel is not None
                and not self.channel.is_closed
            )
        except Exception:
            return False
    
    def health_check(self) -> dict:
        """
        Perform health check on RabbitMQ connection.
        
        Returns:
            Dictionary with connection status
        """
        is_connected = self.is_connected()
        return {
            "rabbitmq_connected": is_connected,
            "host": self.settings.RABBITMQ_HOST,
            "port": self.settings.RABBITMQ_PORT,
        }
    
    def publish_message(self, queue_name: str, message: Any) -> bool:
        """
        Publish a message to a queue.
        
        Args:
            queue_name: Name of the queue
            message: Message to publish (will be converted to JSON)
            
        Returns:
            True if successful
            
        Raises:
            Exception: If publishing fails
        """
        try:
            # Check if connection is active
            if not self.connection or self.connection.is_closed:
                self.connect()
            
            # Convert Pydantic object to dict then to JSON
            if hasattr(message, 'model_dump'):
                message_dict = message.model_dump()
            else:
                message_dict = message
                
            message_body = json.dumps(message_dict, ensure_ascii=False)
            
            # Publish message
            self.channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=message_body,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                    content_type='application/json'
                )
            )
            
            logger.info(f"Mensagem publicada na fila {queue_name}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao publicar mensagem na fila {queue_name}: {str(e)}")
            # Try to reconnect
            try:
                self.connect()
            except:
                pass
            raise
    
    def publish_agreement(self, agreement: Any) -> bool:
        """Publish agreement data to specific queue."""
        return self.publish_message(self.settings.RABBITMQ_AGREEMENT_QUEUE, agreement)
    
    def publish_document(self, document: Any) -> bool:
        """Publish document data to specific queue."""
        return self.publish_message(self.settings.RABBITMQ_DOCUMENT_QUEUE, document)


# Global client instance
rabbitmq_client = RabbitMQClient()

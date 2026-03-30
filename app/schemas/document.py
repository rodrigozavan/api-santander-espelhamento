"""Document schemas for request/response validation."""
from pydantic import BaseModel, Field


class DocumentData(BaseModel):
    """Document file information."""
    filename: str = Field(..., description="Nome do arquivo")
    base64: str = Field(..., description="Conteúdo do arquivo codificado em base64")


class Document(BaseModel):
    """Document request schema."""
    numero_acordo: str = Field(..., description="Número do acordo relacionado")
    documento: str = Field(..., description="Tipo ou nome do documento")
    arquivo: DocumentData = Field(..., description="Dados do arquivo")


class DocumentResponse(BaseModel):
    """Document response schema."""
    message: str = Field(..., description="Mensagem de resposta")
    numero_acordo: str = Field(..., description="Número do acordo")
    filename: str = Field(..., description="Nome do arquivo")

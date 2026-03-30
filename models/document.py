from pydantic import BaseModel


class DocumentData(BaseModel):
    filename: str
    base64: str


class Document(BaseModel):
    numero_acordo: str
    documento: str
    arquivo: DocumentData

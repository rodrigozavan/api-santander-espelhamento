"""Agreement schemas for request/response validation."""
from pydantic import BaseModel, Field


class AgreementData(BaseModel):
    """Detailed agreement information."""
    nome: str = Field(..., description="Nome do cliente")
    documento: str = Field(..., description="Documento do cliente (CPF/CNPJ)")
    numero_acordo: str = Field(..., description="Número do acordo")
    meio_de_pagamento: str = Field(..., description="Meio de pagamento")
    iof: str = Field(..., description="Valor do IOF")
    taxa_de_juros: str = Field(..., description="Taxa de juros")
    taxa_cet: str = Field(..., description="Taxa CET")
    modalidade_do_desconto: str = Field(..., description="Modalidade do desconto")
    data_da_primeira_parcela: str = Field(..., description="Data da primeira parcela")
    vencimento_demais_parcelas: str = Field(..., description="Vencimento das demais parcelas")
    valor_total_da_divida: str = Field(..., description="Valor total da dívida")
    valor_do_desconto: str = Field(..., description="Valor do desconto")
    valor_para_pagamento: str = Field(..., description="Valor para pagamento")
    valor_negociado: str = Field(..., description="Valor negociado")
    quantidade_de_parcelas: str = Field(..., description="Quantidade de parcelas")
    valor_das_parcelas: str = Field(..., description="Valor das parcelas")
    data_da_entrada: str = Field(..., description="Data da entrada")
    valor_da_entrada: str = Field(..., description="Valor da entrada")


class Agreement(BaseModel):
    """Agreement request schema."""
    operador: str = Field(..., description="Identificador do operador")
    iniciado_em: str = Field(..., description="Data e hora de início")
    finalizado_em: str = Field(..., description="Data e hora de finalização")
    dados: AgreementData = Field(..., description="Dados completos do acordo")


class AgreementResponse(BaseModel):
    """Agreement response schema."""
    message: str = Field(..., description="Mensagem de resposta")
    numero_acordo: str = Field(..., description="Número do acordo")
    operador: str = Field(..., description="Identificador do operador")

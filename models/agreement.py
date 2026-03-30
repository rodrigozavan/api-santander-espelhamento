from pydantic import BaseModel


class AgreementData(BaseModel):
    nome: str
    documento: str
    numero_acordo: str
    meio_de_pagamento: str
    iof: str
    taxa_de_juros: str
    taxa_cet: str
    modalidade_do_desconto: str
    data_da_primeira_parcela: str
    vencimento_demais_parcelas: str
    valor_total_da_divida: str
    valor_do_desconto: str
    valor_para_pagamento: str
    valor_negociado: str
    quantidade_de_parcelas: str
    valor_das_parcelas: str
    data_da_entrada: str
    valor_da_entrada: str


class Agreement(BaseModel):
    operador: str
    iniciado_em: str
    finalizado_em: str
    dados: AgreementData
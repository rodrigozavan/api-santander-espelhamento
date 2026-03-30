# API Santander Espelhamento

API desenvolvida com FastAPI para receber dados de acordos e documentos e publicá-los em filas do RabbitMQ.

## Funcionalidades

- Receber dados de acordos via POST
- Receber documentos em base64 via POST
- Publicar automaticamente em filas do RabbitMQ:
  - `santander_varejo_return_agreements` - dados de acordos
  - `santander_varejo_return_billet` - dados de documentos

## Instalação

### 1. Clone o repositório

### 2. Crie um ambiente virtual

```bash
python -m venv .venv
```

### 3. Ative o ambiente virtual

**Windows PowerShell:**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -e .
```

### 5. Configure as variáveis de ambiente

Copie o arquivo de exemplo e configure suas credenciais:
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações.

## Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
API_KEY=sua-chave-secreta-aqui
API_VERSION=v1

# RabbitMQ Configuration
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_VHOST=/
RABBITMQ_AGREEMENT_QUEUE=santander_varejo_return_agreements
RABBITMQ_DOCUMENT_QUEUE=santander_varejo_return_billet
```

Você pode copiar o arquivo `.env.example` como base.

## Pré-requisitos

- Python 3.13+
- RabbitMQ Server rodando (localmente ou remoto)

### Instalação do RabbitMQ (Windows)

```powershell
# Usando Chocolatey
choco install rabbitmq

# Ou baixe diretamente de: https://www.rabbitmq.com/download.html
```

### Instalação do RabbitMQ (Docker)

```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

Acesse a interface de gerenciamento em: `http://localhost:15672` (usuário: guest, senha: guest)

## Executar a API

```bash
# Ativar o ambiente virtual
.venv\Scripts\Activate.ps1

# Executar a API
python main.py
```

Ou com uvicorn diretamente:

```bash
uvicorn main:app --reload
```

A API estará disponível em: `http://localhost:8000`

## Endpoints

### Health Check
- **GET** `/health`
- Verifica se a API está funcionando
- **Não requer autenticação**

### Criar Acordo
- **POST** `/api/v1/agreement`
- Recebe dados de um acordo e publica na fila `santander_varejo_return_agreements`
- **Requer autenticação via header `X-Api-Key`**

### Criar Documento
- **POST** `/api/v1/document`
- Recebe um documento em base64 e publica na fila `santander_varejo_return_billet`
- **Requer autenticação via header `X-Api-Key`**

## Autenticação

Os endpoints POST são protegidos por API Key. Você deve enviar o header `X-Api-Key` com a chave configurada no arquivo `.env`:

```bash
curl -X POST "http://localhost:8000/api/v1/agreement" \
  -H "X-Api-Key: sua-chave-secreta-aqui" \
  -H "Content-Type: application/json" \
  -d '{"operador": "teste", ...}'
```

## Documentação

Acesse a documentação interativa em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testes

A API inclui testes automatizados usando pytest.

### Instalar dependências de teste

```bash
pip install -e ".[dev]"
```

### Executar os testes

```bash
# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=app --cov-report=html

# Executar testes específicos
pytest tests/api/v1/test_health.py
pytest tests/api/v1/test_agreement.py -v
```

### Estrutura de Testes

```
tests/
├── conftest.py              # Fixtures e configuração
├── api/
│   └── v1/
│       ├── test_health.py
│       ├── test_agreement.py
│       └── test_document.py
└── services/                # Testes de serviços
```

## Arquitetura

### Estrutura do Projeto

A API segue as melhores práticas do FastAPI com separação clara de responsabilidades:

```
api-santander-espelhamento/
├── app/                        # Pacote principal da aplicação
│   ├── api/                    # Camada de API/Rotas
│   │   ├── v1/                 # Versão 1 da API
│   │   │   ├── endpoints/      # Endpoints individuais
│   │   │   │   ├── agreement.py
│   │   │   │   ├── document.py
│   │   │   │   └── health.py
│   │   │   └── router.py       # Agregador de rotas v1
│   │   └── dependencies.py     # Dependências compartilhadas
│   ├── core/                   # Configurações e utilitários core
│   │   ├── config.py           # Configurações da aplicação
│   │   ├── security.py         # Autenticação e segurança
│   │   └── rabbitmq.py         # Cliente RabbitMQ
│   ├── schemas/                # Schemas Pydantic (validação)
│   │   ├── agreement.py        # Schemas de acordo
│   │   ├── document.py         # Schemas de documento
│   │   └── health.py           # Schemas de health check
│   └── services/               # Lógica de negócio
│       ├── agreement_service.py
│       └── document_service.py
├── main.py                     # Ponto de entrada da aplicação
├── pyproject.toml              # Configuração do projeto
└── .env                        # Variáveis de ambiente (não versionado)
```

### Camadas da Aplicação

1. **API Layer** (`app/api/`): Define os endpoints HTTP e validações de entrada
2. **Service Layer** (`app/services/`): Implementa a lógica de negócio
3. **Core Layer** (`app/core/`): Configurações, segurança e clientes externos
4. **Schema Layer** (`app/schemas/`): Modelos Pydantic para validação de dados

### Fluxo de Dados

1. Cliente envia requisição POST para `/api/v1/agreement` ou `/api/v1/document`
2. API valida API Key
3. API valida dados recebidos usando Pydantic
4. API publica mensagem JSON na fila correspondente do RabbitMQ
5. API retorna confirmação ao cliente

### Filas RabbitMQ

- **santander_varejo_return_agreements**: Recebe todos os dados de acordos criados
- **santander_varejo_return_billet**: Recebe todos os documentos/boletos criados

As filas são declaradas como `durable=True` para persistência das mensagens.

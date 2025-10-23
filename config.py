#!/usr/bin/env python3
"""
Arquivo de configuração para o script de licitações PNCP
"""

# Configurações da API
API_BASE_URL = "https://pncp.gov.br/api"
API_TIMEOUT = 30

# Headers padrão para requisições
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# Configurações de paginação
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Configurações de exportação
EXPORT_FORMATS = ['excel', 'csv', 'json']
DEFAULT_EXCEL_ENGINE = 'openpyxl'
CSV_ENCODING = 'utf-8-sig'

# Filtros disponíveis
MODALIDADES_DISPONIVEIS = [
    "Pregão - Eletrônico",
    "Pregão Presencial", 
    "Credenciamento",
    "Concorrência",
    "Tomada de Preços",
    "Convite",
    "Concurso",
    "RDC - Regime Diferenciado de Contratações",
    "Leilão"
]

SITUACOES_DISPONIVEIS = [
    "Divulgada no PNCP",
    "Em Andamento",
    "Suspensa",
    "Cancelada",
    "Deserta",
    "Fracassada",
    "Homologada",
    "Adjudicada"
]

# Estados brasileiros
ESTADOS_BRASIL = {
    'AC': 'Acre',
    'AL': 'Alagoas', 
    'AP': 'Amapá',
    'AM': 'Amazonas',
    'BA': 'Bahia',
    'CE': 'Ceará',
    'DF': 'Distrito Federal',
    'ES': 'Espírito Santo',
    'GO': 'Goiás',
    'MA': 'Maranhão',
    'MT': 'Mato Grosso',
    'MS': 'Mato Grosso do Sul',
    'MG': 'Minas Gerais',
    'PA': 'Pará',
    'PB': 'Paraíba',
    'PR': 'Paraná',
    'PE': 'Pernambuco',
    'PI': 'Piauí',
    'RJ': 'Rio de Janeiro',
    'RN': 'Rio Grande do Norte',
    'RS': 'Rio Grande do Sul',
    'RO': 'Rondônia',
    'RR': 'Roraima',
    'SC': 'Santa Catarina',
    'SP': 'São Paulo',
    'SE': 'Sergipe',
    'TO': 'Tocantins'
}

# Configurações de logging
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'

# Configurações de retry
MAX_RETRIES = 3
RETRY_DELAY = 1  # segundos

# Configurações de cache (para futuras implementações)
CACHE_ENABLED = False
CACHE_TTL = 300  # segundos
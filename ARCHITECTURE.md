# Arquitetura

## 🏗️ Visão Geral

O Listador de Licitações PNCP é construído com uma arquitetura modular e extensível, projetada para ser robusta, escalável e fácil de manter.

## 📐 Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    Interface Layer                          │
├─────────────────────────────────────────────────────────────┤
│  CLI Interface  │  Web Interface  │  API Interface  │  GUI  │
├─────────────────────────────────────────────────────────────┤
│                    Business Logic Layer                     │
├─────────────────────────────────────────────────────────────┤
│  Main Controller  │  Data Processor  │  Export Manager     │
├─────────────────────────────────────────────────────────────┤
│                    Data Access Layer                       │
├─────────────────────────────────────────────────────────────┤
│  PNCP API Client  │  Web Scraper  │  File System  │  Cache │
├─────────────────────────────────────────────────────────────┤
│                    External Services                       │
├─────────────────────────────────────────────────────────────┤
│  PNCP Portal  │  File Storage  │  Logging  │  Monitoring  │
└─────────────────────────────────────────────────────────────┘
```

## 🧩 Componentes Principais

### 1. Interface Layer

#### CLI Interface (`main.py`)
- **Responsabilidade**: Interface de linha de comando
- **Tecnologias**: `argparse`, `sys`
- **Funcionalidades**:
  - Parsing de argumentos
  - Validação de entrada
  - Coordenação de operações
  - Tratamento de erros

#### Web Interface (Futuro)
- **Responsabilidade**: Interface web
- **Tecnologias**: `Flask`/`FastAPI`, `HTML`/`CSS`/`JavaScript`
- **Funcionalidades**:
  - Dashboard interativo
  - Formulários de busca
  - Visualização de dados
  - Exportação online

### 2. Business Logic Layer

#### Main Controller (`main.py`)
- **Responsabilidade**: Orquestração de operações
- **Funcionalidades**:
  - Seleção de método de busca
  - Coordenação entre componentes
  - Gerenciamento de fluxo
  - Tratamento de erros

#### Data Processor (`LicitacaoProcessor`)
- **Responsabilidade**: Processamento de dados
- **Funcionalidades**:
  - Formatação de dados
  - Validação de informações
  - Transformação de estruturas
  - Preparação para exportação

#### Export Manager (Integrado)
- **Responsabilidade**: Gerenciamento de exportação
- **Funcionalidades**:
  - Exportação para Excel
  - Exportação para CSV
  - Exportação para JSON
  - Validação de formatos

### 3. Data Access Layer

#### PNCP API Client (`pncp_licitacoes.py`)
- **Responsabilidade**: Acesso via API
- **Tecnologias**: `requests`, `json`
- **Funcionalidades**:
  - Requisições HTTP
  - Parsing de JSON
  - Tratamento de erros de API
  - Rate limiting

#### Web Scraper (`pncp_web_scraper.py`)
- **Responsabilidade**: Web scraping
- **Tecnologias**: `requests`, `BeautifulSoup`
- **Funcionalidades**:
  - Parsing de HTML
  - Extração de dados
  - Simulação de navegador
  - Tratamento de JavaScript

#### File System (Integrado)
- **Responsabilidade**: Gerenciamento de arquivos
- **Funcionalidades**:
  - Leitura de configurações
  - Escrita de logs
  - Salvamento de dados
  - Gerenciamento de cache

### 4. External Services

#### PNCP Portal
- **Responsabilidade**: Fonte de dados
- **Protocolo**: HTTP/HTTPS
- **Formato**: JSON/HTML
- **Rate Limit**: Conforme política do portal

#### File Storage
- **Responsabilidade**: Armazenamento local
- **Formatos**: Excel, CSV, JSON
- **Localização**: Sistema de arquivos local

## 🔄 Fluxo de Dados

### 1. Busca de Licitações

```
Usuário → CLI → Main Controller → Data Access Layer → PNCP Portal
                ↓
            Data Processor → Export Manager → File System
```

### 2. Processamento de Dados

```
Dados Brutos → Parser → Validator → Formatter → Exporter → Arquivo
```

### 3. Tratamento de Erros

```
Erro → Logger → Error Handler → User Feedback → Recovery
```

## 🛠️ Padrões de Design

### 1. Strategy Pattern
- **Implementação**: Diferentes métodos de busca (API vs Web Scraping)
- **Benefícios**: Flexibilidade e extensibilidade

### 2. Factory Pattern
- **Implementação**: Criação de processadores de dados
- **Benefícios**: Desacoplamento e reutilização

### 3. Observer Pattern
- **Implementação**: Sistema de notificações
- **Benefícios**: Loose coupling e reatividade

### 4. Template Method Pattern
- **Implementação**: Processamento de dados
- **Benefícios**: Consistência e reutilização

## 🔧 Configuração

### Variáveis de Ambiente
```bash
PNCP_API_URL=https://pncp.gov.br/api
PNCP_WEB_URL=https://pncp.gov.br
PNCP_TIMEOUT=30
DEFAULT_PAGE_SIZE=20
MAX_RETRIES=3
```

### Arquivo de Configuração
```python
# config.py
API_BASE_URL = "https://pncp.gov.br/api"
DEFAULT_HEADERS = {...}
MODALIDADES_DISPONIVEIS = [...]
```

## 📊 Monitoramento

### Logs
- **Nível**: INFO, WARNING, ERROR
- **Formato**: Estruturado (JSON)
- **Rotação**: Diária
- **Retenção**: 30 dias

### Métricas
- **Performance**: Tempo de resposta
- **Disponibilidade**: Uptime
- **Erros**: Taxa de erro
- **Uso**: Número de requisições

### Alertas
- **Erro de API**: Notificação imediata
- **Timeout**: Alerta após 3 tentativas
- **Rate Limit**: Aviso de limitação
- **Disco**: Espaço em disco baixo

## 🚀 Escalabilidade

### Horizontal
- **Load Balancer**: Distribuição de carga
- **Microserviços**: Separação de responsabilidades
- **Cache Distribuído**: Redis/Memcached
- **Message Queue**: Processamento assíncrono

### Vertical
- **CPU**: Processamento paralelo
- **Memória**: Cache em memória
- **Disco**: SSD para I/O
- **Rede**: Conexões otimizadas

## 🔒 Segurança

### Autenticação
- **API Keys**: Chaves de acesso
- **OAuth 2.0**: Autenticação moderna
- **JWT**: Tokens seguros
- **2FA**: Autenticação de dois fatores

### Autorização
- **RBAC**: Controle baseado em roles
- **ACL**: Listas de controle de acesso
- **Permissions**: Permissões granulares
- **Audit**: Logs de auditoria

### Criptografia
- **HTTPS**: Comunicação segura
- **TLS 1.3**: Protocolo moderno
- **AES-256**: Criptografia de dados
- **Hashing**: Senhas seguras

## 🧪 Testes

### Unitários
- **Cobertura**: 90%+
- **Frameworks**: `pytest`, `unittest`
- **Mocking**: `unittest.mock`
- **Fixtures**: Dados de teste

### Integração
- **APIs**: Testes de endpoints
- **Database**: Testes de persistência
- **External**: Mocks de serviços
- **E2E**: Testes end-to-end

### Performance
- **Load Testing**: Carga simulada
- **Stress Testing**: Limites do sistema
- **Memory Profiling**: Análise de memória
- **CPU Profiling**: Análise de CPU

## 📈 Evolução

### Versionamento
- **Semantic Versioning**: MAJOR.MINOR.PATCH
- **Changelog**: Histórico de mudanças
- **Migration**: Scripts de migração
- **Deprecation**: Avisos de descontinuação

### Backward Compatibility
- **API**: Manutenção de versões
- **Data**: Formato compatível
- **Configuration**: Configurações legadas
- **Migration**: Ferramentas de migração

### Future-Proofing
- **Modularity**: Arquitetura modular
- **Extensibility**: Fácil extensão
- **Standards**: Padrões abertos
- **Documentation**: Documentação completa

## 🔍 Troubleshooting

### Problemas Comuns
1. **Timeout**: Aumentar timeout
2. **Rate Limit**: Implementar retry
3. **Memory**: Otimizar processamento
4. **Network**: Verificar conectividade

### Debugging
- **Logs**: Análise de logs
- **Profiling**: Análise de performance
- **Monitoring**: Métricas em tempo real
- **Tracing**: Rastreamento de requisições

---

**Última atualização**: 17 de Janeiro de 2025
# Listador de Licitações PNCP

Script Python para listar e analisar licitações do Portal Nacional de Contratações Públicas (PNCP).

## 📋 Funcionalidades

- ✅ Busca licitações por diversos filtros (UF, município, órgão, modalidade, etc.)
- ✅ Busca por CNPJ específico
- ✅ Busca por município
- ✅ Exportação para Excel, CSV e JSON
- ✅ Formatação automática de datas e valores
- ✅ Interface de linha de comando intuitiva
- ✅ Tratamento de erros robusto

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/Thiag086/Licita-oes_geral.git
cd Licita-oes_geral
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 📖 Como Usar

### Uso Básico

```bash
# Listar todas as licitações (primeira página)
python pncp_licitacoes.py

# Buscar por UF
python pncp_licitacoes.py --uf PR

# Buscar por município
python pncp_licitacoes.py --municipio "Mandirituba" --uf PR

# Buscar por CNPJ
python pncp_licitacoes.py --cnpj 76105550000137
```

### Filtros Avançados

```bash
# Buscar por modalidade específica
python pncp_licitacoes.py --modalidade "Pregão - Eletrônico"

# Buscar por situação
python pncp_licitacoes.py --situacao "Divulgada no PNCP"

# Buscar por período
python pncp_licitacoes.py --data-inicio 2025-01-01 --data-fim 2025-12-31

# Combinar filtros
python pncp_licitacoes.py --uf PR --municipio "Mandirituba" --modalidade "Credenciamento"
```

### Paginação

```bash
# Especificar página e tamanho
python pncp_licitacoes.py --pagina 2 --tamanho 50
```

### Exportação de Dados

```bash
# Salvar em Excel
python pncp_licitacoes.py --uf PR --excel licitacoes_pr.xlsx

# Salvar em CSV
python pncp_licitacoes.py --municipio "Mandirituba" --csv licitacoes_mandirituba.csv

# Salvar em JSON
python pncp_licitacoes.py --cnpj 76105550000137 --json licitacoes_orgao.json

# Múltiplos formatos
python pncp_licitacoes.py --uf PR --excel pr.xlsx --csv pr.csv --json pr.json
```

## 📊 Estrutura dos Dados

O script extrai as seguintes informações principais de cada licitação:

- **Título**: Nome/título da licitação
- **Número PNCP**: Número de controle no PNCP
- **Órgão**: Nome do órgão responsável
- **Município**: Município da licitação
- **UF**: Unidade Federativa
- **Modalidade**: Tipo de modalidade (Pregão, Credenciamento, etc.)
- **Situação**: Status atual da licitação
- **Data Publicação**: Data de publicação no PNCP
- **Data Início Vigência**: Data de início da vigência
- **Data Fim Vigência**: Data de fim da vigência
- **Valor Global**: Valor total da licitação (quando disponível)
- **URL**: Link direto para a licitação no PNCP

## 🔧 Parâmetros Disponíveis

| Parâmetro | Descrição | Exemplo |
|-----------|-----------|---------|
| `--uf` | Unidade Federativa | `--uf PR` |
| `--municipio` | Nome do município | `--municipio "Mandirituba"` |
| `--orgao` | Nome do órgão | `--orgao "PREFEITURA"` |
| `--cnpj` | CNPJ do órgão | `--cnpj 76105550000137` |
| `--modalidade` | Modalidade de licitação | `--modalidade "Pregão"` |
| `--situacao` | Situação da licitação | `--situacao "Divulgada"` |
| `--data-inicio` | Data de início (YYYY-MM-DD) | `--data-inicio 2025-01-01` |
| `--data-fim` | Data de fim (YYYY-MM-DD) | `--data-fim 2025-12-31` |
| `--pagina` | Número da página | `--pagina 2` |
| `--tamanho` | Itens por página | `--tamanho 50` |
| `--excel` | Salvar em Excel | `--excel arquivo.xlsx` |
| `--csv` | Salvar em CSV | `--csv arquivo.csv` |
| `--json` | Salvar em JSON | `--json arquivo.json` |

## 📝 Exemplos Práticos

### Exemplo 1: Buscar licitações de um município específico
```bash
python pncp_licitacoes.py --municipio "Mandirituba" --uf PR --excel mandirituba.xlsx
```

### Exemplo 2: Buscar licitações de um órgão por CNPJ
```bash
python pncp_licitacoes.py --cnpj 76105550000137 --csv orgao.csv
```

### Exemplo 3: Buscar licitações de um período específico
```bash
python pncp_licitacoes.py --data-inicio 2025-01-01 --data-fim 2025-03-31 --json q1_2025.json
```

### Exemplo 4: Buscar licitações de uma modalidade específica
```bash
python pncp_licitacoes.py --modalidade "Credenciamento" --uf PR --excel credenciamentos_pr.xlsx
```

## 🛠️ Desenvolvimento

### Estrutura do Código

- `PNCPClient`: Classe para interação com a API do PNCP
- `LicitacaoProcessor`: Classe para processamento e formatação dos dados
- `main()`: Função principal com interface de linha de comando

### Adicionando Novos Filtros

Para adicionar novos filtros, modifique a função `buscar_licitacoes()` na classe `PNCPClient` e adicione o parâmetro correspondente no `argparse`.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abrir um Pull Request

## 📞 Suporte

Se encontrar algum problema ou tiver dúvidas, abra uma issue no repositório.

---

**Desenvolvido por:** Thiago  
**Repositório:** [Thiag086/Licita-oes_geral](https://github.com/Thiag086/Licita-oes_geral)
#!/bin/bash

# Script de instalação para o Listador de Licitações PNCP
# Autor: Thiago
# Repositório: Thiag086/Licita-oes_geral

echo "🚀 Instalando Listador de Licitações PNCP..."
echo "=============================================="

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.8 ou superior."
    exit 1
fi

echo "✅ Python 3 encontrado: $(python3 --version)"

# Verificar se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não encontrado. Por favor, instale pip3."
    exit 1
fi

echo "✅ pip3 encontrado"

# Instalar dependências
echo "📦 Instalando dependências..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependências instaladas com sucesso!"
else
    echo "❌ Erro ao instalar dependências"
    exit 1
fi

# Tornar scripts executáveis
chmod +x pncp_licitacoes.py
chmod +x pncp_web_scraper.py
chmod +x main.py
chmod +x exemplo_uso.py

echo "✅ Scripts tornados executáveis"

# Testar instalação
echo "🧪 Testando instalação..."
python3 main.py --exemplo --excel teste_instalacao.xlsx

if [ $? -eq 0 ]; then
    echo "✅ Instalação concluída com sucesso!"
    echo ""
    echo "📖 Como usar:"
    echo "  python3 main.py --help"
    echo "  python3 main.py --exemplo"
    echo "  python3 main.py --uf PR --excel licitacoes_pr.xlsx"
    echo ""
    echo "📚 Documentação completa em README.md"
else
    echo "❌ Erro durante o teste. Verifique as dependências."
    exit 1
fi
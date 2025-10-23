.PHONY: help install test clean build docker run

help: ## Mostrar esta mensagem de ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instalar dependências
	pip install -r requirements.txt

test: ## Executar testes
	python main.py --exemplo --excel test_output.xlsx
	python main.py --help

clean: ## Limpar arquivos temporários
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.xlsx" -delete
	find . -type f -name "*.csv" -delete
	find . -type f -name "*.json" -delete
	find . -type f -name "teste_*" -delete
	find . -type f -name "exemplo_*" -delete

build: ## Construir pacote
	python setup.py sdist bdist_wheel

docker: ## Construir imagem Docker
	docker build -t pncp-licitacoes .

run: ## Executar com Docker
	docker run --rm -v $(PWD)/output:/app/output pncp-licitacoes

dev: ## Executar em modo desenvolvimento
	python main.py --exemplo --excel output/licitacoes.xlsx

lint: ## Executar linter
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format: ## Formatar código
	black .
	isort .

all: clean install test ## Executar tudo: limpar, instalar, testar
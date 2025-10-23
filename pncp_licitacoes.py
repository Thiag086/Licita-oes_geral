#!/usr/bin/env python3
"""
Script para listar licitações do Portal Nacional de Contratações Públicas (PNCP)
Autor: Thiago
Repositório: Thiag086/Licita-oes_geral
"""

import requests
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import argparse
import sys


class PNCPClient:
    """Cliente para acessar a API do PNCP"""
    
    def __init__(self):
        self.base_url = "https://pncp.gov.br/api"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def buscar_licitacoes(self, 
                         uf: Optional[str] = None,
                         municipio: Optional[str] = None,
                         orgao: Optional[str] = None,
                         modalidade: Optional[str] = None,
                         situacao: Optional[str] = None,
                         data_inicio: Optional[str] = None,
                         data_fim: Optional[str] = None,
                         pagina: int = 1,
                         tamanho_pagina: int = 20) -> Dict:
        """
        Busca licitações no PNCP com filtros opcionais
        
        Args:
            uf: Unidade Federativa (ex: 'PR', 'SP')
            municipio: Nome do município
            orgao: Nome do órgão
            modalidade: Modalidade de licitação
            situacao: Situação da licitação
            data_inicio: Data de início (formato: YYYY-MM-DD)
            data_fim: Data de fim (formato: YYYY-MM-DD)
            pagina: Número da página
            tamanho_pagina: Quantidade de itens por página
        
        Returns:
            Dict com os dados das licitações
        """
        
        # URL da API de busca
        url = f"{self.base_url}/catalog/items"
        
        # Parâmetros da consulta
        params = {
            'page': pagina,
            'size': tamanho_pagina,
            'sort': 'data_publicacao_pncp,desc'
        }
        
        # Adicionar filtros se fornecidos
        if uf:
            params['uf'] = uf
        if municipio:
            params['municipio'] = municipio
        if orgao:
            params['orgao'] = orgao
        if modalidade:
            params['modalidade'] = modalidade
        if situacao:
            params['situacao'] = situacao
        if data_inicio:
            params['data_inicio'] = data_inicio
        if data_fim:
            params['data_fim'] = data_fim
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar licitações: {e}")
            return {"items": [], "total": 0}
    
    def buscar_por_cnpj(self, cnpj: str, pagina: int = 1, tamanho_pagina: int = 20) -> Dict:
        """
        Busca licitações por CNPJ do órgão
        
        Args:
            cnpj: CNPJ do órgão (apenas números)
            pagina: Número da página
            tamanho_pagina: Quantidade de itens por página
        
        Returns:
            Dict com os dados das licitações
        """
        return self.buscar_licitacoes(orgao=cnpj, pagina=pagina, tamanho_pagina=tamanho_pagina)
    
    def buscar_por_municipio(self, municipio: str, uf: str = None, pagina: int = 1, tamanho_pagina: int = 20) -> Dict:
        """
        Busca licitações por município
        
        Args:
            municipio: Nome do município
            uf: Unidade Federativa (opcional)
            pagina: Número da página
            tamanho_pagina: Quantidade de itens por página
        
        Returns:
            Dict com os dados das licitações
        """
        return self.buscar_licitacoes(municipio=municipio, uf=uf, pagina=pagina, tamanho_pagina=tamanho_pagina)


class LicitacaoProcessor:
    """Processador para analisar e formatar dados das licitações"""
    
    @staticmethod
    def formatar_data(data_str: str) -> str:
        """Formata data para exibição"""
        if not data_str:
            return "N/A"
        try:
            dt = datetime.fromisoformat(data_str.replace('Z', '+00:00'))
            return dt.strftime('%d/%m/%Y %H:%M')
        except:
            return data_str
    
    @staticmethod
    def extrair_informacoes_principais(licitacao: Dict) -> Dict:
        """Extrai informações principais de uma licitação"""
        return {
            'Título': licitacao.get('title', 'N/A'),
            'Número PNCP': licitacao.get('numero_controle_pncp', 'N/A'),
            'Órgão': licitacao.get('orgao_nome', 'N/A'),
            'Município': licitacao.get('municipio_nome', 'N/A'),
            'UF': licitacao.get('uf', 'N/A'),
            'Modalidade': licitacao.get('modalidade_licitacao_nome', 'N/A'),
            'Situação': licitacao.get('situacao_nome', 'N/A'),
            'Data Publicação': LicitacaoProcessor.formatar_data(licitacao.get('data_publicacao_pncp')),
            'Data Início Vigência': LicitacaoProcessor.formatar_data(licitacao.get('data_inicio_vigencia')),
            'Data Fim Vigência': LicitacaoProcessor.formatar_data(licitacao.get('data_fim_vigencia')),
            'Valor Global': f"R$ {licitacao.get('valor_global', 0):,.2f}" if licitacao.get('valor_global') else 'N/A',
            'URL': f"https://pncp.gov.br{licitacao.get('item_url', '')}"
        }
    
    @staticmethod
    def salvar_para_excel(licitacoes: List[Dict], nome_arquivo: str = None):
        """Salva licitações em arquivo Excel"""
        if not nome_arquivo:
            nome_arquivo = f"licitacoes_pncp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        # Converter para DataFrame
        dados_formatados = [LicitacaoProcessor.extrair_informacoes_principais(lic) for lic in licitacoes]
        df = pd.DataFrame(dados_formatados)
        
        # Salvar Excel
        df.to_excel(nome_arquivo, index=False, engine='openpyxl')
        print(f"Dados salvos em: {nome_arquivo}")
    
    @staticmethod
    def salvar_para_csv(licitacoes: List[Dict], nome_arquivo: str = None):
        """Salva licitações em arquivo CSV"""
        if not nome_arquivo:
            nome_arquivo = f"licitacoes_pncp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Converter para DataFrame
        dados_formatados = [LicitacaoProcessor.extrair_informacoes_principais(lic) for lic in licitacoes]
        df = pd.DataFrame(dados_formatados)
        
        # Salvar CSV
        df.to_csv(nome_arquivo, index=False, encoding='utf-8-sig')
        print(f"Dados salvos em: {nome_arquivo}")


def main():
    """Função principal do script"""
    parser = argparse.ArgumentParser(description='Listar licitações do PNCP')
    parser.add_argument('--uf', help='Unidade Federativa (ex: PR, SP)')
    parser.add_argument('--municipio', help='Nome do município')
    parser.add_argument('--orgao', help='Nome do órgão')
    parser.add_argument('--cnpj', help='CNPJ do órgão')
    parser.add_argument('--modalidade', help='Modalidade de licitação')
    parser.add_argument('--situacao', help='Situação da licitação')
    parser.add_argument('--data-inicio', help='Data de início (YYYY-MM-DD)')
    parser.add_argument('--data-fim', help='Data de fim (YYYY-MM-DD)')
    parser.add_argument('--pagina', type=int, default=1, help='Número da página')
    parser.add_argument('--tamanho', type=int, default=20, help='Itens por página')
    parser.add_argument('--excel', help='Salvar em Excel (nome do arquivo)')
    parser.add_argument('--csv', help='Salvar em CSV (nome do arquivo)')
    parser.add_argument('--json', help='Salvar em JSON (nome do arquivo)')
    
    args = parser.parse_args()
    
    # Inicializar cliente PNCP
    client = PNCPClient()
    processor = LicitacaoProcessor()
    
    # Buscar licitações
    if args.cnpj:
        resultado = client.buscar_por_cnpj(args.cnpj, args.pagina, args.tamanho)
    elif args.municipio:
        resultado = client.buscar_por_municipio(args.municipio, args.uf, args.pagina, args.tamanho)
    else:
        resultado = client.buscar_licitacoes(
            uf=args.uf,
            municipio=args.municipio,
            orgao=args.orgao,
            modalidade=args.modalidade,
            situacao=args.situacao,
            data_inicio=args.data_inicio,
            data_fim=args.data_fim,
            pagina=args.pagina,
            tamanho_pagina=args.tamanho
        )
    
    licitacoes = resultado.get('items', [])
    total = resultado.get('total', 0)
    
    print(f"\n=== RESULTADOS DA BUSCA ===")
    print(f"Total de licitações encontradas: {total}")
    print(f"Página atual: {args.pagina}")
    print(f"Itens por página: {args.tamanho}")
    print(f"Exibindo: {len(licitacoes)} licitações\n")
    
    # Exibir licitações
    for i, licitacao in enumerate(licitacoes, 1):
        info = processor.extrair_informacoes_principais(licitacao)
        print(f"--- LICITAÇÃO {i} ---")
        for chave, valor in info.items():
            print(f"{chave}: {valor}")
        print()
    
    # Salvar em arquivos se solicitado
    if args.excel:
        processor.salvar_para_excel(licitacoes, args.excel)
    
    if args.csv:
        processor.salvar_para_csv(licitacoes, args.csv)
    
    if args.json:
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)
        print(f"Dados salvos em: {args.json}")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Script alternativo para listar licitações do PNCP usando web scraping
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
from bs4 import BeautifulSoup
import time
import re


class PNCPWebScraper:
    """Scraper para acessar dados do PNCP via web scraping"""
    
    def __init__(self):
        self.base_url = "https://pncp.gov.br"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def buscar_licitacoes_por_filtros(self, 
                                    uf: Optional[str] = None,
                                    municipio: Optional[str] = None,
                                    orgao: Optional[str] = None,
                                    modalidade: Optional[str] = None,
                                    situacao: Optional[str] = None,
                                    data_inicio: Optional[str] = None,
                                    data_fim: Optional[str] = None) -> List[Dict]:
        """
        Busca licitações usando web scraping com filtros
        """
        licitacoes = []
        
        try:
            # URL de busca do PNCP
            search_url = f"{self.base_url}/pesquisa"
            
            # Parâmetros de busca
            params = {}
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
            
            response = self.session.get(search_url, params=params, timeout=30)
            response.raise_for_status()
            
            # Parse do HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Procurar por elementos que contenham dados de licitações
            # (isso pode variar dependendo da estrutura atual do site)
            licitacao_elements = soup.find_all(['div', 'tr', 'li'], class_=re.compile(r'licitacao|item|resultado'))
            
            for element in licitacao_elements:
                licitacao_data = self._extrair_dados_licitacao(element)
                if licitacao_data:
                    licitacoes.append(licitacao_data)
            
            # Se não encontrou elementos específicos, tentar buscar em tabelas
            if not licitacoes:
                tables = soup.find_all('table')
                for table in tables:
                    rows = table.find_all('tr')
                    for row in rows[1:]:  # Pular cabeçalho
                        licitacao_data = self._extrair_dados_licitacao_tabela(row)
                        if licitacao_data:
                            licitacoes.append(licitacao_data)
            
        except Exception as e:
            print(f"Erro ao buscar licitações: {e}")
        
        return licitacoes
    
    def _extrair_dados_licitacao(self, element) -> Optional[Dict]:
        """Extrai dados de licitação de um elemento HTML"""
        try:
            # Procurar por links que possam ser licitações
            link = element.find('a')
            if not link:
                return None
            
            # Extrair informações básicas
            titulo = link.get_text(strip=True)
            url = link.get('href', '')
            
            if not titulo or 'licitacao' not in titulo.lower():
                return None
            
            # Procurar por outras informações no elemento pai
            parent = element.parent if element.parent else element
            
            # Extrair data se disponível
            data_text = parent.find(text=re.compile(r'\d{2}/\d{2}/\d{4}'))
            data_publicacao = data_text.strip() if data_text else None
            
            # Extrair órgão se disponível
            orgao_text = parent.find(text=re.compile(r'[A-Z]{2,}'))
            orgao = orgao_text.strip() if orgao_text else None
            
            return {
                'title': titulo,
                'item_url': url,
                'orgao_nome': orgao,
                'data_publicacao_pncp': data_publicacao,
                'municipio_nome': None,
                'uf': None,
                'modalidade_licitacao_nome': None,
                'situacao_nome': None,
                'numero_controle_pncp': None,
                'valor_global': None
            }
            
        except Exception:
            return None
    
    def _extrair_dados_licitacao_tabela(self, row) -> Optional[Dict]:
        """Extrai dados de licitação de uma linha de tabela"""
        try:
            cells = row.find_all(['td', 'th'])
            if len(cells) < 2:
                return None
            
            # Assumir estrutura básica de tabela
            titulo = cells[0].get_text(strip=True)
            link = cells[0].find('a')
            url = link.get('href', '') if link else ''
            
            orgao = cells[1].get_text(strip=True) if len(cells) > 1 else None
            data = cells[2].get_text(strip=True) if len(cells) > 2 else None
            
            return {
                'title': titulo,
                'item_url': url,
                'orgao_nome': orgao,
                'data_publicacao_pncp': data,
                'municipio_nome': None,
                'uf': None,
                'modalidade_licitacao_nome': None,
                'situacao_nome': None,
                'numero_controle_pncp': None,
                'valor_global': None
            }
            
        except Exception:
            return None
    
    def buscar_licitacoes_dados_exemplo(self) -> List[Dict]:
        """
        Retorna os dados de exemplo fornecidos pelo usuário
        para demonstração do script
        """
        return [
            {
                "id": "33eef20234def233056514e1dec9915e",
                "index": "catalog2",
                "doc_type": "_doc",
                "title": "Edital nº 90039/2025",
                "description": "Registro de preços para futuras e eventuais aquisições de eletrodomésticos, eletrônicos e utensílios de cozinha",
                "item_url": "/compras/76105550000137/2025/85",
                "document_type": "edital",
                "createdAt": "2025-10-17T07:42:39.162889",
                "numero": None,
                "ano": "2025",
                "numero_sequencial": "85",
                "numero_sequencial_compra_ata": None,
                "numero_controle_pncp": "76105550000137-1-000085/2025",
                "orgao_id": "38904",
                "orgao_cnpj": "76105550000137",
                "orgao_nome": "MUNICIPIO DE MANDIRITUBA",
                "orgao_subrogado_id": None,
                "orgao_subrogado_nome": None,
                "unidade_id": "58391",
                "unidade_codigo": "455978",
                "unidade_nome": "PREFEITURA MUNICIPAL DE MANDIRITUBA - PR",
                "esfera_id": "M",
                "esfera_nome": "Municipal",
                "poder_id": "N",
                "poder_nome": "Não se aplica",
                "municipio_id": "4111",
                "municipio_nome": "Mandirituba",
                "uf": "PR",
                "modalidade_licitacao_id": "6",
                "modalidade_licitacao_nome": "Pregão - Eletrônico",
                "situacao_id": "1",
                "situacao_nome": "Divulgada no PNCP",
                "data_publicacao_pncp": "2025-09-24T07:28:16.330332",
                "data_atualizacao_pncp": "2025-10-17T07:42:39.136772030",
                "data_assinatura": None,
                "data_inicio_vigencia": "2025-09-24T08:00",
                "data_fim_vigencia": "2025-10-30T09:00",
                "cancelado": False,
                "valor_global": None,
                "tem_resultado": False,
                "tipo_id": "1",
                "tipo_nome": "Edital",
                "tipo_contrato_id": None,
                "tipo_contrato_nome": None,
                "fonte_orcamentaria": None,
                "fonte_orcamentaria_id": None,
                "fonte_orcamentaria_nome": None,
                "exigencia_conteudo_nacional": False,
                "tipo_margem_preferencia": None,
                "tipo_margem_preferencia_id": None,
                "tipo_margem_preferencia_nome": None
            },
            {
                "id": "7ea0d533ca27d20107d9ef5a06821ad5",
                "index": "catalog2",
                "doc_type": "_doc",
                "title": "Edital de Chamamento Público nº 1/2025",
                "description": "Credenciamento de Agências de Viagens e Turismo, objetivando o menor preço por grupo no dia da cotação, para reserva de hotéis e aquisição de passagens aéreas, incluindo cotação, reserva, emissão, entrega, transferência, endosso, marcação/remarcação e reembolso de bilhetes de passagens aéreas para trechos nacionais",
                "item_url": "/compras/00942395000141/2025/10",
                "document_type": "edital",
                "createdAt": "2025-08-15T16:12:04.256732",
                "numero": None,
                "ano": "2025",
                "numero_sequencial": "10",
                "numero_sequencial_compra_ata": None,
                "numero_controle_pncp": "00942395000141-1-000010/2025",
                "orgao_id": "48015",
                "orgao_cnpj": "00942395000141",
                "orgao_nome": "CAMARA MUNICIPAL DE MANDIRITUBA",
                "orgao_subrogado_id": None,
                "orgao_subrogado_nome": None,
                "unidade_id": "2455820",
                "unidade_codigo": "930228",
                "unidade_nome": "CAMARA MUNICIPAL DE MANDIRITUBA - PR",
                "esfera_id": "M",
                "esfera_nome": "Municipal",
                "poder_id": "L",
                "poder_nome": "Legislativo",
                "municipio_id": "4111",
                "municipio_nome": "Mandirituba",
                "uf": "PR",
                "modalidade_licitacao_id": "12",
                "modalidade_licitacao_nome": "Credenciamento",
                "situacao_id": "1",
                "situacao_nome": "Divulgada no PNCP",
                "data_publicacao_pncp": "2025-08-15T16:12:02.065839",
                "data_atualizacao_pncp": "2025-08-15T16:12:02.065839",
                "data_assinatura": None,
                "data_inicio_vigencia": "2025-08-19T08:00",
                "data_fim_vigencia": "2026-08-19T08:00",
                "cancelado": False,
                "valor_global": None,
                "tem_resultado": False,
                "tipo_id": "4",
                "tipo_nome": "Edital de Chamamento Público",
                "tipo_contrato_id": None,
                "tipo_contrato_nome": None,
                "fonte_orcamentaria": None,
                "fonte_orcamentaria_id": None,
                "fonte_orcamentaria_nome": None,
                "exigencia_conteudo_nacional": False,
                "tipo_margem_preferencia": None,
                "tipo_margem_preferencia_id": None,
                "tipo_margem_preferencia_nome": None
            },
            {
                "id": "865c14e7edc4768d63dc2ec5f8dba240",
                "index": "catalog2",
                "doc_type": "_doc",
                "title": "Edital de Chamamento Público nº 1/2026",
                "description": "CREDENCIAMENTO DE PESSOA(S) FÍSICA(S), EMPRESÁRIOS UNIPESSOAL (SLU) E PESSOA(S) JURÍDICA(S) PARA PRESTAÇÃO DOS SEGUINTES SERVIÇOS: PEDIATRIA, PSIQUIATRIA, NEUROLOGIA, NEUROPEDIATRIA, GINECOLOGIA, ENFERMAGEM E PLANTÕES MÉDICOS (CLÍNICO GERAL), MÉDICO CLINICO GERAL, PLANTÕES DE ENFERMEIROS, PLANTÕES DE TÉCNICOS EM ENFERMAGEM, A SEREM REALIZADOS NO HOSPITAL MUNICIPAL DE MANDIRITUBA (AMBULATÓRIO E UNIDADE DE PRONTO ATENDIMENTO) 24 HORAS, POLICLÍNICA MUNICIPAL E CENTRO DE ATENÇÃO PSICOSSOCIAL (CAPS).",
                "item_url": "/compras/76105550000137/2026/1",
                "document_type": "edital",
                "createdAt": "2025-03-31T15:20:47.325071",
                "numero": None,
                "ano": "2026",
                "numero_sequencial": "1",
                "numero_sequencial_compra_ata": None,
                "numero_controle_pncp": "76105550000137-1-000001/2026",
                "orgao_id": "38904",
                "orgao_cnpj": "76105550000137",
                "orgao_nome": "MUNICIPIO DE MANDIRITUBA",
                "orgao_subrogado_id": None,
                "orgao_subrogado_nome": None,
                "unidade_id": "58391",
                "unidade_codigo": "455978",
                "unidade_nome": "PREFEITURA MUNICIPAL DE MANDIRITUBA - PR",
                "esfera_id": "M",
                "esfera_nome": "Municipal",
                "poder_id": "N",
                "poder_nome": "Não se aplica",
                "municipio_id": "4111",
                "municipio_nome": "Mandirituba",
                "uf": "PR",
                "modalidade_licitacao_id": "12",
                "modalidade_licitacao_nome": "Credenciamento",
                "situacao_id": "1",
                "situacao_nome": "Divulgada no PNCP",
                "data_publicacao_pncp": "2025-03-31T15:20:00.784926",
                "data_atualizacao_pncp": "2025-03-31T15:20:00.784926",
                "data_assinatura": None,
                "data_inicio_vigencia": "2025-04-01T08:00",
                "data_fim_vigencia": "2025-12-31T18:00",
                "cancelado": False,
                "valor_global": None,
                "tem_resultado": False,
                "tipo_id": "4",
                "tipo_nome": "Edital de Chamamento Público",
                "tipo_contrato_id": None,
                "tipo_contrato_nome": None,
                "fonte_orcamentaria": "",
                "fonte_orcamentaria_id": "",
                "fonte_orcamentaria_nome": "",
                "exigencia_conteudo_nacional": False,
                "tipo_margem_preferencia": "",
                "tipo_margem_preferencia_id": "",
                "tipo_margem_preferencia_nome": ""
            }
        ]


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
    parser = argparse.ArgumentParser(description='Listar licitações do PNCP (Web Scraper)')
    parser.add_argument('--uf', help='Unidade Federativa (ex: PR, SP)')
    parser.add_argument('--municipio', help='Nome do município')
    parser.add_argument('--orgao', help='Nome do órgão')
    parser.add_argument('--modalidade', help='Modalidade de licitação')
    parser.add_argument('--situacao', help='Situação da licitação')
    parser.add_argument('--data-inicio', help='Data de início (YYYY-MM-DD)')
    parser.add_argument('--data-fim', help='Data de fim (YYYY-MM-DD)')
    parser.add_argument('--excel', help='Salvar em Excel (nome do arquivo)')
    parser.add_argument('--csv', help='Salvar em CSV (nome do arquivo)')
    parser.add_argument('--json', help='Salvar em JSON (nome do arquivo)')
    parser.add_argument('--exemplo', action='store_true', help='Usar dados de exemplo')
    
    args = parser.parse_args()
    
    # Inicializar scraper e processador
    scraper = PNCPWebScraper()
    processor = LicitacaoProcessor()
    
    # Buscar licitações
    if args.exemplo:
        print("Usando dados de exemplo...")
        licitacoes = scraper.buscar_licitacoes_dados_exemplo()
    else:
        licitacoes = scraper.buscar_licitacoes_por_filtros(
            uf=args.uf,
            municipio=args.municipio,
            orgao=args.orgao,
            modalidade=args.modalidade,
            situacao=args.situacao,
            data_inicio=args.data_inicio,
            data_fim=args.data_fim
        )
    
    print(f"\n=== RESULTADOS DA BUSCA ===")
    print(f"Total de licitações encontradas: {len(licitacoes)}")
    print()
    
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
            json.dump({"items": licitacoes, "total": len(licitacoes)}, f, ensure_ascii=False, indent=2)
        print(f"Dados salvos em: {args.json}")


if __name__ == "__main__":
    main()
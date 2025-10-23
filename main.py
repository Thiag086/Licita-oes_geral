#!/usr/bin/env python3
"""
Script principal para listar licitações do PNCP
Combina API e web scraping para máxima compatibilidade
Autor: Thiago
Repositório: Thiag086/Licita-oes_geral
"""

import argparse
import sys
from pncp_licitacoes import PNCPClient, LicitacaoProcessor
from pncp_web_scraper import PNCPWebScraper


def main():
    """Função principal que escolhe o melhor método de busca"""
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
    parser.add_argument('--exemplo', action='store_true', help='Usar dados de exemplo')
    parser.add_argument('--metodo', choices=['api', 'web', 'auto'], default='auto', 
                       help='Método de busca: api, web ou auto (padrão)')
    
    args = parser.parse_args()
    
    processor = LicitacaoProcessor()
    licitacoes = []
    
    if args.exemplo:
        print("Usando dados de exemplo...")
        scraper = PNCPWebScraper()
        licitacoes = scraper.buscar_licitacoes_dados_exemplo()
    else:
        # Tentar API primeiro se método for 'auto' ou 'api'
        if args.metodo in ['api', 'auto']:
            try:
                print("Tentando buscar via API...")
                client = PNCPClient()
                
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
                if licitacoes:
                    print(f"✓ API funcionou! Encontradas {len(licitacoes)} licitações")
                else:
                    print("⚠ API não retornou dados")
                    
            except Exception as e:
                print(f"✗ Erro na API: {e}")
                licitacoes = []
        
        # Se API falhou e método é 'auto' ou 'web', tentar web scraping
        if not licitacoes and args.metodo in ['web', 'auto']:
            try:
                print("Tentando buscar via web scraping...")
                scraper = PNCPWebScraper()
                licitacoes = scraper.buscar_licitacoes_por_filtros(
                    uf=args.uf,
                    municipio=args.municipio,
                    orgao=args.orgao,
                    modalidade=args.modalidade,
                    situacao=args.situacao,
                    data_inicio=args.data_inicio,
                    data_fim=args.data_fim
                )
                
                if licitacoes:
                    print(f"✓ Web scraping funcionou! Encontradas {len(licitacoes)} licitações")
                else:
                    print("⚠ Web scraping não retornou dados")
                    
            except Exception as e:
                print(f"✗ Erro no web scraping: {e}")
                licitacoes = []
    
    # Exibir resultados
    print(f"\n=== RESULTADOS DA BUSCA ===")
    print(f"Total de licitações encontradas: {len(licitacoes)}")
    print()
    
    if licitacoes:
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
            import json
            with open(args.json, 'w', encoding='utf-8') as f:
                json.dump({"items": licitacoes, "total": len(licitacoes)}, f, ensure_ascii=False, indent=2)
            print(f"Dados salvos em: {args.json}")
    else:
        print("Nenhuma licitação encontrada com os filtros especificados.")
        print("\nDicas:")
        print("- Use --exemplo para ver dados de demonstração")
        print("- Verifique se os filtros estão corretos")
        print("- Tente usar --metodo web para web scraping")
        print("- Tente usar --metodo api para API (se disponível)")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import sys
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional


ISO_DATE_FIELDS = {
    "data_publicacao_pncp",
    "data_atualizacao_pncp",
    "data_assinatura",
    "data_inicio_vigencia",
    "data_fim_vigencia",
}


@dataclass
class CliOptions:
    input_path: str
    output_format: str
    search_text: Optional[str]
    filter_uf: Optional[str]
    filter_municipio: Optional[str]
    filter_modalidade: Optional[str]
    filter_situacao: Optional[str]
    filter_orgao: Optional[str]
    filter_ano: Optional[str]
    limit: int
    sort_by: str
    sort_desc: bool


def parse_args() -> CliOptions:
    parser = argparse.ArgumentParser(
        description="Listar licitações do PNCP a partir de um arquivo JSON"
    )
    parser.add_argument(
        "-i",
        "--input",
        dest="input_path",
        required=True,
        help='Caminho para o JSON (objeto com campo "items" ou lista).',
    )
    parser.add_argument(
        "-f",
        "--format",
        dest="output_format",
        choices=["list", "table", "json", "csv"],
        default="list",
        help="Formato de saída (padrão: list)",
    )
    parser.add_argument(
        "-s",
        "--search",
        dest="search_text",
        help="Busca (case-insensitive) em título, descrição, órgão e município",
    )
    parser.add_argument("--uf", dest="filter_uf", help="Filtrar por UF (ex: PR)")
    parser.add_argument(
        "--municipio", dest="filter_municipio", help="Filtrar por Município (contém)"
    )
    parser.add_argument(
        "--modalidade",
        dest="filter_modalidade",
        help="Filtrar por Modalidade (contém)",
    )
    parser.add_argument(
        "--situacao",
        dest="filter_situacao",
        help="Filtrar por Situação (contém)",
    )
    parser.add_argument("--orgao", dest="filter_orgao", help="Filtrar por Órgão (contém)")
    parser.add_argument("--ano", dest="filter_ano", help="Filtrar por Ano (exato)")
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Limitar quantidade de resultados (0 = sem limite)",
    )
    parser.add_argument(
        "--sort-by",
        dest="sort_by",
        default="data_publicacao_pncp",
        help="Campo de ordenação (padrão: data_publicacao_pncp)",
    )
    parser.add_argument(
        "--desc",
        dest="sort_desc",
        action="store_true",
        help="Ordenar em ordem decrescente",
    )

    args = parser.parse_args()
    return CliOptions(
        input_path=args.input_path,
        output_format=args.output_format,
        search_text=args.search_text,
        filter_uf=args.filter_uf,
        filter_municipio=args.filter_municipio,
        filter_modalidade=args.filter_modalidade,
        filter_situacao=args.filter_situacao,
        filter_orgao=args.filter_orgao,
        filter_ano=args.filter_ano,
        limit=args.limit,
        sort_by=args.sort_by,
        sort_desc=args.sort_desc,
    )


def load_items_from_file(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "items" in data and isinstance(data["items"], list):
        return data["items"]
    if isinstance(data, list):
        return data
    raise ValueError(
        "JSON inválido: deve ser uma lista ou um objeto com campo 'items' (lista)"
    )


def normalize_text(value: Optional[Any]) -> str:
    if value is None:
        return ""
    return str(value)


def contains_filter(value: Optional[Any], term: Optional[str]) -> bool:
    if term is None or term == "":
        return True
    return term.lower() in normalize_text(value).lower()


def build_full_url(item: Dict[str, Any]) -> str:
    relative = normalize_text(item.get("item_url"))
    if relative.startswith("http://") or relative.startswith("https://"):
        return relative
    if relative and not relative.startswith("/"):
        relative = "/" + relative
    return f"https://pncp.gov.br{relative}" if relative else ""


def try_parse_iso_datetime(value: Any) -> Optional[datetime]:
    s = normalize_text(value).strip()
    if not s:
        return None
    # Handle 'Z' timezone if present
    if s.endswith("Z"):
        s = s.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None


def sort_key(item: Dict[str, Any], key: str):
    value = item.get(key)
    if key in ISO_DATE_FIELDS or (isinstance(value, str) and "T" in value):
        dt = try_parse_iso_datetime(value)
        if dt is not None:
            return dt
    return normalize_text(value)


def filter_items(items: Iterable[Dict[str, Any]], options: CliOptions) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    search_term = options.search_text.lower() if options.search_text else None

    for item in items:
        if options.filter_uf and normalize_text(item.get("uf")).upper() != options.filter_uf.upper():
            continue
        if not contains_filter(item.get("municipio_nome"), options.filter_municipio):
            continue
        if not contains_filter(
            item.get("modalidade_licitacao_nome"), options.filter_modalidade
        ):
            continue
        if not contains_filter(item.get("situacao_nome"), options.filter_situacao):
            continue
        if not contains_filter(item.get("orgao_nome"), options.filter_orgao):
            continue
        if options.filter_ano and normalize_text(item.get("ano")) != options.filter_ano:
            continue

        if search_term:
            compound = " ".join(
                [
                    normalize_text(item.get("title")),
                    normalize_text(item.get("description")),
                    normalize_text(item.get("orgao_nome")),
                    normalize_text(item.get("municipio_nome")),
                ]
            ).lower()
            if search_term not in compound:
                continue

        results.append(item)

    results.sort(key=lambda it: sort_key(it, options.sort_by), reverse=options.sort_desc)

    if options.limit and options.limit > 0:
        results = results[: options.limit]

    return results


def truncate(text: str, max_len: int) -> str:
    if len(text) <= max_len:
        return text
    if max_len <= 1:
        return text[:max_len]
    return text[: max_len - 1] + "\N{HORIZONTAL ELLIPSIS}"


def fmt_date(value: Any) -> str:
    dt = try_parse_iso_datetime(value)
    return dt.strftime("%Y-%m-%d %H:%M") if dt else ""


def print_list(items: List[Dict[str, Any]]):
    for item in items:
        title = normalize_text(item.get("title"))
        tipo = normalize_text(item.get("tipo_nome"))
        modalidade = normalize_text(item.get("modalidade_licitacao_nome"))
        situacao = normalize_text(item.get("situacao_nome"))
        orgao = normalize_text(item.get("orgao_nome"))
        mun = normalize_text(item.get("municipio_nome"))
        uf = normalize_text(item.get("uf"))
        ano = normalize_text(item.get("ano"))
        seq = normalize_text(item.get("numero_sequencial"))
        inicio = fmt_date(item.get("data_inicio_vigencia"))
        fim = fmt_date(item.get("data_fim_vigencia"))
        url = build_full_url(item)

        print(f"{title} ({tipo}, {modalidade})")
        print(
            f"- Situação: {situacao} | Órgão: {orgao} | {mun}/{uf} | Ano: {ano} | Seq: {seq}"
        )
        print(f"- Vigência: {inicio} → {fim}")
        print(f"- URL: {url}")
        print()


def print_table(items: List[Dict[str, Any]]):
    # Define colunas essenciais e larguras máximas para melhor leitura em terminal
    columns = [
        ("ano", "Ano", 4),
        ("tipo_nome", "Tipo", 20),
        ("modalidade_licitacao_nome", "Modalidade", 22),
        ("situacao_nome", "Situação", 22),
        ("orgao_nome", "Órgão", 32),
        ("munuf", "Mun/UF", 22),
        ("title", "Título", 60),
        ("data_inicio_vigencia", "Início", 16),
        ("data_fim_vigencia", "Fim", 16),
        ("url", "URL", 60),
    ]

    def row_values(item: Dict[str, Any]) -> List[str]:
        munuf = f"{normalize_text(item.get('municipio_nome'))}/{normalize_text(item.get('uf'))}"
        values = {
            "ano": normalize_text(item.get("ano")),
            "tipo_nome": normalize_text(item.get("tipo_nome")),
            "modalidade_licitacao_nome": normalize_text(
                item.get("modalidade_licitacao_nome")
            ),
            "situacao_nome": normalize_text(item.get("situacao_nome")),
            "orgao_nome": normalize_text(item.get("orgao_nome")),
            "munuf": munuf,
            "title": normalize_text(item.get("title")),
            "data_inicio_vigencia": fmt_date(item.get("data_inicio_vigencia")),
            "data_fim_vigencia": fmt_date(item.get("data_fim_vigencia")),
            "url": build_full_url(item),
        }
        return [values[key] for key, _, _ in columns]

    # Header
    headers = [header for _, header, _ in columns]
    widths = [width for _, _, width in columns]
    header_line = " | ".join(
        truncate(headers[i], widths[i]).ljust(widths[i]) for i in range(len(headers))
    )
    sep_line = "-+-".join("-" * w for w in widths)
    print(header_line)
    print(sep_line)

    for item in items:
        values = row_values(item)
        line = " | ".join(
            truncate(values[i], widths[i]).ljust(widths[i]) for i in range(len(values))
        )
        print(line)


def print_json(items: List[Dict[str, Any]]):
    print(json.dumps(items, ensure_ascii=False, indent=2))


def print_csv(items: List[Dict[str, Any]]):
    fieldnames = [
        "id",
        "title",
        "description",
        "ano",
        "numero_sequencial",
        "numero_controle_pncp",
        "orgao_nome",
        "orgao_cnpj",
        "municipio_nome",
        "uf",
        "modalidade_licitacao_nome",
        "situacao_nome",
        "data_publicacao_pncp",
        "data_atualizacao_pncp",
        "data_inicio_vigencia",
        "data_fim_vigencia",
        "valor_global",
        "tipo_nome",
        "item_url",
        "url",
    ]

    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=fieldnames,
        extrasaction="ignore",
        lineterminator="\n",
    )
    writer.writeheader()
    for item in items:
        row = dict(item)
        row["url"] = build_full_url(item)
        writer.writerow(row)


def main():
    options = parse_args()
    all_items = load_items_from_file(options.input_path)
    filtered = filter_items(all_items, options)

    if options.output_format == "list":
        print_list(filtered)
    elif options.output_format == "table":
        print_table(filtered)
    elif options.output_format == "json":
        print_json(filtered)
    elif options.output_format == "csv":
        print_csv(filtered)
    else:
        raise ValueError(f"Formato de saída não suportado: {options.output_format}")


if __name__ == "__main__":
    main()

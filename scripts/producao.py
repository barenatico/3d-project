#!/usr/bin/env python3
"""
CLI de gestao de producao para impressao 3D.

Impressoras: 4x Bambu Lab A1
Produtos: Botao Tarefas, Blocos Lego 0.4, Blocos Lego 0.8
"""

import argparse
import math
import sys

# ---------------------------------------------------------------------------
# Dados de referencia dos produtos
# ---------------------------------------------------------------------------

PRODUTOS = {
    "botao": {
        "nome": "Botao Tarefas",
        "pecas_por_mesa": 90,
        "unidade": "peca",
        "unidade_plural": "pecas",
        "gramas_por_mesa": 120,
        "tempo_mesa_h": 2.0,
        "nozzle": "0.4mm",
        "material": "PLA",
    },
    "lego04": {
        "nome": "Blocos Lego 0.4",
        "pecas_por_mesa": 156,
        "jogos_por_mesa": 4,
        "pecas_por_jogo": 39,
        "unidade": "jogo",
        "unidade_plural": "jogos",
        "gramas_por_mesa": 200,
        "tempo_mesa_h": 4.0,
        "nozzle": "0.4mm",
        "material": "PLA",
    },
    "lego08": {
        "nome": "Blocos Lego 0.8",
        "pecas_por_mesa": 156,
        "jogos_por_mesa": 4,
        "pecas_por_jogo": 39,
        "unidade": "jogo",
        "unidade_plural": "jogos",
        "gramas_por_mesa": 200,
        "tempo_mesa_h": 2.0,
        "nozzle": "0.8mm",
        "material": "PLA",
    },
}

IMPRESSORAS_DEFAULT = 4
GRAMAS_POR_ROLO = 1000

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def produto_valido(slug: str) -> dict:
    """Retorna dados do produto ou encerra com erro."""
    if slug not in PRODUTOS:
        print(f"Erro: produto '{slug}' nao reconhecido.")
        print(f"Produtos disponiveis: {', '.join(PRODUTOS.keys())}")
        sys.exit(1)
    return PRODUTOS[slug]


def formatar_tempo(horas: float) -> str:
    """Formata horas decimais em 'Xh YYmin'."""
    h = int(horas)
    m = int(round((horas - h) * 60))
    if h == 0:
        return f"{m}min"
    if m == 0:
        return f"{h}h"
    return f"{h}h {m:02d}min"


def linha(largura: int = 50) -> str:
    return "-" * largura


def quantidade_em_unidades(prod: dict, quantidade: int) -> str:
    """Descreve a quantidade na unidade correta."""
    un = prod["unidade_plural"] if quantidade != 1 else prod["unidade"]
    return f"{quantidade} {un}"


def _calcular(prod: dict, quantidade: int):
    """Calcula mesas, pecas totais e sobra para uma quantidade pedida.

    Para lego, quantidade eh em jogos. Para botao, em pecas.
    """
    if prod["unidade"] == "jogo":
        jogos_por_mesa = prod["jogos_por_mesa"]
        mesas = math.ceil(quantidade / jogos_por_mesa)
        total_jogos = mesas * jogos_por_mesa
        sobra = total_jogos - quantidade
        total_pecas = total_jogos * prod["pecas_por_jogo"]
        return mesas, total_jogos, sobra, total_pecas
    else:
        pecas_por_mesa = prod["pecas_por_mesa"]
        mesas = math.ceil(quantidade / pecas_por_mesa)
        total = mesas * pecas_por_mesa
        sobra = total - quantidade
        return mesas, total, sobra, None


def _filamento(prod: dict, mesas: int):
    """Retorna gramas totais e rolos necessarios."""
    gramas = mesas * prod["gramas_por_mesa"]
    rolos = math.ceil(gramas / GRAMAS_POR_ROLO)
    return gramas, rolos


def _tempo(prod: dict, mesas: int, impressoras: int):
    """Retorna tempo sequencial e paralelo."""
    seq = mesas * prod["tempo_mesa_h"]
    paralelo = math.ceil(mesas / impressoras) * prod["tempo_mesa_h"]
    return seq, paralelo


# ---------------------------------------------------------------------------
# Subcomandos
# ---------------------------------------------------------------------------


def cmd_calcular(args):
    prod = produto_valido(args.produto)
    qtd = args.quantidade
    mesas, total, sobra, total_pecas = _calcular(prod, qtd)
    tempo_seq, tempo_par = _tempo(prod, mesas, IMPRESSORAS_DEFAULT)

    print()
    print(f"  CALCULO DE PRODUCAO — {prod['nome']}")
    print(f"  {linha(40)}")
    print(f"  Pedido:        {quantidade_em_unidades(prod, qtd)}")
    print(f"  Mesas:         {mesas}")
    print(f"  Producao:      {quantidade_em_unidades(prod, total)}")
    if total_pecas is not None:
        print(f"                 ({total_pecas} pecas total)")
    print(f"  Sobra:         {quantidade_em_unidades(prod, sobra)}")
    print(f"  Tempo est.:    ~{formatar_tempo(tempo_par)} (com {IMPRESSORAS_DEFAULT} impressoras)")
    print()


def cmd_filamento(args):
    prod = produto_valido(args.produto)
    mesas = args.mesas
    gramas, rolos = _filamento(prod, mesas)

    print()
    print(f"  CONSUMO DE FILAMENTO — {prod['nome']}")
    print(f"  {linha(40)}")
    print(f"  Mesas:         {mesas}")
    print(f"  Material:      {prod['material']} ({prod['nozzle']})")
    print(f"  Consumo/mesa:  ~{prod['gramas_por_mesa']}g")
    print(f"  Total:         ~{gramas}g")
    print(f"  Rolos (1kg):   {rolos}")
    print()


def cmd_tempo(args):
    prod = produto_valido(args.produto)
    mesas = args.mesas
    impressoras = args.impressoras
    seq, par = _tempo(prod, mesas, impressoras)

    print()
    print(f"  ESTIMATIVA DE TEMPO — {prod['nome']}")
    print(f"  {linha(40)}")
    print(f"  Mesas:         {mesas}")
    print(f"  Tempo/mesa:    ~{formatar_tempo(prod['tempo_mesa_h'])}")
    print(f"  Sequencial:    ~{formatar_tempo(seq)}")
    print(f"  Impressoras:   {impressoras}")
    print(f"  Paralelo:      ~{formatar_tempo(par)}")
    print()


def cmd_resumo(args):
    prod = produto_valido(args.produto)
    qtd = args.quantidade
    impressoras = args.impressoras

    mesas, total, sobra, total_pecas = _calcular(prod, qtd)
    gramas, rolos = _filamento(prod, mesas)
    seq, par = _tempo(prod, mesas, impressoras)

    print()
    print(f"  {'=' * 50}")
    print(f"  RESUMO DE PEDIDO — {prod['nome']}")
    print(f"  {'=' * 50}")
    print()
    print(f"  PRODUCAO")
    print(f"  {linha(40)}")
    print(f"  Pedido:        {quantidade_em_unidades(prod, qtd)}")
    print(f"  Mesas:         {mesas}")
    print(f"  Producao:      {quantidade_em_unidades(prod, total)}")
    if total_pecas is not None:
        print(f"                 ({total_pecas} pecas total)")
    print(f"  Sobra:         {quantidade_em_unidades(prod, sobra)}")
    print()
    print(f"  FILAMENTO")
    print(f"  {linha(40)}")
    print(f"  Material:      {prod['material']} ({prod['nozzle']})")
    print(f"  Consumo/mesa:  ~{prod['gramas_por_mesa']}g")
    print(f"  Total:         ~{gramas}g")
    print(f"  Rolos (1kg):   {rolos}")
    print()
    print(f"  TEMPO")
    print(f"  {linha(40)}")
    print(f"  Tempo/mesa:    ~{formatar_tempo(prod['tempo_mesa_h'])}")
    print(f"  Sequencial:    ~{formatar_tempo(seq)}")
    print(f"  Impressoras:   {impressoras}")
    print(f"  Paralelo:      ~{formatar_tempo(par)}")
    print()
    print(f"  {'=' * 50}")
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="CLI de gestao de producao — Impressao 3D",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Produtos disponiveis:\n"
            "  botao   — Botao Tarefas (90 pecas/mesa, 0.4mm)\n"
            "  lego04  — Blocos Lego 0.4 (4 jogos/mesa, 0.4mm)\n"
            "  lego08  — Blocos Lego 0.8 (4 jogos/mesa, 0.8mm)\n"
        ),
    )
    sub = parser.add_subparsers(dest="comando", help="Subcomando")

    # --- calcular ---
    p_calc = sub.add_parser("calcular", help="Calculadora de producao")
    p_calc.add_argument(
        "--produto", required=True, choices=PRODUTOS.keys(), help="Produto"
    )
    p_calc.add_argument(
        "--quantidade",
        required=True,
        type=int,
        help="Quantidade desejada (pecas ou jogos)",
    )

    # --- filamento ---
    p_fil = sub.add_parser("filamento", help="Estimativa de consumo de filamento")
    p_fil.add_argument(
        "--produto", required=True, choices=PRODUTOS.keys(), help="Produto"
    )
    p_fil.add_argument(
        "--mesas", required=True, type=int, help="Numero de mesas"
    )

    # --- tempo ---
    p_tempo = sub.add_parser("tempo", help="Estimativa de tempo de producao")
    p_tempo.add_argument(
        "--produto", required=True, choices=PRODUTOS.keys(), help="Produto"
    )
    p_tempo.add_argument(
        "--mesas", required=True, type=int, help="Numero de mesas"
    )
    p_tempo.add_argument(
        "--impressoras",
        type=int,
        default=IMPRESSORAS_DEFAULT,
        help=f"Numero de impressoras (default: {IMPRESSORAS_DEFAULT})",
    )

    # --- resumo ---
    p_resumo = sub.add_parser("resumo", help="Resumo completo de um pedido")
    p_resumo.add_argument(
        "--produto", required=True, choices=PRODUTOS.keys(), help="Produto"
    )
    p_resumo.add_argument(
        "--quantidade",
        required=True,
        type=int,
        help="Quantidade desejada (pecas ou jogos)",
    )
    p_resumo.add_argument(
        "--impressoras",
        type=int,
        default=IMPRESSORAS_DEFAULT,
        help=f"Numero de impressoras (default: {IMPRESSORAS_DEFAULT})",
    )

    args = parser.parse_args()

    if args.comando is None:
        parser.print_help()
        sys.exit(0)

    comandos = {
        "calcular": cmd_calcular,
        "filamento": cmd_filamento,
        "tempo": cmd_tempo,
        "resumo": cmd_resumo,
    }

    comandos[args.comando](args)


if __name__ == "__main__":
    main()

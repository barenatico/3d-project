# Scripts de Producao — Impressao 3D

CLI para calcular producao, consumo de filamento e tempo de impressao.

## Requisitos

Python 3 (sem dependencias externas).

## Uso

```bash
# Ver ajuda geral
python scripts/producao.py --help

# Ver ajuda de um subcomando
python scripts/producao.py calcular --help
```

## Produtos disponiveis

| Slug     | Produto          | Pecas/mesa | Nozzle |
|----------|------------------|------------|--------|
| `botao`  | Botao Tarefas    | 90 pecas   | 0.4mm  |
| `lego04` | Blocos Lego 0.4  | 4 jogos (156 pecas) | 0.4mm |
| `lego08` | Blocos Lego 0.8  | 4 jogos (156 pecas) | 0.8mm |

## Subcomandos

### calcular

Calcula mesas necessarias para produzir uma quantidade.

```bash
python scripts/producao.py calcular --produto botao --quantidade 270
python scripts/producao.py calcular --produto lego04 --quantidade 20
```

### filamento

Estima consumo de filamento para um numero de mesas.

```bash
python scripts/producao.py filamento --produto botao --mesas 5
```

### tempo

Estima tempo de producao com paralelismo entre impressoras.

```bash
python scripts/producao.py tempo --produto botao --mesas 12
python scripts/producao.py tempo --produto lego04 --mesas 8 --impressoras 2
```

### resumo

Resumo completo combinando calculo, filamento e tempo.

```bash
python scripts/producao.py resumo --produto lego04 --quantidade 20
python scripts/producao.py resumo --produto botao --quantidade 500 --impressoras 3
```

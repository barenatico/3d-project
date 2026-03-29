# 3D Project — Produção de Impressão 3D

## Sobre o projeto

Repositório de perfis e automações para produção em impressão 3D. O usuário produz peças em volume que são insumos para outros produtos.

## Setup de produção

- **Impressoras:** 4x Bambu Lab A1 (Direct Drive)
- **Nozzles:** 0.4mm (principal) e 0.8mm
- **Material principal:** PLA
- **Material secundário:** TPU 95A (Bambu Lab)
- **Software:** Bambu Studio (macOS)
- **User ID Bambu Studio:** 3244242577
- **Caminho dos perfis do usuário:** `/Users/leonardoparra/Library/Application Support/BambuStudio/user/3244242577/`
  - `process/` — perfis de processo (fatiamento)
  - `filament/` — perfis de filamento
  - `machine/` — perfis de máquina

## Produtos atuais

### Botão de Check — Tarefas Diárias (UniqueKids)
- Botão pequeno para produto "Tarefas Diárias da UniqueKids"
- **90 botões por mesa** (build plate cheia)
- Material: PLA
- Nozzle: 0.4mm
- Perfis ativos: processo **"Botão Tarefas"** + filamento **"Botão Tarefas"**
- Perfis antigos (mantidos): processo "Botão TD" + filamento "DEMON SPEED"

### Blocos Lego — Foto Personalizada
- Blocos estilo LEGO que montados formam uma foto personalizada do cliente
- **A foto é impressa na superfície LATERAL dos blocos** (não no topo)
- O cliente recebe desmontado e monta a foto
- **156 peças = 4 jogos completos por mesa**
- Material: PLA
- Perfis disponíveis: "Bricks Speed" (0.4), "Bricks Speed 0.8" (0.8), "0.16 Bricks" (qualidade)
- Para os bricks, a qualidade da **outer wall** é crítica (é a face da foto)

## Perfis no repositório

### Processo (profiles/process/)

| Perfil | Produto | Nozzle | Layer | Destaque |
|---|---|---|---|---|
| Botão Tarefas | Botões TD | 0.4 | 0.36mm | Otimizado: overhang on, top 2 layers, accel 10000 |
| Botão TD | Botões TD | 0.4 | 0.36mm | Original, sem otimizações |
| TPU 0.8 @A1 | Peças funcionais TPU | 0.8 | 0.32mm | Velocidades conservadoras, suporte configurado |

### Filamento (profiles/filament/)

| Perfil | Material | Destaque |
|---|---|---|
| Botão Tarefas | PLA genérico | MVS 20, temp 235/220°C, z-hop 0.3 |
| DEMON SPEED | PLA genérico | MVS 28, temp 235/205°C, z-hop 0.5 (original) |
| Bambu TPU 95A 0.8 @A1 | TPU 95A | MVS 5.5, retração 0.8mm a 15mm/s |

## Regras para alteração de perfis

### Criação de perfis
- Perfis de **processo** precisam de: `.json` + `.info` em `process/`
- Perfis de **filamento** precisam de: `.json` + `.info` em `filament/`
- O `.info` segue o formato:
  ```
  sync_info =
  user_id = 3244242577
  setting_id =
  base_id = <ID do perfil pai>
  updated_time = <timestamp>
  ```
- O `.json` deve ter `"from": "User"` e `inherits` apontando para um perfil concreto (não `@base`)
- `filament_settings_id` e `print_settings_id` devem ser arrays `["nome"]`
- Incluir campo `version`

### Edição de perfis existentes
- **NUNCA editar perfis enquanto o Bambu Studio estiver aberto** — ele sobrescreve os arquivos ao fechar
- Se precisar alterar um perfil existente, **criar um perfil novo com nome diferente**
- Avisar o usuário para fechar o Bambu Studio antes de criar perfis novos

### Registro no repositório
- Sempre copiar os JSONs para `profiles/process/` ou `profiles/filament/` no repo
- Fazer commit e push a cada alteração
- Atualizar este CLAUDE.md quando houver mudanças nos perfis ou setup

## Conceitos técnicos importantes

### MVS (Max Volumetric Speed)
- Limita o fluxo real de plástico independente da velocidade configurada
- Nozzle 0.4mm PLA realista: **18-22 mm³/s**
- Nozzle 0.8mm PLA: **~30-40 mm³/s**
- Nozzle 0.8mm TPU 95A: **~5.5 mm³/s**
- Fórmula: velocidade_real = MVS / (line_width × layer_height)
- Se a velocidade configurada > velocidade_real, o slicer reduz automaticamente

### TPU na A1
- Não usar AMS — alimentação direta
- Retração mínima (0.8mm) e lenta (15mm/s)
- Velocidades baixas (80-120mm/s)
- Aceleração baixa (2000-3000)
- Suporte: possível mas difícil de remover. Usar Z distance 0.36mm, rectilinear, baixa densidade

### Bricks (Legos)
- Superfície lateral é a face visível (foto)
- Layer height menor = melhor qualidade da foto lateral
- Outer wall speed deve ser controlada
- Seam position: back (esconder costura)
- Precisão dimensional importa para encaixe entre peças

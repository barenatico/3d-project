#!/bin/bash
# Backup dos perfis do Bambu Studio para o repositório
# Copia os JSONs de processo e filamento do usuário para profiles/

set -e

BAMBU_USER="/Users/leonardoparra/Library/Application Support/BambuStudio/user/3244242577"
REPO_DIR="/Users/leonardoparra/Documents/3d-project"

echo "=== Backup de Perfis Bambu Studio ==="
echo ""

# Verificar se Bambu Studio está rodando
if pgrep -x "BambuStudio" > /dev/null 2>&1; then
    echo "AVISO: Bambu Studio está aberto!"
    echo "Os perfis podem ser sobrescritos ao fechar o programa."
    echo "Recomendado: feche o Bambu Studio antes de continuar."
    echo ""
    read -p "Continuar mesmo assim? (s/N) " resp
    if [[ "$resp" != "s" && "$resp" != "S" ]]; then
        echo "Cancelado."
        exit 0
    fi
fi

# Backup processo
echo "Copiando perfis de processo..."
count=0
for f in "$BAMBU_USER/process/"*.json; do
    [ -f "$f" ] || continue
    nome=$(basename "$f")
    cp "$f" "$REPO_DIR/profiles/process/$nome"
    echo "  + process/$nome"
    count=$((count + 1))
done
echo "  $count perfis de processo copiados."
echo ""

# Backup filamento
echo "Copiando perfis de filamento..."
count=0
for f in "$BAMBU_USER/filament/"*.json; do
    [ -f "$f" ] || continue
    nome=$(basename "$f")
    cp "$f" "$REPO_DIR/profiles/filament/$nome"
    echo "  + filament/$nome"
    count=$((count + 1))
done
echo "  $count perfis de filamento copiados."
echo ""

# Backup machine (se existir)
if [ -d "$BAMBU_USER/machine" ]; then
    mkdir -p "$REPO_DIR/profiles/machine"
    echo "Copiando perfis de máquina..."
    count=0
    for f in "$BAMBU_USER/machine/"*.json; do
        [ -f "$f" ] || continue
        nome=$(basename "$f")
        cp "$f" "$REPO_DIR/profiles/machine/$nome"
        echo "  + machine/$nome"
        count=$((count + 1))
    done
    echo "  $count perfis de máquina copiados."
    echo ""
fi

echo "=== Backup concluído ==="
echo "Diretório: $REPO_DIR/profiles/"

#!/bin/bash
# ============================================================
# isabelle-integration.sh
# v4.0 : Mode CLI Isabelle pour integration avec Gabriel
# 
# Fonction:
#  1. Surveille le dossier /theories pour les fichiers .thy
#  2. Traite les fichiers avec isabelle process (batch mode)
#  3. Envoie les résultats à Gabriel via HTTP API
#  4. Sauvegarde les outputs dans /tmp/isabelle-output
# ============================================================

set -e

GABRIEL_HOST="${GABRIEL_HOST:-llm-agent-multiloop}"
GABRIEL_PORT="${GABRIEL_PORT:-8000}"
THEORIES_DIR="/theories"
OUTPUT_DIR="/tmp/isabelle-output"

echo "=== Isabelle CLI Integration v4.0 ==="
echo "Gabriel Host: $GABRIEL_HOST:$GABRIEL_PORT"
echo "Theories Dir: $THEORIES_DIR"
echo "Output Dir: $OUTPUT_DIR"
echo ""

# Creer le dossier de output
mkdir -p "$OUTPUT_DIR"

# Fonction: Traiter un fichier .thy avec Isabelle
process_theory_file() {
    local thy_file="$1"
    local filename=$(basename "$thy_file" .thy)
    local output_file="$OUTPUT_DIR/${filename}_result.txt"
    
    echo "[$(date)] Traitement: $thy_file"
    
    # Mode CLI: isabelle process (batch verification)
    if isabelle process -o quick -T "$thy_file" > "$output_file" 2>&1; then
        echo "[$(date)] ✓ Succes: $thy_file"
        
        # Envoyer le resultat a Gabriel via HTTP
        send_to_gabriel "$thy_file" "$output_file" "success"
    else
        echo "[$(date)] ✗ Erreur: $thy_file"
        send_to_gabriel "$thy_file" "$output_file" "error"
    fi
}

# Fonction: Envoyer le resultat a Gabriel
send_to_gabriel() {
    local thy_file="$1"
    local output_file="$2"
    local status="$3"
    
    # Verifier que Gabriel est accessible
    if ! nc -z "$GABRIEL_HOST" "$GABRIEL_PORT" 2>/dev/null; then
        echo "[$(date)] ⚠ Gabriel non accessible sur $GABRIEL_HOST:$GABRIEL_PORT (sera retente)"
        return 1
    fi
    
    # Lire le contenu de output
    local output_content=$(cat "$output_file" | head -100)  # 100 premieres lignes
    
    # Envoyer a Gabriel via curl
    curl -s -X POST "http://$GABRIEL_HOST:$GABRIEL_PORT/isabelle/verify" \
        -H "Content-Type: application/json" \
        -d "{
            \"theory_file\": \"$thy_file\",
            \"status\": \"$status\",
            \"output\": $(echo "$output_content" | jq -R -s .),
            \"timestamp\": \"$(date -Iseconds)\"
        }" > /dev/null 2>&1
    
    echo "[$(date)] Gabriel notifie: $thy_file ($status)"
}

# Fonction: Surveiller les changements (inotify)
watch_theories() {
    echo "[$(date)] Surveillance du dossier $THEORIES_DIR pour changements..."
    
    # Mode 1: Si inotify-tools est disponible (prefere)
    if command -v inotifywait &> /dev/null; then
        inotifywait -m -e close_write --format '%w%f' "$THEORIES_DIR" | while read thy_file; do
            if [[ "$thy_file" == *.thy ]]; then
                process_theory_file "$thy_file"
            fi
        done
    else
        # Mode 2: Fallback - polling chaque 10 secondes
        echo "[$(date)] inotify non disponible, utilisation du polling (10s)"
        while true; do
            find "$THEORIES_DIR" -name "*.thy" -type f -mmin -1 | while read thy_file; do
                process_theory_file "$thy_file"
            done
            sleep 10
        done
    fi
}

# Mode 1: Batch initial - traiter tous les .thy existants
echo "[$(date)] Phase 1: Traitement batch des fichiers .thy existants"
find "$THEORIES_DIR" -name "*.thy" -type f | head -20 | while read thy_file; do
    process_theory_file "$thy_file"
done

# Mode 2: Surveil continue pour nouveaux fichiers
echo "[$(date)] Phase 2: Surveillance continue activee"
watch_theories

# Graceful shutdown
trap "echo '[$(date)] Arret d Isabelle CLI'; exit 0" SIGTERM SIGINT
wait

#!/bin/bash
# ============================================================
# quick-start.sh
# v4.0 : Démarrage rapide Gabriel + Isabelle + API HTTP
# ============================================================

set -e

echo "╔════════════════════════════════════════════════════╗"
echo "║  Gabriel v4.0 - Quick Start                        ║"
echo "║  Multi-Loop Mathematical Agent                     ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Configuration
DOCKER_COMPOSE_FILE="docker-compose.yml"
PROFILES="${1:-}"  # Accept --profile isabelle as argument

echo "[1] Checking prerequisites..."
if ! command -v docker &> /dev/null; then
    echo "✗ Docker not found. Please install Docker Desktop."
    exit 1
fi
if ! command -v docker-compose &> /dev/null; then
    echo "⚠ docker-compose not found. Trying docker compose instead..."
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi
echo "✓ Docker available"
echo ""

# Check if docker-compose.yml exists
if [ ! -f "$DOCKER_COMPOSE_FILE" ]; then
    echo "✗ $DOCKER_COMPOSE_FILE not found. Please run from project root."
    exit 1
fi
echo "✓ docker-compose.yml found"
echo ""

# Determine mode
if [ "$PROFILES" = "--profile" ] || [ "$PROFILES" = "-i" ] || [ "$PROFILES" = "--isabelle" ]; then
    MODE="WITH ISABELLE"
    COMPOSE_CMD="$DOCKER_COMPOSE --profile isabelle up -d"
else
    MODE="STANDARD (Gabriel + Ollama)"
    COMPOSE_CMD="$DOCKER_COMPOSE up -d"
fi

echo "[2] Starting services ($MODE)..."
echo "    Command: $COMPOSE_CMD"
echo ""

eval "$COMPOSE_CMD"

echo "✓ Services launched"
echo ""

# Wait for services to start
echo "[3] Waiting for services to initialize (30s)..."
sleep 30

# Health checks
echo "[4] Health checks..."

# Check Gabriel
if curl -s http://localhost:8000/health | grep -q "online"; then
    echo "✓ Gabriel HTTP API: ONLINE (port 8000)"
else
    echo "⚠ Gabriel HTTP API: STARTING (may take a moment)"
fi

# Check Ollama
if curl -s http://localhost:11434 > /dev/null; then
    echo "✓ Ollama: ONLINE (port 11434)"
else
    echo "⚠ Ollama: STARTING"
fi

# Check containers
echo ""
echo "[5] Running containers:"
docker ps --filter "network=agent-network" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║  ✓ Gabriel v4.0 Ready!                             ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

echo "📍 Access points:"
echo "   • Gabriel HTTP API: http://localhost:8000"
echo "   • Ollama:          http://localhost:11434"
if [ "$MODE" = "WITH ISABELLE" ]; then
    echo "   • Isabelle:        docker exec -it isabelle bash"
fi
echo ""

echo "🔍 Test Gabriel:"
echo "   curl -X POST http://localhost:8000/query \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"question\": \"Quel est le 10eme nombre premier?\"}'"
echo ""

echo "📚 Documentation:"
echo "   • README_v4.0.md - Overview"
echo "   • INTEGRATION_UNIVERSESTAUCARRE.md - Connect to www.universestaucarre.com"
echo "   • GUIDE_JEDIT_GABRIEL.md - Isabelle Jed it integration"
echo ""

if [ "$MODE" = "WITH ISABELLE" ]; then
    echo "⚙️  Isabelle Commands:"
    echo "   # Access Isabelle container"
    echo "   docker exec -it isabelle bash"
    echo ""
    echo "   # Launch Jed it (requires X11 on Windows)"
    echo "   isabelle jedit /theories/example.thy"
    echo ""
    echo "   # Process .thy files (batch mode)"
    echo "   isabelle process -o quick /theories/file.thy"
    echo ""
fi

echo "❌ To stop:"
echo "   docker-compose down"
echo ""

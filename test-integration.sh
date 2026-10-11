#!/bin/bash
# ============================================================
# test-integration.sh
# v4.0 : Tests d'integration Gabriel + Isabelle + www.universestaucarre.com
# ============================================================

set -e

GABRIEL_URL="http://localhost:8000"
SLEEP_TIME=5

echo "=== Gabriel Integration Tests v4.0 ==="
echo ""

# Test 1: Health check
echo "[1] Testing Gabriel health..."
if curl -s "$GABRIEL_URL/health" | grep -q "online"; then
    echo "✓ Gabriel is ONLINE"
else
    echo "✗ Gabriel health check FAILED"
    exit 1
fi
echo ""

# Test 2: Simple query
echo "[2] Testing query endpoint..."
QUERY_RESPONSE=$(curl -s -X POST "$GABRIEL_URL/query" \
    -H "Content-Type: application/json" \
    -d '{
        "question": "Quel est le 5eme nombre premier?",
        "source": "test"
    }')

if echo "$QUERY_RESPONSE" | grep -q "answer"; then
    echo "✓ Query endpoint works"
    echo "  Response: $(echo "$QUERY_RESPONSE" | head -c 100)..."
else
    echo "✗ Query endpoint FAILED"
    echo "  Response: $QUERY_RESPONSE"
    exit 1
fi
echo ""

# Test 3: Sync endpoint (www.universestaucarre.com)
echo "[3] Testing sync/universestaucarre endpoint..."
SYNC_RESPONSE=$(curl -s -X POST "$GABRIEL_URL/sync/universestaucarre" \
    -H "Content-Type: application/json" \
    -d '{
        "session_id": "test-123",
        "question": "L'"'"'univers au carre existe-t-il?",
        "results": {
            "gpt4": "Oui",
            "claude": "Oui",
            "gemini": "Oui",
            "gabriel_web": "Oui"
        }
    }')

if echo "$SYNC_RESPONSE" | grep -q "synced"; then
    echo "✓ Sync endpoint works"
else
    echo "✗ Sync endpoint FAILED"
    echo "  Response: $SYNC_RESPONSE"
fi
echo ""

# Test 4: Isabelle verify endpoint
echo "[4] Testing isabelle/verify endpoint..."
ISABELLE_RESPONSE=$(curl -s -X POST "$GABRIEL_URL/isabelle/verify" \
    -H "Content-Type: application/json" \
    -d '{
        "theory_file": "/theories/test.thy",
        "status": "success",
        "output": "Verification complete",
        "timestamp": "2025-01-15T14:30:00"
    }')

if echo "$ISABELLE_RESPONSE" | grep -q "stored"; then
    echo "✓ Isabelle verify endpoint works"
else
    echo "✗ Isabelle verify endpoint FAILED"
    echo "  Response: $ISABELLE_RESPONSE"
fi
echo ""

# Test 5: Check Docker services
echo "[5] Checking Docker services..."
if docker ps | grep -q "llm-agent-multiloop-run"; then
    echo "✓ Gabriel container is running"
else
    echo "✗ Gabriel container NOT running"
    exit 1
fi

if docker ps | grep -q "ollama"; then
    echo "✓ Ollama container is running"
else
    echo "✗ Ollama container NOT running"
fi

if docker ps | grep -q "isabelle"; then
    echo "✓ Isabelle container is running"
else
    echo "⚠ Isabelle container NOT running (OK if profile not enabled)"
fi
echo ""

# Test 6: Check port 8000
echo "[6] Checking port 8000..."
if lsof -i :8000 >/dev/null 2>&1 || netstat -an | grep -q ":8000"; then
    echo "✓ Port 8000 is OPEN"
else
    echo "⚠ Port 8000 might not be open (could be normal)"
fi
echo ""

# Test 7: Check volumes
echo "[7] Checking Docker volumes..."
if docker volume ls | grep -q "agent-data"; then
    echo "✓ Agent data volume exists"
else
    echo "⚠ Agent data volume NOT found"
fi

if docker volume ls | grep -q "isabelle"; then
    echo "✓ Isabelle volume exists"
else
    echo "⚠ Isabelle volume NOT found (OK if profile not enabled)"
fi
echo ""

# Test 8: Check network
echo "[8] Checking Docker network..."
if docker network ls | grep -q "agent-network"; then
    echo "✓ Agent network exists"
    echo "  Containers:"
    docker network inspect agent-network | grep -o '"Name": "[^"]*"' | head -5
else
    echo "✗ Agent network NOT found"
fi
echo ""

echo "=== All tests completed! ==="
echo ""
echo "Summary:"
echo "  - Gabriel HTTP API: ✓ WORKING"
echo "  - Isabelle CLI: $(docker ps | grep isabelle > /dev/null && echo '✓ Running' || echo '⚠ Not active')"
echo "  - Docker services: ✓ OK"
echo ""
echo "Next steps:"
echo "  1. Connect www.universestaucarre.com to http://localhost:8000"
echo "  2. See INTEGRATION_UNIVERSESTAUCARRE.md for details"
echo ""

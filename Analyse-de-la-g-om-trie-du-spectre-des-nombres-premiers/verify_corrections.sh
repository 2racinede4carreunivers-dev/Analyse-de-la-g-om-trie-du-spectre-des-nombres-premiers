#!/usr/bin/env bash
# verify_corrections.sh
# Script pour verifier que toutes les corrections v4.1 sont appliquees

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  VERIFICATION DES CORRECTIONS GABRIEL v4.1                    ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

PROJECT_DIR="."
CHECKS_PASSED=0
CHECKS_TOTAL=0

# Function pour verifier une condition
check() {
    CHECKS_TOTAL=$((CHECKS_TOTAL + 1))
    if [ "$1" = "true" ]; then
        echo "✓ $2"
        CHECKS_PASSED=$((CHECKS_PASSED + 1))
    else
        echo "✗ $2"
    fi
}

echo "📋 VERIFICATION DES FICHIERS MODIFIES"
echo "───────────────────────────────────────"

# Fichiers code
test -f "$PROJECT_DIR/docker-compose.yml" && EXIST_COMPOSE="true" || EXIST_COMPOSE="false"
check "$EXIST_COMPOSE" "Fichier docker-compose.yml presente"

test -f "$PROJECT_DIR/main_cli.py" && EXIST_MAIN="true" || EXIST_MAIN="false"
check "$EXIST_MAIN" "Fichier main_cli.py presente"

test -f "$PROJECT_DIR/src/ui/ci_status.py" && EXIST_CI="true" || EXIST_CI="false"
check "$EXIST_CI" "Fichier src/ui/ci_status.py presente"

# Fichiers documentation
test -f "$PROJECT_DIR/CORRECTIONS_v4.1.md" && EXIST_DOC1="true" || EXIST_DOC1="false"
check "$EXIST_DOC1" "Documentation CORRECTIONS_v4.1.md presente"

test -f "$PROJECT_DIR/RESUME_EXECUTIF.md" && EXIST_DOC2="true" || EXIST_DOC2="false"
check "$EXIST_DOC2" "Documentation RESUME_EXECUTIF.md presente"

test -f "$PROJECT_DIR/REDEMARRAGE_v4.1.md" && EXIST_DOC3="true" || EXIST_DOC3="false"
check "$EXIST_DOC3" "Documentation REDEMARRAGE_v4.1.md presente"

echo ""
echo "🔍 VERIFICATION DES MODIFICATIONS DE CODE"
echo "──────────────────────────────────────────"

# Verifier les modifications dans docker-compose.yml
if grep -q "logging:" "$PROJECT_DIR/docker-compose.yml" 2>/dev/null; then
    check "true" "docker-compose.yml : logging driver configure"
else
    check "false" "docker-compose.yml : logging driver configure"
fi

if grep -q "GABRIEL_TESTS_DIR" "$PROJECT_DIR/docker-compose.yml" 2>/dev/null; then
    check "true" "docker-compose.yml : GABRIEL_TESTS_DIR defini"
else
    check "false" "docker-compose.yml : GABRIEL_TESTS_DIR defini"
fi

if grep -q "./tests:/home/agent/app/tests" "$PROJECT_DIR/docker-compose.yml" 2>/dev/null; then
    check "true" "docker-compose.yml : volume tests monte"
else
    check "false" "docker-compose.yml : volume tests monte"
fi

# Verifier les modifications dans main_cli.py
if grep -q "time.sleep(0.5)" "$PROJECT_DIR/main_cli.py" 2>/dev/null; then
    check "true" "main_cli.py : delai au demarrage ajoute"
else
    check "false" "main_cli.py : delai au demarrage ajoute"
fi

if grep -q "GABRIEL_TESTS_DIR" "$PROJECT_DIR/main_cli.py" 2>/dev/null; then
    check "true" "main_cli.py : logging GABRIEL_TESTS_DIR ajoute"
else
    check "false" "main_cli.py : logging GABRIEL_TESTS_DIR ajoute"
fi

# Verifier les modifications dans ci_status.py
if grep -q "_find_tests_dir" "$PROJECT_DIR/src/ui/ci_status.py" 2>/dev/null; then
    check "true" "ci_status.py : fonction _find_tests_dir() presente"
else
    check "false" "ci_status.py : fonction _find_tests_dir() presente"
fi

if grep -q "GABRIEL_TESTS_DIR" "$PROJECT_DIR/src/ui/ci_status.py" 2>/dev/null; then
    check "true" "ci_status.py : support GABRIEL_TESTS_DIR ajoute"
else
    check "false" "ci_status.py : support GABRIEL_TESTS_DIR ajoute"
fi

echo ""
echo "📚 VERIFICATION DE LA DOCUMENTATION"
echo "───────────────────────────────────"

test -f "$PROJECT_DIR/CHECKLIST_v4.1.md" && EXIST_CL="true" || EXIST_CL="false"
check "$EXIST_CL" "Checklist de verification present"

test -f "$PROJECT_DIR/STATUS_FINAL_v4.1.txt" && EXIST_STATUS="true" || EXIST_STATUS="false"
check "$EXIST_STATUS" "Fichier status final present"

test -f "$PROJECT_DIR/INDEX_DOCUMENTATION.md" && EXIST_INDEX="true" || EXIST_INDEX="false"
check "$EXIST_INDEX" "Index documentation present"

test -f "$PROJECT_DIR/QUICKSTART.md" && EXIST_QS="true" || EXIST_QS="false"
check "$EXIST_QS" "Quick Start present"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  RESULTAT : $CHECKS_PASSED/$CHECKS_TOTAL verifications reussies          ║"

if [ "$CHECKS_PASSED" = "$CHECKS_TOTAL" ]; then
    echo "║                                                                ║"
    echo "║  ✓ TOUTES LES CORRECTIONS v4.1 SONT APPLIQUEES !            ║"
    echo "║                                                                ║"
    echo "║  Prochaine etape :                                            ║"
    echo "║  $ docker-compose build --no-cache llm-agent-multiloop       ║"
    echo "║  $ docker-compose up                                          ║"
    echo "║                                                                ║"
    exit 0
else
    echo "║                                                                ║"
    echo "║  ⚠️  CERTAINES CORRECTIONS NE SONT PAS APPLIQUEES             ║"
    echo "║                                                                ║"
    echo "║  Verifiez les fichiers signales ci-dessus.                    ║"
    echo "║                                                                ║"
    exit 1
fi
echo "╚════════════════════════════════════════════════════════════════╝"

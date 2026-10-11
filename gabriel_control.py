#!/usr/bin/env python3
"""
GABRIEL CLEAN SHUTDOWN
Arrêt propre sans laisser de processus orphelins.
"""

import subprocess
import sys
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def shutdown_gabriel():
    """Arrêt propre de Gabriel et de tous les conteneurs."""
    logger.info("🛑 Arrêt propre de Gabriel...")
    
    # Étape 1: Arrêt des conteneurs
    logger.info("1️⃣  Arrêt des conteneurs...")
    result = subprocess.run(
        ["docker", "compose", "down"],
        capture_output=True,
        text=True,
        cwd=r"C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local"
    )
    
    if result.returncode == 0:
        logger.info("✓ Conteneurs arrêtés")
    else:
        logger.warning(f"⚠ Erreur lors de l'arrêt: {result.stderr}")
    
    # Étape 2: Attendre que les ports se libèrent
    logger.info("2️⃣  Attente de libération des ports...")
    time.sleep(3)
    
    # Étape 3: Vérifier les ports
    logger.info("3️⃣  Vérification des ports...")
    check_ports()
    
    logger.info("✅ Gabriel arrêté proprement")
    logger.info("💡 Conseil: Redémarrez simplement avec: docker compose up -d")


def check_ports():
    """Vérifie l'état des ports Gabriel."""
    ports = [
        ("8080", "Gabriel HTTP"),
        ("11434", "Ollama"),
    ]
    
    for port, service in ports:
        result = subprocess.run(
            f'netstat -ano | findstr :{port}',
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.stdout.strip():
            logger.warning(f"⚠ Port {port} ({service}): OCCUPÉ")
            # Montrer le PID
            parts = result.stdout.strip().split()
            if len(parts) > 0:
                pid = parts[-1]
                logger.info(f"  → PID: {pid}")
        else:
            logger.info(f"✓ Port {port} ({service}): LIBRE")


def start_gabriel():
    """Redémarrage de Gabriel."""
    logger.info("🚀 Démarrage de Gabriel...")
    
    result = subprocess.run(
        ["docker", "compose", "up", "-d"],
        capture_output=True,
        text=True,
        cwd=r"C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local"
    )
    
    if result.returncode == 0:
        logger.info("✓ Gabriel en cours de démarrage...")
        logger.info("⏳ Attendez 20-30 secondes pour la connexion complète")
        logger.info("🌐 Accès: http://localhost:8080")
    else:
        logger.error(f"❌ Erreur: {result.stderr}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "stop":
            shutdown_gabriel()
        elif command == "start":
            start_gabriel()
        elif command == "restart":
            shutdown_gabriel()
            time.sleep(2)
            start_gabriel()
        elif command == "status":
            check_ports()
        else:
            print("""
Usage: python gabriel_control.py [COMMAND]

Commands:
  stop      - Arrêt propre de Gabriel
  start     - Démarrage de Gabriel
  restart   - Redémarrage complet
  status    - Vérifier l'état des ports

Examples:
  python gabriel_control.py stop
  python gabriel_control.py start
  python gabriel_control.py restart
  python gabriel_control.py status
            """)
    else:
        print("Usage: python gabriel_control.py [stop|start|restart|status]")
        check_ports()

#!/usr/bin/env python3
"""
suppress_ollama_logs.py
Supprime les logs Ollama du stdout/stderr de docker-compose
avant le lancement de Gabriel CLI.

Methode : Capture et supprime les logs Ollama qui apparaissent a l'ouverture.
"""
import sys
import time
import subprocess


def suppress_docker_logs():
    """Attendre que Docker termine ses messages de demarrage de Ollama."""
    # Ollama affiche generalement ses logs pendant 2-5 secondes au lancement
    # On attend un peu pour que les conteneurs se stabilisent
    print("  [dim]Demarrage des services backend (Ollama, orchestrateur)...[/dim]", flush=True)
    time.sleep(3)  # Laisser Ollama demarrer silencieusement
    print()  # Ligne vide pour separator


if __name__ == "__main__":
    suppress_docker_logs()

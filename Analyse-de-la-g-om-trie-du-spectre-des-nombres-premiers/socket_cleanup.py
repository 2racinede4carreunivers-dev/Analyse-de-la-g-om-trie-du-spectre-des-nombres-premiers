#!/usr/bin/env python3
"""
SOCKET CLEANUP UTILITY - Ferme complètement les sockets sans fermer Docker Desktop

Cette librairie gère la fermeture des sockets au niveau du système d'exploitation
pour garantir que le port se libère quand Gabriel s'arrête.

SÉCURITÉ: Par défaut, les sockets sont bindées sur 127.0.0.1 (localhost) pour éviter
l'exposition sur toutes les interfaces réseau. Voir CWE-200.
"""

import os
import sys
import socket
import logging
import subprocess
import time
from typing import Optional
from contextlib import contextmanager

logger = logging.getLogger(__name__)

# SÉCURITÉ: Configuration par défaut bindée sur localhost
DEFAULT_BIND_ADDRESS = '127.0.0.1'  # Au lieu de '0.0.0.0'


class SocketCleanup:
    """Gère la fermeture complète des sockets au niveau système."""
    
    def __init__(self, port: int, bind_address: str = DEFAULT_BIND_ADDRESS):
        """
        Args:
            port: Numéro de port à nettoyer
            bind_address: Adresse IP pour binder (défaut: 127.0.0.1 pour sécurité)
                          SÉCURITÉ: Éviter '0.0.0.0' car elle expose sur tous les interfaces
                          Voir CWE-200: Exposure of Sensitive Information to an Unauthorized Actor
        """
        self.port = port
        self.bind_address = bind_address
        self.listener_socket: Optional[socket.socket] = None
        self.original_sigint = None
        
    def close_socket(self):
        """Ferme la socket directement."""
        if self.listener_socket:
            try:
                self.listener_socket.close()
                logger.info(f"Socket fermée proprement (port {self.port})")
            except Exception as e:
                logger.warning(f"Erreur fermeture socket: {e}")
    
    def force_close_port_listeners(self):
        """Force la fermeture de tous les listeners sur le port (au niveau OS)."""
        try:
            if sys.platform == "win32":
                self._close_port_windows()
            elif sys.platform in ["linux", "linux2"]:
                self._close_port_linux()
            elif sys.platform == "darwin":
                self._close_port_macos()
        except Exception as e:
            logger.warning(f"Erreur force close: {e}")
    
    def _close_port_windows(self):
        """Windows: Utilise netstat + taskkill pour fermer le port."""
        try:
            # Trouver les PIDs qui écouten sur le port
            result = subprocess.run(
                f'netstat -ano | findstr :{self.port}',
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                pids = set()
                
                for line in lines:
                    parts = line.split()
                    if len(parts) > 0:
                        try:
                            pid = int(parts[-1])
                            pids.add(pid)
                        except (ValueError, IndexError):
                            pass
                
                # TUE SEULEMENT LE LISTENER, PAS LE PARENT
                for pid in pids:
                    try:
                        proc_info = subprocess.run(
                            f'tasklist /fi "PID eq {pid}"',
                            shell=True,
                            capture_output=True,
                            text=True
                        )
                        
                        # Vérifier que c'est pas docker daemon lui-même
                        if "docker" not in proc_info.stdout.lower() or "wsl" in proc_info.stdout.lower():
                            subprocess.run(
                                f'taskkill /PID {pid} /F',
                                shell=True,
                                timeout=3
                            )
                            logger.info(f"Listener PID {pid} fermé (port {self.port})")
                    except Exception as e:
                        logger.warning(f"Erreur fermeture PID {pid}: {e}")
        
        except subprocess.TimeoutExpired:
            logger.warning("Timeout lors de la fermeture du port")
        except Exception as e:
            logger.warning(f"Erreur Windows close: {e}")
    
    def _close_port_linux(self):
        """Linux: Utilise lsof + kill."""
        try:
            result = subprocess.run(
                f'lsof -i :{self.port} -t',
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            for pid_str in result.stdout.strip().split():
                try:
                    pid = int(pid_str)
                    os.kill(pid, 15)  # SIGTERM
                    time.sleep(0.5)
                    try:
                        os.kill(pid, 9)  # SIGKILL si encore actif
                    except ProcessLookupError:
                        pass
                    logger.info(f"Listener PID {pid} tué (port {self.port})")
                except (ValueError, ProcessLookupError):
                    pass
        except Exception as e:
            logger.warning(f"Erreur Linux close: {e}")
    
    def _close_port_macos(self):
        """macOS: Utilise lsof + kill (similaire à Linux)."""
        self._close_port_linux()
    
    def reset_port(self):
        """Remet le port en état utilisable.
        
        SÉCURITÉ: Utilise bind_address (localhost par défaut) au lieu de '0.0.0.0'
        pour éviter l'exposition sur toutes les interfaces réseau.
        Ref: CWE-200 Exposure of Sensitive Information to an Unauthorized Actor
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, b'\x01\x00\x00\x00\x00\x00\x00\x00')
            
            # SÉCURITÉ: Binder sur l'adresse configurée (défaut: 127.0.0.1 localhost)
            # Au lieu de '0.0.0.0' qui accepte toutes les connexions
            sock.bind((self.bind_address, self.port))
            sock.close()
            logger.info(f"Port {self.port} réinitialisé (SO_REUSEADDR, bind={self.bind_address})")
            return True
        except OSError as e:
            logger.warning(f"Port {self.port} pas complètement libéré: {e}")
            return False
    
    def cleanup(self):
        """Nettoyage complet."""
        logger.info(f"=== SOCKET CLEANUP: Port {self.port} (bind={self.bind_address}) ===")
        
        # Étape 1: Fermer la socket Python
        self.close_socket()
        
        # Étape 2: Forcer la fermeture des listeners
        self.force_close_port_listeners()
        
        # Étape 3: Réinitialiser le port
        time.sleep(1)
        self.reset_port()
        
        logger.info(f"=== SOCKET CLEANUP COMPLÈTE ===")


@contextmanager
def socket_context(port: int, bind_address: str = DEFAULT_BIND_ADDRESS):
    """Context manager pour socket cleanup automatique.
    
    Args:
        port: Numéro de port
        bind_address: Adresse IP pour binder (défaut: 127.0.0.1 pour sécurité)
    """
    cleanup = SocketCleanup(port, bind_address)
    try:
        yield cleanup
    finally:
        cleanup.cleanup()


def force_port_cleanup(port: int, bind_address: str = DEFAULT_BIND_ADDRESS, force_kill_listener: bool = True):
    """Force le cleanup du port (fonction standalone).
    
    Args:
        port: Numéro de port
        bind_address: Adresse IP pour binder (défaut: 127.0.0.1 pour sécurité)
        force_kill_listener: Forcer la fermeture des listeners existants
        
    SÉCURITÉ: Par défaut utilise 127.0.0.1 (localhost) pour éviter l'exposition
    sur toutes les interfaces réseau.
    """
    cleanup = SocketCleanup(port, bind_address)
    if force_kill_listener:
        cleanup.force_close_port_listeners()
    time.sleep(1)
    cleanup.reset_port()
    logger.info(f"Port {port} forcément nettoyé (bind={bind_address})")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    # SÉCURITÉ: Accepter optionnellement une adresse de binding en ligne de commande
    # Défaut: 127.0.0.1 (localhost) pour sécurité
    bind_address = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_BIND_ADDRESS
    
    print(f"Nettoyage port {port} (bind={bind_address})...")
    force_port_cleanup(port, bind_address)
    print(f"Port {port} nettoyé!")

#!/usr/bin/env python3
"""
PORT CLEANUP UTILITY FOR GABRIEL
Ensures proper socket cleanup on exit and port release.

SÉCURITÉ: Par défaut, les sockets sont bindées sur 127.0.0.1 (localhost) pour éviter
l'exposition sur toutes les interfaces réseau. Voir CWE-200.

Usage:
  from port_cleanup import CleanPortManager
  
  with CleanPortManager(9000) as manager:
      # Launch Flask or other service
      pass
  # Port is guaranteed to be released
"""

import os
import socket
import signal
import sys
import logging
import time
from contextlib import contextmanager
from pathlib import Path

logger = logging.getLogger(__name__)

# SÉCURITÉ: Configuration par défaut bindée sur localhost
DEFAULT_BIND_ADDRESS = '127.0.0.1'  # Au lieu de '0.0.0.0'


class CleanPortManager:
    """Manages proper cleanup of TCP ports on exit.
    
    SÉCURITÉ: Par défaut utilise 127.0.0.1 (localhost) pour éviter l'exposition
    sur toutes les interfaces réseau. Voir CWE-200.
    """
    
    def __init__(self, port: int, timeout: int = 10, bind_address: str = DEFAULT_BIND_ADDRESS):
        """
        Args:
            port: Numéro de port à gérer
            timeout: Timeout pour les opérations
            bind_address: Adresse IP pour binder (défaut: 127.0.0.1 pour sécurité)
                          SÉCURITÉ: Éviter '0.0.0.0' car elle expose sur tous les interfaces
        """
        self.port = port
        self.timeout = timeout
        self.bind_address = bind_address
        self.original_sigint = None
        self.original_sigterm = None
        
    def __enter__(self):
        """Setup signal handlers for clean exit."""
        self.original_sigint = signal.signal(signal.SIGINT, self._handle_signal)
        self.original_sigterm = signal.signal(signal.SIGTERM, self._handle_signal)
        logger.info(f"Port manager active for port {self.port} (bind={self.bind_address})")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Restore signal handlers and cleanup port."""
        # Restore original handlers
        if self.original_sigint is not None:
            signal.signal(signal.SIGINT, self.original_sigint)
        if self.original_sigterm is not None:
            signal.signal(signal.SIGTERM, self.original_sigterm)
        
        # Close the port
        self.release_port()
        logger.info(f"Port {self.port} cleaned up and released")
        return False
    
    def _handle_signal(self, signum, frame):
        """Handle termination signals."""
        logger.info(f"Received signal {signum}, shutting down cleanly...")
        self.release_port()
        sys.exit(0)
    
    def release_port(self):
        """Force release of the port.
        
        SÉCURITÉ: Utilise bind_address (localhost par défaut) au lieu de '0.0.0.0'
        pour éviter l'exposition sur toutes les interfaces réseau.
        Ref: CWE-200 Exposure of Sensitive Information to an Unauthorized Actor
        """
        # Try to close any listening sockets
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, b'\x01\x00\x00\x00\x00\x00\x00\x00')
            
            # SÉCURITÉ: Binder sur l'adresse configurée (défaut: 127.0.0.1 localhost)
            # Au lieu de '0.0.0.0' qui accepte toutes les connexions
            sock.bind((self.bind_address, self.port))
            sock.close()
            logger.info(f"Port {self.port} successfully released (bind={self.bind_address})")
        except OSError as e:
            logger.warning(f"Could not bind to port {self.port}: {e}")
            # Try using lsof/netstat to kill processes
            self._force_kill_port_processes()
    
    def _force_kill_port_processes(self):
        """Kill processes using the port (platform-specific)."""
        try:
            if sys.platform == "win32":
                # Windows: use netstat and taskkill
                import subprocess
                result = subprocess.run(
                    f'netstat -ano | findstr :{self.port}',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                for line in result.stdout.split('\n'):
                    if line.strip():
                        parts = line.split()
                        if len(parts) > 0:
                            try:
                                pid = int(parts[-1])
                                subprocess.run(f'taskkill /PID {pid} /F', shell=True, timeout=2)
                                logger.info(f"Killed process {pid} using port {self.port}")
                            except (ValueError, subprocess.TimeoutExpired):
                                pass
            else:
                # Linux/macOS: use lsof
                import subprocess
                result = subprocess.run(
                    f'lsof -i :{self.port} -t',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                for pid_str in result.stdout.strip().split():
                    try:
                        pid = int(pid_str)
                        os.kill(pid, signal.SIGTERM)
                        time.sleep(0.5)
                        try:
                            os.kill(pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                        logger.info(f"Killed process {pid} using port {self.port}")
                    except (ValueError, ProcessLookupError):
                        pass
        except Exception as e:
            logger.warning(f"Could not force kill port processes: {e}")


def check_port_available(port: int, bind_address: str = DEFAULT_BIND_ADDRESS) -> bool:
    """Check if a port is available.
    
    Args:
        port: Numéro de port
        bind_address: Adresse à vérifier (défaut: 127.0.0.1)
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        result = sock.connect_ex((bind_address, port))
        sock.close()
        return result != 0  # 0 means connected (port in use), != 0 means available
    except Exception:
        return True


def wait_for_port_available(port: int, timeout: int = 30, bind_address: str = DEFAULT_BIND_ADDRESS) -> bool:
    """Wait for a port to become available.
    
    Args:
        port: Numéro de port
        timeout: Timeout en secondes
        bind_address: Adresse à vérifier (défaut: 127.0.0.1)
    """
    start = time.time()
    while time.time() - start < timeout:
        if check_port_available(port, bind_address):
            logger.info(f"Port {port} is now available")
            return True
        time.sleep(1)
    logger.warning(f"Port {port} not available after {timeout}s")
    return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9000
    # SÉCURITÉ: Accepter optionnellement une adresse de binding en ligne de commande
    # Défaut: 127.0.0.1 (localhost) pour sécurité
    bind_address = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_BIND_ADDRESS
    
    print(f"Checking port {port} (bind={bind_address})...")
    if check_port_available(port, bind_address):
        print(f"✓ Port {port} is available")
    else:
        print(f"✗ Port {port} is in use, attempting to free it...")
        manager = CleanPortManager(port, bind_address=bind_address)
        manager.release_port()
        if wait_for_port_available(port, bind_address=bind_address):
            print(f"✓ Port {port} is now available")
        else:
            print(f"✗ Could not free port {port}")
            sys.exit(1)

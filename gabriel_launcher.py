#!/usr/bin/env python3
"""
GABRIEL LAUNCHER WITH PROPER PORT CLEANUP
Ensures sockets are cleaned up on exit or 'quitter' command.
"""

import os
import sys
import logging
from pathlib import Path

# Add root to path
_ROOT = Path(__file__).parent.resolve()
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

# Import FIRST before anything else
from port_cleanup import CleanPortManager, wait_for_port_available

logger = logging.getLogger(__name__)


def main():
    """
    Main entry point with port cleanup.
    """
    # Get configuration
    http_port = int(os.getenv("GABRIEL_HTTP_PORT", "9000"))
    
    # Setup logging first
    from src.core.logging_setup import setup_logging
    log_dir = os.getenv("GABRIEL_LOG_DIR", "./logs")
    setup_logging(log_dir)
    
    logging.info(f"Gabriel Launcher: Configuring for port {http_port}")
    
    # Ensure port is available before starting
    logging.info(f"Checking if port {http_port} is available...")
    if not wait_for_port_available(http_port, timeout=5):
        logging.warning(f"Port {http_port} may still be in use, attempting cleanup...")
        manager = CleanPortManager(http_port)
        manager.release_port()
        if not wait_for_port_available(http_port, timeout=5):
            logging.error(f"Could not acquire port {http_port}, exiting")
            sys.exit(1)
    
    # Launch Gabriel with port manager
    with CleanPortManager(http_port):
        try:
            # Import and run main_cli
            from main_cli import main as gabriel_main
            gabriel_main()
        except KeyboardInterrupt:
            logging.info("Received keyboard interrupt, shutting down...")
        except Exception as e:
            logging.error(f"Fatal error: {e}", exc_info=True)
            sys.exit(1)
    
    # Port is automatically cleaned up by context manager
    logging.info("Gabriel session ended, port cleaned up")


if __name__ == "__main__":
    main()

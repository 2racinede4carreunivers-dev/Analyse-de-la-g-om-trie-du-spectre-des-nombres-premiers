#!/usr/bin/env python
"""
Vérification rapide : Gabriel + Cline Hybrid Fusion
====================================================
"""
import sys
from pathlib import Path

# Vérifier les 3 fichiers créés
print("\n[CHECK] Fichiers d'intégration Cline...")
files_to_check = [
    "src/adapters/cline_tools_bridge.py",
    "src/adapters/hybrid_dispatcher.py",
    "src/ui/cli_cline_extension.py",
]

for f in files_to_check:
    path = Path(f)
    status = "[OK]" if path.exists() else "[MISSING]"
    print(f"  {status}: {f}")
    if not path.exists():
        sys.exit(1)

# Vérifier les imports
print("\n[CHECK] Imports des modules...")
try:
    from src.adapters.cline_tools_bridge import ClineToolDispatcher
    print("  [OK] cline_tools_bridge")
except Exception as e:
    print(f"  [FAILED] cline_tools_bridge - {e}")
    sys.exit(1)

try:
    from src.adapters.hybrid_dispatcher import HybridDispatcher
    print("  [OK] hybrid_dispatcher")
except Exception as e:
    print(f"  [FAILED] hybrid_dispatcher - {e}")
    sys.exit(1)

try:
    from src.ui.cli_cline_extension import CLIClikeExtension
    print("  [OK] cli_cline_extension")
except Exception as e:
    print(f"  [FAILED] cli_cline_extension - {e}")
    sys.exit(1)

# Verifier CLI avec Cline
print("\n[CHECK] CLI Gabriel avec integration Cline...")
try:
    from src.ui.cli import CLIInterface
    print("  [OK] CLIInterface imported")
except Exception as e:
    print(f"  [FAILED] CLIInterface - {e}")
    sys.exit(1)

# Verifier que CLIInterface a la propriete _cline_ext
try:
    cli = CLIInterface()
    has_cline = hasattr(cli, '_cline_ext')
    if has_cline:
        print("  [OK] Cline extension integrated into CLI")
    else:
        print("  [FAILED] Cline extension NOT integrated")
        sys.exit(1)
except Exception as e:
    print(f"  [FAILED] Creating CLIInterface - {e}")
    sys.exit(1)

# Test dispatcher
print("\n[CHECK] Dispatcher recognition...")
try:
    dispatcher = HybridDispatcher()
    
    # Test Cline detection
    category = dispatcher.detect_category("read test.txt")
    if category.value == "cline_file":
        print("  [OK] Cline file command detected")
    else:
        print(f"  [FAILED] Expected cline_file, got {category.value}")
        sys.exit(1)
    
    # Test Gabriel detection
    category = dispatcher.detect_category("ratio 1/2 spectral")
    if category.value == "gabriel_math":
        print("  [OK] Gabriel math command detected")
    else:
        print(f"  [FAILED] Expected gabriel_math, got {category.value}")
        sys.exit(1)
    
    # Test LLM routing
    category = dispatcher.detect_category("hello world")
    if category.value == "llm_routing":
        print("  [OK] LLM routing detected")
    else:
        print(f"  [FAILED] Expected llm_routing, got {category.value}")
        sys.exit(1)
        
except Exception as e:
    print(f"  [FAILED] Dispatcher test - {e}")
    sys.exit(1)

# Test file operations
print("\n[CHECK] File operations...")
try:
    dispatcher = ClineToolDispatcher()
    
    # Create
    result = dispatcher.dispatch("create verify_fusion_test.txt Hello Fusion")
    if result.success:
        print("  [OK] File creation")
    else:
        print(f"  [FAILED] File creation - {result.error}")
        sys.exit(1)
    
    # Read
    result = dispatcher.dispatch("read verify_fusion_test.txt")
    if result.success and "Hello Fusion" in result.output:
        print("  [OK] File reading")
    else:
        print(f"  [FAILED] File reading - {result.error}")
        sys.exit(1)
    
    # Delete
    result = dispatcher.dispatch("delete verify_fusion_test.txt")
    if result.success:
        print("  [OK] File deletion")
    else:
        print(f"  [FAILED] File deletion - {result.error}")
        sys.exit(1)
        
except Exception as e:
    print(f"  [FAILED] File operations - {e}")
    sys.exit(1)

print("\n" + "="*70)
print("GABRIEL + CLINE HYBRID FUSION - VERIFICATION OK")
print("="*70)
print("\n=> Prochaine etape: Demarrer Gabriel\n")
print("   cd C:\\agent-multiloop-Gabriel-local\\agent-multiloop-Gabriel-local")
print("   .\\.venv\\Scripts\\python.exe main_cli.py\n")
print("   Puis tapez: gabriel> aide\n")
print("="*70 + "\n")

sys.exit(0)

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports

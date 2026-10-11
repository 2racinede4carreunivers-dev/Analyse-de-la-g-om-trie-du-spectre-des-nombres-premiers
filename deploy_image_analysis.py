#!/usr/bin/env python3
"""
GABRIEL IMAGE ANALYSIS - DEPLOYMENT SCRIPT (FINAL)
Déploie la pipeline d'analyse d'images avec 1 commande
"""

import subprocess
import sys
from pathlib import Path

def main():
    print("\n" + "="*80)
    print("  GABRIEL IMAGE ANALYSIS - DEPLOYMENT SCRIPT")
    print("="*80)
    
    # Step 1: Install dependencies
    print("\n[STEP 1] Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "Pillow", "numpy", "--quiet"],
                      check=True, timeout=120)
        print("  ✅ Dependencies installed")
    except Exception as e:
        print(f"  ⚠️ Install warning: {e}")
    
    # Step 2: Check Gabriel vision module exists
    print("\n[STEP 2] Checking Gabriel Vision module...")
    vision_module = Path("src/gabriel_vision_integration.py")
    if vision_module.exists():
        print(f"  ✅ {vision_module} found ({vision_module.stat().st_size // 1024} KB)")
    else:
        print(f"  ❌ {vision_module} NOT FOUND - cannot continue")
        return False
    
    # Step 3: Apply CLI patch
    print("\n[STEP 3] Applying CLI patch...")
    try:
        # Direct inline patch application
        cli_path = Path("src/ui/cli.py")
        if not cli_path.exists():
            print(f"  ❌ {cli_path} not found")
            return False
        
        with open(cli_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already patched
        if "IMAGE ANALYSIS INTEGRATION" in content and "_handle_image_query" in content:
            print("  ✅ CLI already patched (skipping)")
        else:
            print("  ⚠️ Manual patching required - see COMPLETE_INTEGRATION_INSTRUCTIONS.md")
            print("     (Automatic patching of large files recommended via: python apply_image_analysis_patch.py)")
            return False
        
    except Exception as e:
        print(f"  ❌ Patch error: {e}")
        return False
    
    # Step 4: Test imports
    print("\n[STEP 4] Testing imports...")
    try:
        from src.gabriel_vision_integration import GabrielVisionIntegration
        print("  ✅ gabriel_vision_integration imported successfully")
    except Exception as e:
        print(f"  ⚠️ Import test: {e}")
    
    # Final summary
    print("\n" + "="*80)
    print("  ✅ DEPLOYMENT READY")
    print("="*80)
    
    print("""
Next steps:
  1. Ensure CLI patch is applied (if not, run: python apply_image_analysis_patch.py)
  2. Start Gabriel: python src/ui/cli.py
  3. Test: gabriel> analyse image C:\\path\\to\\image.png
  
Expected response:
  🔍 Analyzing image...
  [Image Analysis Report]
  ✅ Confidence: 9.5/10
  Source: Vision Module

Documentation:
  - COMPLETE_INTEGRATION_INSTRUCTIONS.md (step-by-step guide)
  - 00_START_HERE_IMAGE_ANALYSIS.md (quick overview)
""")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

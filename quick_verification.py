#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QUICK START - Gabriel v2.0 Mathematical Engine
Script de verification rapide du deploiement
"""

import os
import sys
from pathlib import Path

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_file_exists(path, description):
    """Verifie existence fichier"""
    exists = Path(path).exists()
    status = "[OK]" if exists else "[FAIL]"
    print(f"{status} {description}: {path}")
    return exists

def check_directory_exists(path, description):
    """Verifie existence repertoire"""
    exists = Path(path).is_dir()
    status = "[OK]" if exists else "[FAIL]"
    print(f"{status} {description}: {path}")
    return exists

def main():
    print_header("GABRIEL v2.0 DEPLOYMENT VERIFICATION")
    
    base_path = Path(__file__).parent
    all_good = True
    
    # ============================================================
    # Verifier structure
    # ============================================================
    
    print("\n[STRUCTURE] VERIFICATION STRUCTURE FICHIERS")
    print("-" * 60)
    
    files_to_check = [
        ("src/mathematical_engine.py", "Module mathematique"),
        ("src/hol_lean_interface.py", "Interface HOL4/Lean4"),
        ("src/pdf_rag_processor.py", "Processeur PDF RAG"),
        ("src/__init__.py", "Package __init__"),
        ("gabriel_mathematical.py", "Assistant mathematique principal"),
        ("integration_mathematical.py", "Routes FastAPI + integration"),
        ("config_mathematical.env", "Fichier configuration"),
        ("requirements.txt", "Dependencies"),
        ("theories/riemann_spectral.thy", "Theorie HOL4"),
        ("theories/RiemannSpectral.lean", "Theorie Lean4"),
        ("README_MATHEMATICAL_v2.md", "Documentation vue d'ensemble"),
        ("SETUP_MATHEMATICAL_v2.md", "Documentation setup"),
        ("CHECKLIST_FINAL.md", "Checklist finale"),
    ]
    
    for filepath, description in files_to_check:
        full_path = base_path / filepath
        if not check_file_exists(full_path, description):
            all_good = False
    
    # Verifier repertoires
    dirs_to_check = [
        ("src", "Repertoire modules"),
        ("theories", "Repertoire theories"),
        ("data", "Repertoire donnees"),
        ("pdf", "Repertoire PDF"),
    ]
    
    for dirpath, description in dirs_to_check:
        full_path = base_path / dirpath
        if not check_directory_exists(full_path, description):
            all_good = False
    
    # Verifier PDF
    print("\n[PDF] VERIFICATION PDF")
    print("-" * 60)
    pdf_path = base_path / "pdf" / "analyse_hypothese_riemann_savard.pdf"
    if not check_file_exists(pdf_path, "PDF Riemann"):
        print("  [WARN] PDF non trouve a l'emplacement attendu!")
        print(f"  [INFO] Attendu: {pdf_path}")
        print("  [OK] (OK si PDF est dans: C:\\agent-multiloop-Gabriel-local-final\\pdf\\)")
    
    # ============================================================
    # Verifier imports Python
    # ============================================================
    
    print("\n[PYTHON] VERIFICATION IMPORTS PYTHON")
    print("-" * 60)
    
    imports_to_check = [
        ("sympy", "SymPy (calculs symboliques)"),
        ("mpmath", "mpmath (haute precision)"),
        ("PyPDF2", "PyPDF2 (extraction PDF)"),
        ("pydantic", "Pydantic (validation)"),
        ("dotenv", "python-dotenv (config)"),
    ]
    
    for module_name, description in imports_to_check:
        try:
            __import__(module_name)
            print(f"[OK] {description}")
        except ImportError:
            print(f"[FAIL] {description}")
            if module_name == "PyPDF2":
                print("  => pip install PyPDF2")
            all_good = False
    
    # ============================================================
    # Verifier modules custom
    # ============================================================
    
    print("\n[MODULES] VERIFICATION MODULES CUSTOM")
    print("-" * 60)
    
    os.chdir(base_path)
    sys.path.insert(0, str(base_path))
    
    custom_modules = [
        ("src.mathematical_engine", "MathematicalEngine"),
        ("src.hol_lean_interface", "FormalVerificationPipeline"),
        ("src.pdf_rag_processor", "PDFRAGProcessor"),
    ]
    
    for module_path, class_name in custom_modules:
        try:
            module = __import__(module_path, fromlist=[class_name])
            getattr(module, class_name)
            print(f"[OK] {module_path}.{class_name}")
        except Exception as e:
            print(f"[FAIL] {module_path}.{class_name}: {e}")
            all_good = False
    
    # ============================================================
    # Verifier configuration
    # ============================================================
    
    print("\n[CONFIG] VERIFICATION CONFIGURATION")
    print("-" * 60)
    
    config_file = base_path / "config_mathematical.env"
    if config_file.exists():
        print(f"[OK] Fichier config trouve: {config_file.name}")
        
        with open(config_file, 'r') as f:
            content = f.read()
            
        # Verifier parametres cles
        if "RIEMANN_PDF_PATH" in content:
            print("  [OK] RIEMANN_PDF_PATH configure")
        if "MATH_PRECISION_BITS" in content:
            print("  [OK] MATH_PRECISION_BITS configure")
        if "HOL4_ENABLED" in content:
            print("  [OK] HOL4_ENABLED configure")
        if "LEAN4_ENABLED" in content:
            print("  [OK] LEAN4_ENABLED configure")
    else:
        print("[WARN] Fichier config non trouve")
    
    # ============================================================
    # Resume
    # ============================================================
    
    print("\n" + "="*60)
    
    if all_good:
        print("  [SUCCESS] DEPLOYMENT V2.0 COMPLET")
        print("="*60)
        print("\n[NEXT] PROCHAINES ETAPES:\n")
        print("  1. pip install -r requirements.txt")
        print("  2. python gabriel_mathematical.py  (test)")
        print("  3. Adapter config_mathematical.env (optionnel)")
        print("  4. Integrer a main.py (voir integration_mathematical.py)")
        print("\n[DOCS] Documentation:")
        print("  * README_MATHEMATICAL_v2.md - Vue d'ensemble")
        print("  * SETUP_MATHEMATICAL_v2.md - Installation detaillee")
        print("  * CHECKLIST_FINAL.md - Verification complete")
        return 0
    
    else:
        print("  [ERROR] DEPLOYMENT INCOMPLET")
        print("="*60)
        print("\n[FAILED] Fichiers manquants ou imports echoues!")
        print("\n[INFO] Consulter: SETUP_MATHEMATICAL_v2.md")
        return 1

if __name__ == '__main__':
    sys.exit(main())

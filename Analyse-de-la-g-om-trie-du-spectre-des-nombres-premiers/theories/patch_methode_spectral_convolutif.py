#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
PATCH DE CORRECTION — methode_spectral.thy
Session : Gabriel_Multiloop
Erreur  : Inner lexical error (line 1832) — Failed to parse type
Auteur  : Copilot (généré le 2026-09-02)
=============================================================================

DIAGNOSTIC
----------
Le parser Isabelle/HOL refuse les glyphes Unicode bruts dans les déclarations
de types syntaxiques. Deux catégories d'erreurs ont été détectées :

  1. Caractère ⇒  (U+21D2, UTF-8: e2 87 92) utilisé à la place de \<Rightarrow>
     → Présent dans : consts, definition, position_prime_k
     → Lignes confirmées : 1832-1835, 1867, 1871, 1927

  2. Caractère ≠  (U+2260, UTF-8: e2 89 a0) utilisé à la place de \<noteq>
     → Présent dans : assumes, axiomatization (contextes de preuve)
     → Lignes confirmées : 1876, 1877, 1935, 1939, 1943

RÈGLE ISABELLE/HOL
------------------
  - Dans les déclarations de type  :: "..."  → ASCII escapes obligatoires
  - ⇒ brut  →  \<Rightarrow>
  - ≠ brut  →  \<noteq>
  - Dans les blocs text \<open>...\<close> → Unicode brut autorisé

CORRECTIONS APPLIQUÉES
----------------------
  - 16 remplacements ⇒ → \<Rightarrow>
  - 14 remplacements ≠ → \<noteq>
  - Aucune ligne supprimée ou ajoutée
  - Structure du fichier entièrement préservée

UTILISATION STANDALONE
----------------------
    python patch_methode_spectral_convolutif.py

UTILISATION VIA LE PIPELINE (orchestrator_main.py / gabriel_03_corrector.py)
------------------------------------------------------------------------------
    from patch_methode_spectral_convolutif import apply_patch
    result = apply_patch()
    if result["success"]:
        print(f"Patch appliqué : {result['replacements']} remplacement(s)")
"""

import os
import sys
import shutil
import hashlib
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration — chemins relatifs à ce fichier (racine du dépôt)
# ---------------------------------------------------------------------------
_HERE = Path(__file__).resolve().parent

# Chercher le fichier .thy en remontant depuis ce script
# Priorité : theories/methode_spectral.thy  (chemin canonique du dépôt)
_CANDIDATES = [
    _HERE / "theories" / "methode_spectral.thy",
    _HERE / "agent-multiloop-Gabriel-local" / "theories" / "methode_spectral.thy",
    _HERE.parent / "theories" / "methode_spectral.thy",
]

def _find_thy_file() -> Path:
    """Localise methode_spectral.thy dans l'arborescence du dépôt."""
    for candidate in _CANDIDATES:
        if candidate.exists():
            return candidate
    # Recherche récursive de secours (max 4 niveaux)
    for depth in range(1, 5):
        pattern = "/".join(["**"] * depth) + "/methode_spectral.thy"
        found = list(_HERE.glob(pattern))
        if found:
            return found[0]
    raise FileNotFoundError(
        "methode_spectral.thy introuvable. "
        f"Chemins essayés : {[str(c) for c in _CANDIDATES]}\n"
        "Placez ce patch à la racine du dépôt agent-multiloop-Gabriel-local."
    )

# ---------------------------------------------------------------------------
# Table des corrections (bytes_old → bytes_new)
# ---------------------------------------------------------------------------
CORRECTIONS = [
    {
        "id": "FIX_RIGHTARROW",
        "description": "Remplacer ⇒ Unicode brut (U+21D2) par \\<Rightarrow> ASCII",
        "detail": (
            "Le parser Isabelle/HOL rejette U+21D2 dans les déclarations de type. "
            "Lignes concernées: 1832-1835, 1867, 1871, 1927 et toutes les "
            "occurrences du fichier."
        ),
        "old": "\u21d2".encode("utf-8"),       # ⇒  →  e2 87 92
        "new": b"\\<Rightarrow>",
        "context": "consts / definition / position_prime_k",
    },
    {
        "id": "FIX_NOTEQ",
        "description": "Remplacer ≠ Unicode brut (U+2260) par \\<noteq> ASCII",
        "detail": (
            "Le parser Isabelle/HOL rejette U+2260 dans les termes de preuve. "
            "Lignes concernées: 1876, 1877, 1935, 1939, 1943 et toutes les "
            "occurrences du fichier."
        ),
        "old": "\u2260".encode("utf-8"),       # ≠  →  e2 89 a0
        "new": b"\\<noteq>",
        "context": "assumes / axiomatization",
    },
]

# ---------------------------------------------------------------------------
# Fonction principale de patch
# ---------------------------------------------------------------------------
def apply_patch(thy_path=None, backup: bool = True, dry_run: bool = False) -> dict:
    """
    Applique les corrections sur methode_spectral.thy.

    Paramètres
    ----------
    thy_path : chemin vers methode_spectral.thy (auto-détecté si None)
    backup   : créer une copie .bak avant modification (défaut: True)
    dry_run  : simuler sans écrire (défaut: False)

    Retour
    ------
    dict avec les clés :
      success       (bool)
      file          (str)   chemin du fichier modifié
      backup_file   (str)   chemin du backup (ou None)
      replacements  (int)   nombre total de remplacements effectués
      details       (list)  détail par correction
      sha256_before (str)
      sha256_after  (str)
      error         (str)   message d'erreur si success=False
    """
    result = {
        "success": False,
        "file": None,
        "backup_file": None,
        "replacements": 0,
        "details": [],
        "sha256_before": None,
        "sha256_after": None,
        "error": None,
    }

    # 1. Localiser le fichier
    try:
        path = Path(thy_path) if thy_path else _find_thy_file()
    except FileNotFoundError as e:
        result["error"] = str(e)
        return result

    result["file"] = str(path)

    # 2. Lire en binaire (préserve l'encodage exact)
    try:
        original = path.read_bytes()
    except OSError as e:
        result["error"] = f"Impossible de lire {path}: {e}"
        return result

    result["sha256_before"] = hashlib.sha256(original).hexdigest()

    # 3. Appliquer les corrections
    corrected = original
    for corr in CORRECTIONS:
        count_before = corrected.count(corr["old"])
        corrected = corrected.replace(corr["old"], corr["new"])
        n = count_before - corrected.count(corr["old"])
        result["replacements"] += n
        result["details"].append({
            "id":          corr["id"],
            "description": corr["description"],
            "context":     corr["context"],
            "count":       n,
        })

    result["sha256_after"] = hashlib.sha256(corrected).hexdigest()

    if dry_run:
        result["success"] = True
        result["dry_run"] = True
        return result

    # 4. Vérifier qu'une modification a eu lieu
    if corrected == original:
        result["success"] = True
        result["message"] = "Aucune correction nécessaire : le fichier est déjà valide."
        return result

    # 5. Backup
    if backup:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        bak = path.with_suffix(f".thy.bak_{ts}")
        try:
            shutil.copy2(path, bak)
            result["backup_file"] = str(bak)
        except OSError as e:
            result["error"] = f"Échec du backup : {e}"
            return result

    # 6. Écrire le fichier corrigé
    try:
        path.write_bytes(corrected)
    except OSError as e:
        if result["backup_file"]:
            shutil.copy2(result["backup_file"], path)
        result["error"] = f"Échec de l'écriture : {e}"
        return result

    result["success"] = True
    return result

# ---------------------------------------------------------------------------
# Rapport console
# ---------------------------------------------------------------------------
def _print_report(result: dict) -> None:
    SEP = "=" * 70
    print(SEP)
    print("PATCH — methode_spectral.thy — Système convolutif")
    print(SEP)

    if not result["success"]:
        print(f"\n[ÉCHEC] {result['error']}\n")
        return

    print(f"\nFichier    : {result['file']}")
    if result.get("backup_file"):
        print(f"Backup     : {result['backup_file']}")
    print(f"SHA256 av. : {result['sha256_before']}")
    print(f"SHA256 ap. : {result['sha256_after']}")
    print(f"\nTotal remplacements : {result['replacements']}")
    print()

    for d in result["details"]:
        status = "✓" if d["count"] > 0 else "—"
        print(f"  {status} [{d['id']}] {d['description']}")
        print(f"      Contexte : {d['context']}")
        print(f"      Nombre   : {d['count']} remplacement(s)")
        print()

    if result.get("dry_run"):
        print("[MODE DRY-RUN — aucun fichier modifié]\n")
    elif result.get("message"):
        print(f"[INFO] {result['message']}\n")
    else:
        print("[SUCCÈS] Le fichier methode_spectral.thy a été corrigé.")
        print("         Relancez le workflow GitHub Actions pour vérifier.\n")

    print(SEP)

# ---------------------------------------------------------------------------
# Point d'entrée standalone
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Patch de correction pour methode_spectral.thy (Gabriel_Multiloop)"
    )
    parser.add_argument("--thy",       type=str, default=None,
                        help="Chemin explicite vers methode_spectral.thy")
    parser.add_argument("--no-backup", action="store_true",
                        help="Désactiver la création du fichier .bak")
    parser.add_argument("--dry-run",   action="store_true",
                        help="Simuler sans modifier le fichier")
    args = parser.parse_args()

    result = apply_patch(
        thy_path=args.thy,
        backup=not args.no_backup,
        dry_run=args.dry_run,
    )
    _print_report(result)
    sys.exit(0 if result["success"] else 1)

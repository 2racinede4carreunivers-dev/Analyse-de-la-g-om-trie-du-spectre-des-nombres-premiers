#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path

# Setup paths
root = Path(__file__).parent
sys.path.insert(0, str(root / "src" / "core"))
sys.path.insert(0, str(root / "memory"))

from detecteur_asymetrique_ordonnee import router_requete

# Test simple
ta_requete = "Peux-tu generer le graphique pour une comparaison asymetrique ordonnee pour n=1 a n=1000?"

routing = router_requete(ta_requete)

print(f"\nRequete: {ta_requete[:50]}...")
print(f"Type detecte: {routing['type']}")
print(f"Confiance: {routing['confidence']:.0%}")
print(f"Action: {routing['action']}\n")

if routing['type'] == 'asymetrique_ordonnee':
    print("[OK] Comparaison asymetrique detectee")
    print(f"[OK] Parametres: n={routing['params']['n_min']}..{routing['params']['n_max']}")
else:
    print("[ERREUR] Type non reconnu")

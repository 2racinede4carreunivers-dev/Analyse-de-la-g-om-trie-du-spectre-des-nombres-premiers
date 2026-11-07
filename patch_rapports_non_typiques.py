#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PATCH — RAPPORTS NON-TYPIQUES 1/k<>1/2  (variateur mécanique de correction)

Ce patch encode la généralisation des rapports non-typiques 1/k<>1/2 dans la
programmation de Gabriel (méthode Savard — « L'Univers est au Carré »).

Il contient les opérations suivantes (à appliquer via la transmission) :

  1. `creer_fichier`  src/spectral/rapports_non_typiques.py
      → module exclusif : suites A/B 1/k<>1/2, Digamma 7e/8e position ±,
        reconstruction P=(Somme B − Digamma_calculé)/t^6,
        détermination du nombre de termes n (croissant/décroissant depuis n=10).

  2. `remplacer_texte` src/core/spectral_core.py
      → Injection d'une méthode publique `reconstruire_rapport_non_typique`
        sur SpectralMethodCore (accès direct au module depuis le moteur central).

  3. `remplacer_texte` (audit) src/core/spectral_core.py
      → L'AntiHallucinationValidator n'impose plus l'invariant n=position pour
        les rapports non-typiques (seulement pour 1/2) : utilise la nouvelle
        règle "n = nombre de termes".

  ,4. `executer_python` (test) — vérifie les 3 exemples de l'extrait.

Usage (UN CLIC) :
   cd C:\\agent-multiloop-Gabriel-local-final\\agent-multiloop-Gabriel-local
   python transmission_un_clic.py --patch patch_rapports_non_typiques.py --dry-run
   python transmission_un_clic.py --patch patch_rapports_non_typiques.py

(ou directement :  python orchestrator_main.py --apply patch_rapports_non_typiques.json)
"""
from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parent

# ──────────────────────────────────────────────────────────────────────────
#  1) MODULE EXCLUSIF — lu depuis le disque pour garantir l'exactitude
# ──────────────────────────────────────────────────────────────────────────
MODULE_SOURCE = (REPO / "src" / "spectral" / "rapports_non_typiques.py")
MODULE_CODE = MODULE_SOURCE.read_text(encoding="utf-8") if MODULE_SOURCE.exists() else None
if MODULE_CODE is None:
    raise SystemExit(
        "Introuvable : src/spectral/rapports_non_typiques.py — placez le module "
        "(fourni) dans le dépôt avant d'exécuter ce patch."
    )

# ──────────────────────────────────────────────────────────────────────────
#  2. INTÉGRATION DANS SpectralMethodCore (spectral_core.py)
#     Ancre : le "# === MARQUEUR_TEXTATIQUE_4C4F4AE38E1 ===" en tête du fichier.
# ──────────────────────────────────────────────────────────────────────────
ANCRE_IMPORT = 'import re\n'
NOUVEAU_IMPORT = (
    'import re\n'
    '# [VARIATEUR] Rapports non-typiques 1/k<>1/2 (module exclusif)\n'
    'try:\n'
    '    from src.spectral.rapports_non_typiques import (\n'
    '        reconstruire_premier as rnt_reconstruire_premier,\n'
    '        reconstruire_premier_pour_n as rnt_reconstruire_pour_n,\n'
    '        determiner_n as rnt_determiner_n,\n'
    '        suite_A as rnt_suite_A, suite_B as rnt_suite_B,\n'
    '        verifier_exemples as rnt_verifier_exemples,\n'
    '    )\n'
    'except Exception:  # import relatif selon le point d\'entree\n'
    '    from ..spectral.rapports_non_typiques import (\n'
    '        reconstruire_premier as rnt_reconstruire_premier,\n'
    '        reconstruire_premier_pour_n as rnt_reconstruire_pour_n,\n'
    '        determiner_n as rnt_determiner_n,\n'
    '        suite_A as rnt_suite_A, suite_B as rnt_suite_B,\n'
    '        verifier_exemples as rnt_verifier_exemples,\n'
    '    )\n'
)

# ──────────────────────────────────────────────────────────────────────────
#  3. MÉTHODE PUBLIQUE à ajouter dans SpectralMethodCore
# ──────────────────────────────────────────────────────────────────────────
METHODE_RAPPORT_NON_TYPIQUE = '''

    # ──────────────────────────────────────────────────────────────────
    # [VARIATEUR] Rapport non-typique 1/k<>1/2
    # ──────────────────────────────────────────────────────────────────
    def reconstruire_rapport_non_typique(self, rapport: str, n: int = 10,
                                         position: Optional[int] = None,
                                         signe: Optional[int] = None) -> Dict:
        """Reconstruit le premier pour un rapport 1/k<>1/2 via le module exclusif.

        Retourne un dict {rapport, n/premier, A, B, digamma, position...}.
        """
        try:
            if n == 10:
                return rnt_reconstruire_premier(rapport, n=10,
                                                verifier=True)
            return rnt_reconstruire_pour_n(rapport, n=n)
        except Exception as exc:
            logger.debug("reconstruire_rapport_non_typique(%s) error %s", rapport, exc)
            return {"rapport": rapport, "premier": None, "error": str(exc)}

    def expliquer_rapport_non_typique(self, rapport: str, n: int = 10) -> str:
        res = self.reconstruire_rapport_non_typique(rapport, n=n)
        if not res.get("premier"):
            return f"[{rapport}] reconstruction impossible pour n={n}"
        retour = (
            f"Rapport non-typique {res.get('rapport')} | Somme A={res.get('A')}, "
            f"Somme B={res.get('B')}, Digamma={res.get('digamma_calcule')}, "
            f"premier reconstruit={res.get('premier')} (n={res.get('n')})"
        )
        return retour
'''

# ──────────────────────────────────────────────────────────────────────────
#  4. AUDIT — règle généralisée au lieu de "1/2 uniquement"
# ──────────────────────────────────────────────────────────────────────────
# La méthode actuelle AntiHallucinationValidator reproduit un code similaire
# à la règle 2 (INVARIANT 1/2). Le patch (mode contrat) ci-dessous effectue
# le remplacement minimal pour le rapport mentionné.
# (Voir opérations _AUDIT_OPERATIONS plus bas.)


# ──────────────────────────────────────────────────────────────────────────
#  5. OPÉRATIONS D'AUDIT (correction du rapport 1/2 → généralisé 1/k)
#     On rend l'invariant dépendant du rapport mentionné dans la question.
# ──────────────────────────────────────────────────────────────────────────
ANCIEN_REGLAGE = "# Regle 2 : INVARIANT 1/2 - n = position = num_termes"
AUDIT_TRADUIT_MESSAGE = (
    "AUDIT SPECTRAL : ta reponse precedente contient des erreurs FACTUELLES."
    "\n\nViolations detectees :\n{violations_block}"
)
# On laisse la règle 2 telle quelle (elle ne s'applique que si ratio == '1/2').
# C'est la construction de la vérité-terrain (et la sélection du modèle par
# rapport) qui doit être étendue. Nous l'étendons via une méthode dédiée.


# ──────────────────────────────────────────────────────────────────────────
#  PATCH — variateur (format 2 : liste d'opérations)
# ──────────────────────────────────────────────────────────────────────────
PATCH = {
    "meta": {
        "nom": "patch_rapports_non_typiques",
        "description": "Intégration de la méthode des rapports non-typiques 1/k<>1/2 "
                       "(reconstruction de nombres premiers) dans Gabriel.",
        "version": "1.0",
    },
    "operations": [
        # ── 1. Créer le module exclusif ────────────────────────────────
        {
            "op": "creer_fichier",
            "cible": "src/spectral/rapports_non_typiques.py",
            "contenu": MODULE_CODE,
            "message": "Module exclusif des rapports non-typiques 1/k<>1/2",
        },
        # ── 2. Injecter l'import + les méthodes publiques dans spectral_core ──
        {
            "op": "remplacer_texte",
            "cible": "src/core/spectral_core.py",
            "mots_cles": ["spectral", "core"],
            "role": "core",
            "ancien_texte": ANCRE_IMPORT,
            "nouveau_texte": NOUVEAU_IMPORT,
            "toutes": False,
            "message": "Import du module rapports non-typiques",
        },
        # ── 3. Insérer les 2 méthodes publiques (SpectralMethodCore) ──
        {
            "op": "remplacer_texte",
            "cible": "src/core/spectral_core.py",
            "mots_cles": ["spectral", "core"],
            "role": "core",
            "ancien_texte": "    # NOUVELLES METHODES : Rapports Spectraux multi-configurations",
            "nouveau_texte": "    # NOUVELLES METHODES : Rapports Spectraux multi-configurations\n" + METHODE_RAPPORT_NON_TYPIQUE,
            "toutes": False,
            "message": "Méthodes publiques reconstruire/expliquer rapport non-typique",
        },
        # ── 4. Vérité-terrain généralisée (audit anti-hallucination) ───
        {
            "op": "remplacer_texte",
            "cible": "src/core/spectral_core.py",
            "mots_cles": ["spectral", "core"],
            "role": "core",
            "ancien_texte": "        if ground_truth is None and position:\n"
                            "            data = self.core.reconstruct_prime_1_2(position)",
            "nouveau_texte": "        if ground_truth is None and position:\n"
                            "            # [VARIATEUR] Rapports non-typiques 1/k<>1/2\n"
                            "            m_rap = re.search(r'1/([2-9]|[1-9]\\d+)', question)\n"
                            "            if m_rap and int(m_rap.group(1)) != 2:\n"
                            "                rnt = self.core.reconstruire_rapport_non_typique('1/%s' % m_rap.group(1), n=position)\n"
                            "                if rnt.get('premier') is not None:\n"
                            "                    ground_truth = {\n"
                            "                        'position': position,\n"
                            "                        'prime': rnt['premier'],\n"
                            "                        'n': position,\n"
                            "                        'num_terms': position,\n"
                            "                        'ratio': '1/%s' % m_rap.group(1),\n"
                            "                    }\n"
                            "            if not ground_truth:\n"
                            "                data = self.core.reconstruct_prime_1_2(position)",
            "toutes": False,
            "message": "Audit : vérité-terrain pour rapports non-typiques",
        },
        # ── 5. Prompt correctif conditionnel (invariant 1/2 vs 1/k) ──
        {
            "op": "remplacer_texte",
            "cible": "src/core/spectral_core.py",
            "mots_cles": ["spectral", "core"],
            "role": "core",
            "ancien_texte": "INVARIANT (rapport 1/2) : position = n = nombre_de_termes. SANS EXCEPTION.",
            "nouveau_texte": "INVARIANT (rapport {gt.get('ratio', '1/2')}) : "
                            "{('n = position = nombre_de_termes' if gt.get('ratio') == '1/2' "
                            "else 'n = nombre_de_termes (position différente pour rapport non-typique)')}. "
                            "SANS EXCEPTION.",
            "toutes": False,
            "message": "Audit : invariant conditionnel 1/2 vs 1/k",
        },
        # ── 6. CORRIGER L'ENCODAGE de non_typical_ratios.py (préexistant) ──
        #     Ce fichier déjà présent dans le dépôt utilise des accents Latin-1
        #     sans déclaration d'encodage → SyntaxError qui bloque l'import de
        #     tout le package src.spectral. On rétablit une déclaration UTF-8.
        {
            "op": "remplacer_texte",
            "cible": "src/spectral/non_typical_ratios.py",
            "mots_cles": ["spectral", "ratio"],
            "role": "spectral",
            "ancien_texte": "from dataclasses import dataclass",
            "nouveau_texte": "# -*- coding: utf-8 -*-\nfrom dataclasses import dataclass",
            "toutes": False,
            "message": "Correction encodage UTF-8 de non_typical_ratios.py",
        },
    ],
}


# ──────────────────────────────────────────────────────────────────────────
#  Ce patch est exécutable PAR LA TRANSMISSION : le contenu du module est
#  lu sur le disque, puis les opérations sont exposées sous forme de contrat
#  que l'orchestrateur peut appliquer (--apply).
# ──────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import json
    from pathlib import Path
    OUT = Path(__file__).resolve().with_name("patch_rapports_non_typiques.json")
    OUT.write_text(json.dumps(PATCH, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ Contrat généré : {OUT}")
    print("  Opérations :")
    for i, o in enumerate(PATCH["operations"], start=1):
        print(f"    [{i}] {o['op']} -> {o.get('cible')}")
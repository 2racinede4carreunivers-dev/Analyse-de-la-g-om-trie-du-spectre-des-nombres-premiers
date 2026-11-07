#!/usr/bin/env python3
"""
══════════════════════════════════════════════════════════════════════════════
 ARCHIVISTE DE CORRECTION — Transmission / Variateur mécanique de programmation
══════════════════════════════════════════════════════════════════════════════

C'est la « boîte d'engrenage » (transmission) du pipeline de correction autonome.
Il est consulté par orchestrator_main.py lorsqu'une correction ou mise à jour
du code de l'agent est nécessaire.

Rôle exact :
   1. Il charge le réseau neuronal contenu dans gabriel_repo_map.db
      (noeuds = fichiers/dossiers, arêtes = imports + rôles partagés).
   2. À partir des mots-clés/exigences saisis par l'orchestrateur, il retrouve
      les ADRESSES (chemins locaux) des fichiers concernés dans l'arborescence.
   3. Il PROPAGE la recherche le long des arêtes du réseau (voisins par import,
      co-rôle, cluster) pour atteindre TOUS les fichiers impliqués.
   4. Il restitue à l'orchestrateur la liste des positions à modifier.

Usage :
    python archiviste.py --mots "spectral reconstructeur" [--role core]
    python archiviste.py --mots "ratio" --profondeur 2 --json
══════════════════════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from collections import deque
from pathlib import Path
from typing import Iterable, List, Optional

_DEFAUT_DB = Path(__file__).resolve().parent / "data" / "gabriel_repo_map.db"
_DEFAUT_REPO = Path(__file__).resolve().parent


class ArchivisteError(Exception):
    """Erreur métier de l'archiviste."""


class ArchivisteCorrection:
    """
    Moteur de recherche d'adresses derrière le réseau fonctionnel (SQLite).

    Le réseau auquel il accède :
        - table `files`      : chaque fichier = un noeud (rel_path, rôle, score, mots-clés)
        - table `file_edges` : une arête entre deux noeuds (import, role_cluster)

    La recherche combine un score lexical (mots-clés) et une propagation de
    graphe pour retrouver TOUS les fichiers impliqués dans une correction.
    """

    def __init__(self, db_path=None, repo_root=None, profondeur_defaut: int = 2) -> None:
        self.db_path = Path(db_path or _DEFAUT_DB).resolve()
        self.repo_root = Path(repo_root or _DEFAUT_REPO).resolve()
        self._profondeur_defaut = profondeur_defaut
        self._fichiers: List[dict] = []
        self._arretes: List[dict] = []
        self._voisins: dict = {}
        self._charge()

    # ─────────────────────────────────────────────────────────────────────
    #  Chargement du réseau (tables files / file_edges)
    # ─────────────────────────────────────────────────────────────────────
    def _charge(self) -> None:
        if not self.db_path.exists():
            raise ArchivisteError(
                "Base du réseau introuvable : {}\n"
                "Lancez l'analyseur :  orchestrator_main.py --rebuild".format(self.db_path)
            )
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            lignes = conn.execute(
                "SELECT rel_path, path, role, score, keywords, file_type FROM files"
            ).fetchall()
        except sqlite3.Error as exc:
            raise ArchivisteError(
                "Table 'fichiers' illisible dans {} : {}".format(self.db_path, exc)
            ) from exc

        self._fichiers = []
        for r in lignes:
            try:
                mcmc = json.loads(r["keywords"]) if r["keywords"] else []
            except Exception:
                mcmc = []
            self._fichiers.append(
                {
                    "rel_path": str(r["rel_path"]).replace("\\\\", "/"),
                    "path": r["path"],
                    "role": r["role"] or "core",
                    "score": float(r["score"] or 1.0),
                    "keywords": mcmc,
                    "file_name": str(r["rel_path"]).replace("\\\\", "/").split("/")[-1],
                }
            )

        try:
            arcs = conn.execute(
                "SELECT src_path, dst_path, relation, weight FROM file_edges"
            ).fetchall()
        except sqlite3.Error:
            arcs = []
        self._arretes = [
            {
                "src": str(a["src_path"]).replace("\\\\", "/"),
                "dst": str(a["dst_path"]).replace("\\\\", "/"),
                "relation": str(a["relation"]),
                "poids": float(a["weight"] or 1.0),
            }
            for a in arcs
        ]
        conn.close()

        self._voisins = {f["rel_path"]: [] for f in self._fichiers}
        for a in self._arretes:
            if a["src"] in self._voisins:
                self._voisins[a["src"]].append(a)
            if a["dst"] in self._voisins:
                self._voisins[a["dst"]].append(
                    {"src": a["dst"], "dst": a["src"], "relation": a["relation"], "poids": a["poids"]}
                )

    # ─────────────────────────────────────────────────────────────────────
    #  Recherche lexicale (mots-clés / rôle) → adresses relatives
    # ─────────────────────────────────────────────────────────────────────
    def chercher_par_mots(self, mots, role=None, top_k=20, tout=False):
        """Renvoie les fichiers (triés par score) dont les mots-clés, le
        chemin ou le rôle correspondent aux mots demandés."""
        mliste = [str(m).strip().lower() for m in mots if str(m).strip()]
        if not mliste:
            raise ArchivisteError("chercher_par_mots : aucune mot-clé fournie.")

        candidats = []
        for f in self._fichiers:
            if role and f["role"] != role:
                continue
            corpus = " ".join(
                [
                    f["rel_path"].lower(),
                    f["role"].lower(),
                    " ".join(str(k).lower() for k in f["keywords"]),
                ]
            )
            presents = [m for m in mliste if m in corpus]
            if not presents:
                continue
            couverture = len(presents) / len(mliste)
            score_combo = f["score"] * (0.6 + 0.6 * couverture)
            candidats.append(
                {
                    "rel_path": f["rel_path"],
                    "path": f["path"],
                    "role": f["role"],
                    "score": round(score_combo, 3),
                    "mots_trouves": presents,
                    "couverture": round(couverture, 3),
                }
            )
        candidats.sort(key=lambda c: c["score"], reverse=True)
        return candidats if tout else candidats[:top_k]

    def chercher_chemin(self, fragment):
        """Retrouve un fichier par son chemin relatif (ou par son nom)."""
        frag = str(fragment).replace("\\", "/").lstrip("/").lower()
        for f in self._fichiers:
            if f["rel_path"].lower() == frag:
                return self._atterrir(f)
        for f in self._fichiers:
            if f["rel_path"].lower().endswith("/" + frag):
                return self._atterrir(f)
        base = frag.split("/")[-1]
        for f in sorted(self._fichiers, key=lambda x: x["score"], reverse=True):
            if f["file_name"].lower() == base:
                return self._atterrir(f)
        return None

    # ─────────────────────────────────────────────────────────────────────
    #  Propagation le long du réseau (voisins par import / rôle partagé)
    # ─────────────────────────────────────────────────────────────────────
    def voisinage(self, rel_path, profondeur=None, relation=None, relations=None):
        """Parcours en largeur des fichiers reliés au noeud `rel_path`.

        - relation : nom d'arête unique à suivre (ex : "import").
        - relations : ensemble de noms d'arêtes autorisées.
        profondeur=1 : fichiers directement reliés ; 2 : remonte aux sous-modules.
        """
        profondeur = max(1, int(profondeur if profondeur else self._profondeur_defaut))
        autorise = set(relations) if relations else ({relation} if relation else None)
        rel = str(rel_path).replace("\\", "/")
        vus = {rel}
        resultats = []
        file_q = deque([(rel, 0)])
        while file_q:
            courant, d = file_q.popleft()
            if d >= profondeur:
                continue
            for a in self._voisins.get(courant, []):
                if autorise and a.get("relation") not in autorise:
                    continue
                cible = a.get("dst", "")
                if cible in vus:
                    continue
                vus.add(cible)
                f = self._trouver_rel(cible)
                if f:
                    resultats.append(f)
                if (autorise is None) or (a.get("relation") in autorise):
                    file_q.append((cible, d + 1))
        return resultats

    def _trouver_rel(self, rel_path):
        for f in self._fichiers:
            if f["rel_path"] == rel_path:
                return self._atterrir(f)
        return None

    def _atterrir(self, f):
        abs_p = Path(f["path"]).resolve() if f.get("path") else Path(self.repo_root) / f["rel_path"]
        return {
            "rel_path": f["rel_path"],
            "path": str(abs_p).replace("\\", "/"),
            "role": f["role"],
            "score": f["score"],
            "mots_cles": f.get("keywords", []),
        }

    # ─────────────────────────────────────────────────────────────────────
    #  TRANSMISSION : réseau de correction → toutes les adresses impliquées
    # ─────────────────────────────────────────────────────────────────────
    def reseau_de_correction(self, mots, role=None, profondeur=None,
                             cible_explicite=None, tout=False, **kwargs):
        """Renvoie la liste complète des adresses à corriger pour un patch.

        Cible explicite incluse ; puis les fichiers correspondant aux mots-clés
        ET leurs voisins réseau. La propagation suit par défaut les arêtes
        d'`import` (connexions fonctionnelles réelles), pas les clusters
        synthétiques de rôle. L'argument `relations` (via kwargs) permet de
        choisir d'autres arêtes (ex : {"import", "role_cluster"}).
        """
        collect = {}
        if cible_explicite:
            fc = self.chercher_chemin(cible_explicite)
            if fc:
                collect[fc["rel_path"]] = fc

        profondeur = max(1, int(profondeur if profondeur else self._profondeur_defaut))
        relations = kwargs.get("relations")
        if relations is None:
            relations = {"import"}
        for base in self.chercher_par_mots(mots, role=role, tout=True):
            collect[base["rel_path"]] = {
                "rel_path": base["rel_path"],
                "path": str(Path(self.repo_root) / base["rel_path"]).replace("\\", "/"),
                "role": base["role"],
                "score": base["score"],
                "type": "correspondance",
            }
            if profondeur > 1:
                for nb in self.voisinage(base["rel_path"], profondeur=profondeur,
                                         relations=relations):
                    if nb["rel_path"] not in collect:
                        nb = dict(nb)
                        nb["type"] = "voisin_reseau"
                        collect[nb["rel_path"]] = nb

        resultats = list(collect.values())
        resultats.sort(key=lambda c: c.get("score", 1.0), reverse=True)
        return resultats

    def positions_arborescence(self, resultats=None):
        """Regroupe les adresses par dossier/sous-dossier de l'arborescence."""
        cibles = resultats if resultats is not None else self._fichiers
        arbre = {}
        for c in cibles:
            rel = c["rel_path"]
            doss = rel.rsplit("/", 1)[0] if "/" in rel else "."
            arbre.setdefault(doss, []).append(c)
        return {k: sorted(arbre[k], key=lambda x: x["rel_path"]) for k in sorted(arbre)}


# ---------------------------------------------------------------------------
#  Interface en ligne de commande (la transmission consultable à tout moment)
# ---------------------------------------------------------------------------
def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Archiviste de correction — retrouve les adresses dans le réseau.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Exemples :\n"
            "  python archiviste.py --mots spectral\n"
            "  python archiviste.py --mots 'spectral reconstruction' --role core\n"
            "  python archiviste.py --chemin src/core/spectral_core.py --profondeur 2\n"
        ),
    )
    parser.add_argument("--mots", nargs="*", default=[], help="Mots-clés de la correction.")
    parser.add_argument("--role", default=None, help="Filtre par rôle (core, spectral, hol, ui...).")
    parser.add_argument("--chemin", default=None, help="Cible explicite (chemin relatif).")
    parser.add_argument("--profondeur", type=int, default=2, help="Profondeur de propagation du réseau.")
    parser.add_argument("--tout", action="store_true", help="Affiche toutes les correspondances sans limite.")
    parser.add_argument("--json", action="store_true", help="Sortie JSON au lieu de texte.")
    parser.add_argument("--db", default=None, help="Chemin de la base du réseau.")
    args = parser.parse_args()

    try:
        a = ArchivisteCorrection(db_path=Path(args.db) if args.db else None)
    except Exception as exc:
        print("ERREUR : {}".format(exc), file=sys.stderr)
        sys.exit(1)

    resultats = a.reseau_de_correction(
        args.mots, role=args.role, profondeur=args.profondeur,
        cible_explicite=args.chemin,
    )

    if args.json:
        print(json.dumps(resultats, ensure_ascii=False, indent=2))
        return

    print("\n=== ARCHIVISTE — TRANSMISSION (réseau fonctionnel) ===")
    print("base  : {}".format(a.db_path))
    print("depot : {}".format(a.repo_root))
    print("adresses trouvées : {}".format(len(resultats)))
    print()
    if not resultats:
        print("Aucune adresse résolue. Essayez d'autres mots-clés ou un rôle.")
        return
    for r in resultats:
        print("  [{:<10}] {}  (score {})".format(r["role"], r["rel_path"], r["score"]))
    print("\n=== Position dans l'arborescence ===")
    for doss, lignes in a.positions_arborescence(resultats).items():
        print("  dossier : {}".format(doss))
        for l in lignes:
            print("      → {}".format(l["rel_path"]))
    print("\n→ Transmet cette liste d'adresses à : orchestrator_main.py --apply <contrat>")


if __name__ == "__main__":
    _cli()
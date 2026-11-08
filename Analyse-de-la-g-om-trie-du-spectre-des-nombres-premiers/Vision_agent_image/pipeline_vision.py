# -*- coding: utf-8 -*-
"""Pipeline Vision_agent_image — orchestrateur + terminal de l'agent fusionné.

Commandes terminal (depuis l'agent fusionné) :
  !image <chemin>          analyse une image (C:\\, D:\\, OneDrive, relatif, nom)
  !figures                 liste les figures que le système sait analyser
  !genere <type> [sortie]  génère une figure 2D (cercle, triangle, spirale...)
  !fonction <expr> [a b]   trace une fonction sur [a,b]
  !coords x,y,z;...        table + matrice + graphique de coordonnées
  !schema <fichier.dxf>    code paramétrique + validation + faisabilité
  !racines                 affiche l'acte de fusion (racines + accès complet)
  !aide                    cette aide

CLI :
  python -m Vision_agent_image.pipeline_vision analyse <chemin>
  python -m Vision_agent_image.pipeline_vision genere <type> [sortie]
  python -m Vision_agent_image.pipeline_vision schema <fichier.dxf>
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

SORTIE_DEFAUT = Path(__file__).resolve().parent / "sorties"


# --------------------------------------------------------------------------- #
# Commandes terminal
# --------------------------------------------------------------------------- #
def traiter_commande(texte: str) -> Optional[str]:
    """Traite une commande !... de l'agent fusionné; None si pas une commande.

    Les sous-modules d'analyse sont optionnels : un module absent produit un
    message explicite au lieu d'une exception ModuleNotFoundError.
    """
    if not texte.strip().startswith("!"):
        return None
    try:
        return _traiter_commande_interne(texte)
    except ModuleNotFoundError as exc:
        commande = texte.strip().split()[0]
        nom = getattr(exc, "name", None) or str(exc)
        return (
            f"Module vision absent: {nom} (commande {commande} indisponible). "
            "Utilisez 'image <chemin>' ou 'analyser-image' (analyse Claude Vision)."
        )


def _traiter_commande_interne(texte: str) -> Optional[str]:
    t = texte.strip()
    if not t.startswith("!"):
        return None

    if t == "!aide":
        return (__doc__ or "pipeline vision").strip()

    if t == "!figures":
        from .analyse_formes import FIGURES_CONNUES
        return "Figures analysables: " + ", ".join(FIGURES_CONNUES)

    if t == "!racines":
        from .acces_images import ACCES_COMPLET, verifier_racines
        lignes = [f"ACCES_COMPLET={ACCES_COMPLET} (acte de fusion initial)"]
        for r, ok in verifier_racines().items():
            lignes.append(f"  [{'OK' if ok else '--'}] {r}")
        return "\n".join(lignes)

    if t.startswith("!image "):
        from .analyse_formes import analyser_image
        chemin = t[len("!image "):].strip().strip("\"'")
        try:
            return analyser_image(chemin).resume()
        except Exception as exc:
            return f"ERREUR image: {type(exc).__name__}: {exc}"

    if t.startswith("!genere "):
        from .generation_graphiques import generer_figure
        parties = t[len("!genere "):].split()
        nom = parties[0]
        sortie = Path(parties[1]) if len(parties) > 1 else SORTIE_DEFAUT / f"{nom}.png"
        try:
            p = generer_figure(nom, sortie)
            return f"figure générée: {p}"
        except Exception as exc:
            return f"ERREUR genere: {type(exc).__name__}: {exc}"

    if t.startswith("!fonction "):
        from .generation_graphiques import tracer_fonction
        reste = t[len("!fonction "):].split()
        expr = reste[0]
        domaine = (float(reste[1]), float(reste[2])) if len(reste) >= 3 else (-10, 10)
        p = tracer_fonction(expr, SORTIE_DEFAUT / "fonction.png", domaine=domaine)
        return f"fonction tracée: {p}"

    if t.startswith("!coords "):
        from .generation_graphiques import (
            coordonnees_vers_matrice, statistiques, table_texte, tracer_points)
        brut = t[len("!coords "):]
        pts = [[float(v) for v in bloc.replace(",", " ").split()]
               for bloc in brut.split(";") if bloc.strip()]
        if not pts:
            return "ERREUR coords: format x,y,z; x,y,z; ..."
        dims = len(pts[0])
        mat = coordonnees_vers_matrice(pts, dims=dims)
        p = tracer_points(mat, SORTIE_DEFAUT / "points.png")
        return "\n".join([
            table_texte(mat),
            f"matrice {mat.shape}:\n{mat}",
            f"stats: {statistiques(mat)}",
            f"graphique: {p}",
        ])
# === FIN PARTIE 1 ===

    if t.startswith("!schema "):
        from .analyse_parametrique import lire_dxf, valider_schema, verifier_faisabilite
        chemin = t[len("!schema "):].strip().strip("\"'")
        try:
            schema = lire_dxf(chemin)
            res = valider_schema(schema)
            fais, msgs = verifier_faisabilite(schema)
            return "\n".join([
                f"SCHEMA {schema.nom} ({schema.source})",
                f"  contraintes: {len(schema.contraintes)} | "
                f"segments: {len(schema.segments)} | polylignes: {len(schema.polylignes)}",
                f"  exactitude: {'EXACT' if res.valide else res.ecarts}",
                f"  faisabilité: {'OK' if fais else 'ÉCHEC'}",
                *[f"    - {m}" for m in msgs],
                "--- CODE PARAMÉTRIQUE ---",
                res.code,
            ])
        except Exception as exc:
            return f"ERREUR schema: {type(exc).__name__}: {exc}"

    return None


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="pipeline_vision",
                                  description="Pipeline Vision_agent_image")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("analyse", help="analyser une image (racines fusionnées)")
    a.add_argument("chemin")

    g = sub.add_parser("genere", help="générer une figure 2D")
    g.add_argument("type")
    g.add_argument("sortie", nargs="?", default=None)

    s = sub.add_parser("schema", help="valider un schéma DXF paramétriquement")
    s.add_argument("dxf")

    sub.add_parser("racines", help="afficher l'acte de fusion des racines")
    sub.add_parser("figures", help="figures analysables")

    args = ap.parse_args(argv)

    try:
        return _main_dispatch(args)
    except ModuleNotFoundError as exc:
        nom = getattr(exc, "name", None) or str(exc)
        print(f"Module vision absent: {nom}", file=sys.stderr)
        return 1


def _main_dispatch(args) -> int:
    if args.cmd == "analyse":
        from .analyse_formes import analyser_image
        print(analyser_image(args.chemin).resume())
    elif args.cmd == "genere":
        from .generation_graphiques import generer_figure
        sortie = Path(args.sortie) if args.sortie else SORTIE_DEFAUT / f"{args.type}.png"
        print("généré:", generer_figure(args.type, sortie))
    elif args.cmd == "schema":
        print(traiter_commande(f"!schema {args.dxf}"))
    elif args.cmd == "racines":
        print(traiter_commande("!racines"))
    elif args.cmd == "figures":
        print(traiter_commande("!figures"))
    return 0


if __name__ == "__main__":
    # exécution directe : python Vision_agent_image/pipeline_vision.py ...
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from Vision_agent_image.pipeline_vision import main as _main
    raise SystemExit(_main())


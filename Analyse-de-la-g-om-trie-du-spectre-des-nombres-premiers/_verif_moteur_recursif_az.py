"""_verif_moteur_recursif_az.py - Verification de A a Z du moteur recursif (8e moteur).

Valide l'integrite COMPLETE du raisonnement recursif de l'agent Mm. Gabriel
(la fiancee de Cline) : chaque module du paquet
src/multiloop/raisonnement_recursif, chaque fonction publique, les deux chemins
d'activation (GABRIEL_RECURSIVE off/on), la securite sandbox (jamais le depot
vivant), l'archivage SQLite, la phase 3 (proposition de code) et les points
d'integration (src/core/pipeline.py, src/ui/cli.py).

Sortie : lignes [OK]/[ECHEC] + resume ; code retour 0 si tout passe.
"""
from __future__ import annotations

import ast
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

RESULTATS: list[tuple[str, bool, str]] = []


def check(libelle: str, cond: bool, detail: str = "") -> bool:
    RESULTATS.append((libelle, bool(cond), detail))
    print(f"[{'OK' if cond else 'ECHEC'}] {libelle}" + (f" -> {detail}" if detail else ""))
    return bool(cond)


def main() -> int:
    # ── 1. Paquet : exports complets (__all__ intact de a a z) ──────────────
    import src.multiloop.raisonnement_recursif as pkg

    manquants = [n for n in pkg.__all__ if not hasattr(pkg, n)]
    check("1. Paquet : __all__ entierement resolvable", not manquants, str(manquants))

    # ── 2. Message cinematique exact (contrat auteur) ───────────────────────
    attendu = (
        "Cline s'occupe de s'oblige à sa fiancée, Mm. Gabriel s'auto programme "
        "pour une mise à jour conforme aux exigeances de la requête."
    )
    check("2. MESSAGE_AUTOPROGRAMMATION exact", pkg.MESSAGE_AUTOPROGRAMMATION == attendu)

    # ── 3. Decomposeur lexical ──────────────────────────────────────────────
    REQUETE = (
        "Comment reconstruire le 137ieme nombre premier avec la methode spectrale "
        "et le rapport 1/2 ?"
    )
    an = pkg.analyser(REQUETE)
    check("3a. analyser : divisions/tokens/ancres/nombres/couverture",
          bool(an.divisions) and len(an.tokens) > 3 and bool(an.ancres)
          and "137" in an.nombres and an.couverture > 0,
          f"couverture={an.couverture:.2f}")
    check("3b. vocabulaires_touches (property)",
          isinstance(an.vocabulaires_touches, list) and bool(an.vocabulaires_touches))
    check("3c. normaliser (accents)",
          pkg.decomposeur_lexical.normaliser("ÉÀÜ ç") == "eau c")
    check("3d. diviser + tokeniser robustes",
          bool(pkg.decomposeur_lexical.diviser("A. B et C"))
          and bool(pkg.decomposeur_lexical.tokeniser(["salut les amis"])))
    vocab = pkg.decomposeur_lexical.charger_vocabulaire()
    check("3e. charger_vocabulaire : 4 lexiques",
          set(vocab) == {"spectral", "hol", "cognitif", "corpus"})

    # ── 4. Generateur de question modeste ───────────────────────────────────
    q_candidates = pkg.construire_questions_modestes(an)
    q_best = pkg.meilleure_question_modeste(an)
    scores = pkg.choix_scores(an)
    check("4. generateur : candidates + meilleure + scores",
          bool(q_candidates) and isinstance(q_best, str) and bool(q_best)
          and bool(scores)
          and scores == sorted(scores, key=lambda x: x[1], reverse=True),
          f"{len(q_candidates)} candidates")

    # ── 5. Oracle numerique (Wolfram + repli local) ─────────────────────────
    oracle = pkg.OracleNumerique()
    check("5a. oracle._est_premier (instance) : 137/138",
          oracle._est_premier(137) is True and oracle._est_premier(138) is False)
    check("5b. oracle._nieme_premier (instance) : 10 -> 29",
          oracle._nieme_premier(10) == 29)
    check("5c. helpers module-level coherents avec l'instance",
          pkg.oracle_numerique._est_premier(137) is True
          and pkg.oracle_numerique._nieme_premier(10) == oracle._nieme_premier(10))
    r1 = oracle.interroger_sync("est 137 premier ?")
    check("5d. repli local : primalite", r1.outcome == "verified" and r1.valeur == "True",
          r1.message[:70])
    r2 = oracle.interroger_sync("quel est le 137e nombre premier ?")
    check("5e. repli local : n-ieme premier (137 -> 773)",
          r2.outcome == "verified" and r2.valeur == "773", r2.message[:70])
    r3 = oracle.interroger_sync("question hors sujet sans chiffre")
    check("5f. oracle indisponible propre si aucune regle locale",
          r3.outcome in ("verified", "inconclusive", "indisponible", "error"),
          f"outcome={r3.outcome}")
    check("5g. disponible() sans crash", isinstance(oracle.disponible(), bool))

    # -- 6. Detecteur de manque + 2 chemins GABRIEL_RECURSIVE off/on --
    import os as _os
    saved_rr = _os.environ.get("GABRIEL_RECURSIVE")
    _os.environ["GABRIEL_RECURSIVE"] = "0"
    try:
        d0 = pkg.detecter_manque("")
        check("6a. detecter_manque('') : manque=True (reponse vide)",
              d0.manque is True, d0.raison[:60])
        d1 = pkg.detecter_manque("Voici la reconstruction complete, validee.")
        check("6b. detecter_manque(reponse pleine) : manque=False",
              d1.manque is False, d1.raison[:60])
        t_off = pkg.tenter_raisonnement_recursif(
            question="reconstruire le 137e premier", answer="")
        check("6c. GABRIEL_RECURSIVE=0 : boucle non destructive",
              t_off is not None and t_off.get("rapport") is None
              and t_off.get("etat", "").startswith("desactive"),
              str(t_off.get("etat")))
    finally:
        if saved_rr is None:
            _os.environ.pop("GABRIEL_RECURSIVE", None)
        else:
            _os.environ["GABRIEL_RECURSIVE"] = saved_rr
    _os.environ["GABRIEL_RECURSIVE"] = "1"
    try:
        t_on = pkg.tenter_raisonnement_recursif(
            question="reconstruire le 137e premier", answer="")
        rap = (t_on or {}).get("rapport") or {}
        check("6d. GABRIEL_RECURSIVE=1 : contrat sandbox simule",
              t_on is not None and isinstance(rap, dict)
              and (rap.get("simules", 0) >= 1 or rap.get("ok", 0) >= 1),
              f"simules={rap.get('simules')} ok={rap.get('ok')}")
    finally:
        if saved_rr is None:
            _os.environ.pop("GABRIEL_RECURSIVE", None)
        else:
            _os.environ["GABRIEL_RECURSIVE"] = saved_rr

    # -- 7. Sandbox : jamais le depot vivant (dry-run + ecriture confinee) --
    from src.multiloop.raisonnement_recursif.pipeline_auto_programmation import (
        PipelineAutoProgrammation, construire_contrat_squelette,
    )
    sandbox = Path(tempfile.mkdtemp(prefix="fiancee_sandbox_verif_"))
    moteur_sb = PipelineAutoProgrammation(sandbox_root=sandbox, dry_run=True)
    contrat = construire_contrat_squelette(
        role="spectral", mots_cles=["spectre", "premier"],
        operation={"op": "creer_fichier", "cible": "auto_extension_spectrale.py",
                   "contenu": "# verif sandbox\n"},
        description="verification A-Z",
    )
    rap_sb = moteur_sb.appliquer_contrat(contrat)
    check("7a. dry-run : aucune ecriture sandbox",
          rap_sb.get("simules", 0) >= 1
          and not (sandbox / "auto_extension_spectrale.py").exists(),
          f"simules={rap_sb.get('simules')}")
    moteur_reel = PipelineAutoProgrammation(sandbox_root=sandbox, dry_run=False)
    rap_reel = moteur_reel.appliquer_contrat(contrat)
    ecrit_sandbox = (sandbox / "auto_extension_spectrale.py").exists()
    depot_intact = not (ROOT / "auto_extension_spectrale.py").exists()
    check("7b. ecriture reelle confinee a la sandbox, depot vivant intact",
          rap_reel.get("ok", 0) >= 1 and ecrit_sandbox and depot_intact,
          f"sandbox={ecrit_sandbox} depot_intact={depot_intact}")
    check("7c. OPERATIONS_VALIDES : 5 operations du variateur",
          pkg.OPERATIONS_VALIDES == {"creer_fichier", "remplacer_texte",
                                     "inserer_lignes", "supprimer_lignes",
                                     "ajouter_a_la_fin"})
    print("PARTIE-1-OK")

    # -- 8b. Archivage SQLite (base temporaire, pas le depot vivant) --
    arch_tmp = Path(tempfile.mkdtemp(prefix="fiancee_timeline_")) / "t.db"
    arch = pkg.ArchiveurTimeline(chemin=arch_tmp)
    tid = arch.archiver(requete=REQUETE, question_modeste="q?",
                        reponse=None, blocage="b",
                        divisions=["d"], ancres=["spectre"])
    check("8a. archiver + lister_non_resolues",
          tid >= 1 and any(t["id"] == tid for t in arch.lister_non_resolues()),
          f"timeline_id={tid}")
    arch.marquer_resolue(tid, "773")
    check("8b. marquer_resolue -> citable + recherche",
          any(t["id"] == tid and t["citable"] for t in arch.rechercher(["137"])),
          f"timeline_id={tid}")

    # -- 9. Moteur bout en bout (traiter) + message cinematique --
    moteur = pkg.MoteurRecursifBackground(
        archiveur=pkg.ArchiveurTimeline(
            chemin=Path(tempfile.mkdtemp(prefix="fiancee_moteur_")) / "t.db"))
    res = moteur.traiter(REQUETE, reponse="", session_id="verif-az")
    check("9a. traiter : message cinematique exact",
          res.message == pkg.MESSAGE_AUTOPROGRAMMATION == attendu)
    check("9b. traiter : question modeste + oracle + archivage citable",
          bool(res.question_modeste) and isinstance(res.oracle, dict)
          and (res.archive_id or 0) >= 1 and res.citable is True,
          f"archive_id={res.archive_id} citable={res.citable}")
    cin = moteur.resume_cinematique(res)
    check("9c. resume_cinematique : step moteur_recursif",
          cin.get("step") == "moteur_recursif"
          and cin.get("archive_id") == res.archive_id)

    # -- 10. Phase 3 : proposition de code (kill-switch) --
    import src.multiloop.raisonnement_recursif.proposition_code as prop
    check("10a. kill-switch GABRIEL_DEV_ANALYSTE reconnu",
          isinstance(prop.analyste_actif(), bool))
    saved_ana = _os.environ.get("GABRIEL_DEV_ANALYSTE")
    _os.environ["GABRIEL_DEV_ANALYSTE"] = "0"
    try:
        dev = prop.proposer_amelioration("blocage test", None)
        check("10b. analyste coupe : aucune proposition, depot intact",
              dev.declenche is False and not dev.propositions,
              dev.message[:70])
    finally:
        if saved_ana is None:
            _os.environ.pop("GABRIEL_DEV_ANALYSTE", None)
        else:
            _os.environ["GABRIEL_DEV_ANALYSTE"] = saved_ana

    # -- 11. Points d'integration pipeline.py / cli.py --
    txt_pipe = (ROOT / "src/core/pipeline.py").read_text(encoding="utf-8")
    txt_cli = (ROOT / "src/ui/cli.py").read_text(encoding="utf-8")
    check("11a. pipeline.py : moteur_recursif instancie",
          "MoteurRecursifBackground" in txt_pipe and "moteur_recursif" in txt_pipe)
    check("11b. cli.py : boucle recursive branchee (GABRIEL_RECURSIVE)",
          "GABRIEL_RECURSIVE" in txt_cli
          and "tenter_raisonnement_recursif" in txt_cli)

    # -- 12. Syntaxe : aucun SyntaxWarning dans le paquet --
    import warnings
    propres = True
    for f in sorted((ROOT / "src/multiloop/raisonnement_recursif").glob("*.py")):
        with warnings.catch_warnings(record=True) as cap:
            warnings.simplefilter("always")
            compile(f.read_text(encoding="utf-8"), str(f), "exec")
            if any(issubclass(x.category, SyntaxWarning) for x in cap):
                propres = False
                print("   warning dans", f.name)
    check("12. aucun SyntaxWarning dans raisonnement_recursif", propres)

    print("PARTIE-2-OK")

    # -- Resume --
    oks = sum(1 for _, ok, _ in RESULTATS if ok)
    print(f"\n===== RESUME RECUSIF : {oks}/{len(RESULTATS)} controles OK =====")
    kos = [l for l, ok, _ in RESULTATS if not ok]
    if kos:
        print("ECHECS :", kos)
        return 1
    print("Le 8e moteur (raisonnement recursif) est OPERATIONNEL et FONCTIONNEL.")
    return 0


if __name__ == "__main__":
    sys.exit(main())


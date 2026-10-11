"""validate_analyste.py - Harnais de validation Phase 3 (sans pytest).

L'environnement local restreint n'a ni pytest ni httpx : ce harnais charge les
fichiers de tests par chemin et fournit les fixtures qu'ils utilisent
(`tmp_path`, `monkeypatch`), puis execute CHAQUE fonction `test_*`.

    python validate_analyste.py

Couvre : Gabriel_Dev_analyste_informatique.py + proposition_code.py +
l'integration du pipeline de correction dans le 8e moteur.
"""
from __future__ import annotations

import importlib.util
import inspect
import os
import shutil
import sys
import tempfile
import traceback
from pathlib import Path

RACINE = Path(__file__).resolve().parent
sys.path.insert(0, str(RACINE))

FICHIERS_TESTS = (
    "tests/test_dev_analyste.py",
    "tests/test_proposition_code.py",
)


class MonkeyPatchShim:
    """Equivalent minimal de pytest.MonkeyPatch (environnement seulement)."""

    def __init__(self) -> None:
        self._memoire: dict[str, str | None] = {}

    def setenv(self, cle: str, valeur: str) -> None:
        if cle not in self._memoire:
            self._memoire[cle] = os.environ.get(cle)
        os.environ[cle] = valeur

    def delenv(self, cle: str) -> None:
        if cle not in self._memoire:
            self._memoire[cle] = os.environ.get(cle)
        os.environ.pop(cle, None)

    def undo(self) -> None:
        for cle, ancien in self._memoire.items():
            if ancien is None:
                os.environ.pop(cle, None)
            else:
                os.environ[cle] = ancien
        self._memoire.clear()


def _charger_module(chemin: Path, nom: str):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    assert spec and spec.loader, f"impossible de charger {chemin}"
    module = importlib.util.module_from_spec(spec)
    sys.modules[nom] = module
    spec.loader.exec_module(module)
    return module


def _lancer(fichier: Path) -> tuple[int, list[tuple[str, str]]]:
    module = _charger_module(fichier, f"_validate_{fichier.stem}")
    tests = [
        (nom, obj) for nom, obj in vars(module).items()
        if nom.startswith("test_") and callable(obj)
    ]
    reussis = 0
    echecs: list[tuple[str, str]] = []
    for nom, func in tests:
        params = inspect.signature(func).parameters
        kwargs = {}
        tmpdir = None
        patch = None
        if "tmp_path" in params:
            tmpdir = Path(tempfile.mkdtemp(prefix="gabriel_val_"))
            kwargs["tmp_path"] = tmpdir
        if "monkeypatch" in params:
            patch = MonkeyPatchShim()
            kwargs["monkeypatch"] = patch
        try:
            func(**kwargs)
            reussis += 1
            print(f"  OK   {nom}")
        except Exception:
            echecs.append((nom, traceback.format_exc()))
            print(f"  ECHEC {nom}")
        finally:
            if patch is not None:
                patch.undo()
            if tmpdir is not None:
                shutil.rmtree(tmpdir, ignore_errors=True)
    return reussis, echecs

def main() -> int:
    print("=" * 72)
    print("Validation Phase 3 — analyste informatique + proposition de code")
    print("=" * 72)
    total_ok = 0
    tous_echecs: list[tuple[str, str]] = []
    for rel in FICHIERS_TESTS:
        fichier = RACINE / rel
        if not fichier.is_file():
            print(f"  ABSENT {rel}")
            tous_echecs.append((rel, "fichier de tests absent"))
            continue
        print(f"\n{rel}")
        ok, echecs = _lancer(fichier)
        total_ok += ok
        tous_echecs.extend((f"{rel}::{n}", t) for n, t in echecs)

    print("\nIntegration")
    ok_int, echecs_int = _verifier_integration()
    total_ok += ok_int
    tous_echecs.extend(echecs_int)

    print("\n8e moteur (pipeline de correction integre)")
    ok_m8, echecs_m8 = _verifier_moteur8()
    total_ok += ok_m8
    tous_echecs.extend(echecs_m8)

    print("\n" + "-" * 72)
    print(f"Reussis : {total_ok}   Echecs : {len(tous_echecs)}")
    for nom, texte in tous_echecs:
        print(f"\n### {nom}\n{texte}")
    print("-" * 72)
    print("RESULTAT :", "OK" if not tous_echecs else "ECHEC")
    return 0 if not tous_echecs else 1


def _verifier_integration() -> tuple[int, list[tuple[str, str]]]:
    """Le 8e moteur pilote le pipeline de correction et le hook CLI existe."""
    import ast

    checks: list[tuple[str, bool]] = []

    texte = (RACINE / "src/multiloop/raisonnement_recursif/__init__.py").read_text(
        encoding="utf-8"
    )
    checks.append(("__init__ exporte proposer_amelioration",
                   "proposer_amelioration" in texte))

    cli = (RACINE / "src/ui/cli.py").read_text(encoding="utf-8")
    checks.append(("hook CLI post-8e-moteur present",
                   "proposer_amelioration as _proposer" in cli))
    checks.append(("hook CLI reference le kill-switch", "GABRIEL_DEV_ANALYSTE" in cli))

    moteur = (RACINE / "src/multiloop/raisonnement_recursif"
              "/engine_recursif_background.py").read_text(encoding="utf-8")
    checks.append(("8e moteur importe detecter_manque", "detecter_manque" in moteur))
    checks.append(("8e moteur tente le raisonnement recursif",
                   "_tenter_raisonnement" in moteur))
    checks.append(("Resultat porte diagnostic_manque", "diagnostic_manque" in moteur))
    checks.append(("Resultat porte rapport_correction", "rapport_correction" in moteur))

    for rel in (
        "Gabriel_Dev_analyste_informatique.py",
        "src/multiloop/raisonnement_recursif/proposition_code.py",
        "src/multiloop/raisonnement_recursif/engine_recursif_background.py",
        "src/multiloop/raisonnement_recursif/__init__.py",
        "src/ui/cli.py",
        "tests/test_dev_analyste.py",
        "tests/test_proposition_code.py",
    ):
        try:
            ast.parse((RACINE / rel).read_text(encoding="utf-8"), filename=rel)
            checks.append((f"AST {rel}", True))
        except SyntaxError as exc:
            checks.append((f"AST {rel} : {exc}", False))

    # Bout-en-bout : analyse du depot, contrats valides, depot vivant intact.
    gab = _charger_module(
        RACINE / "Gabriel_Dev_analyste_informatique.py", "_gabriel_validate_e2e"
    )
    banque = gab.BanqueAnalyste(":memory:")
    banque.amorcer()
    cible = RACINE / "Gabriel_Dev_analyste_informatique.py"
    avant = cible.read_bytes()
    rapport = gab.analyser(
        "documentation tests architecture du depot", banque=banque,
        plafond=8, journal=False,
    )
    checks.append(("analyse sans erreur", not rapport["erreurs"]))
    checks.append(("propositions emises", len(rapport["propositions"]) > 0))
    checks.append(("contrats au format variateur",
                   all(p["contrat"] is None or set(p["contrat"]) == {"meta", "operations"}
                       for p in rapport["propositions"])))
    checks.append(("simulations sans echec",
                   sum(s.get("echouees", 0) for s in rapport["simulations"]) == 0))
    checks.append(("depot vivant intact", cible.read_bytes() == avant))
    banque.fermer()

    ok = 0
    echecs: list[tuple[str, str]] = []
    for libelle, passe in checks:
        if passe:
            ok += 1
            print(f"  OK   {libelle}")
        else:
            echecs.append((libelle, "assertion echouee"))
            print(f"  ECHEC {libelle}")
    return ok, echecs



def _charger_paquet_raisonnement():
    """Charge le paquet raisonnement_recursif SANS src/multiloop/__init__.

    Ce paquet-pere importe httpx (absent ici) : on cree donc un paquet
    synthetique dont le __path__ pointe sur le vrai dossier, ce qui rend les
    imports relatifs fonctionnels sans declencher la chaine lourde.
    """
    import types
    dossier = RACINE / "src" / "multiloop" / "raisonnement_recursif"
    nom = "_gabriel_rr_val"
    if nom in sys.modules:
        return sys.modules[nom]
    paquet = types.ModuleType(nom)
    paquet.__path__ = [str(dossier)]
    sys.modules[nom] = paquet
    return paquet


def _importer_sous_module(nom: str):
    paquet = _charger_paquet_raisonnement()
    complet = f"_gabriel_rr_val.{nom}"
    if complet in sys.modules:
        return sys.modules[complet]
    chemin = RACINE / "src/multiloop/raisonnement_recursif" / f"{nom}.py"
    spec = importlib.util.spec_from_file_location(complet, chemin)
    module = importlib.util.module_from_spec(spec)
    sys.modules[complet] = module
    setattr(paquet, nom, module)
    spec.loader.exec_module(module)
    return module


def _verifier_moteur8() -> tuple[int, list[tuple[str, str]]]:
    """Le 8e moteur pilote maintenant le pipeline de correction."""
    checks: list[tuple[str, bool]] = []
    recolte: dict[str, object] = {}

    ancien = os.environ.get("GABRIEL_RECURSIVE")
    try:
        os.environ.pop("GABRIEL_RECURSIVE", None)
        engine = _importer_sous_module("engine_recursif_background")
        dossier = Path(tempfile.mkdtemp(prefix="gabriel_m8_"))
        moteur = engine.MoteurRecursifBackground(
            archiveur=engine.ArchiveurTimeline(dossier / "tl.db"),
        )
        res = moteur.traiter(
            "Comment reconstruire le 137ieme nombre premier avec le rapport 1/2 ?",
            reponse=None,
        )
        recolte["desactive"] = res
        checks.append(("8e moteur tourne", res.declenche is True))
        checks.append(("diagnostic de manque renseigne",
                       res.diagnostic_manque is not None
                       and res.diagnostic_manque.manque is True))
        checks.append(("rapport de correction : branche kill-switch",
                       isinstance(res.rapport_correction, dict)
                       and "desactive" in str(res.rapport_correction.get("etat"))))
        checks.append(("to_dict serialisable",
                       "diagnostic_manque" in res.to_dict()
                       and "rapport_correction" in res.to_dict()))

        # Branche active : la boucle d'auto-programmation sandboxee tourne.
        os.environ["GABRIEL_RECURSIVE"] = "1"
        os.environ.pop("GABRIEL_RECURSIVE_APPLY", None)
        moteur2 = engine.MoteurRecursifBackground(
            archiveur=engine.ArchiveurTimeline(dossier / "tl2.db"),
        )
        res2 = moteur2.traiter("demonstration par l'absurde de l'exclusivite ?")
        recolte["active"] = res2
        rc = res2.rapport_correction or {}
        checks.append(("boucle recursive declenchee",
                       str(rc.get("etat", "")).startswith("applique")))
        rapport = rc.get("rapport") or {}
        checks.append(("application en dry-run (depot intact)",
                       rapport.get("dry_run") is True))
        checks.append(("aucun echec d'application",
                       int(rapport.get("echouees", -1)) == 0))

        # Chaîne complète : blocage -> proposition d'amélioration du dépôt.
        pc = _importer_sous_module("proposition_code")
        cible = RACINE / "Gabriel_Dev_analyste_informatique.py"
        avant = cible.read_bytes()
        devenir = pc.proposer_amelioration(
            "exclusivite des nombres premiers", res2, plafond=3,
        )
        checks.append(("blocage -> proposition de code", devenir.declenche is True))
        checks.append(("propositions emises apres blocage",
                       len(devenir.propositions) > 0))
        checks.append(("message en francais non vide", bool(devenir.message)))
        checks.append(("depot vivant intact apres proposition",
                       cible.read_bytes() == avant))
        checks.append(("simulations de la proposition en dry-run",
                       all(s.get("dry_run", True) is True
                           for s in devenir.simulations)))

        shutil.rmtree(dossier, ignore_errors=True)
    except Exception:
        checks.append(("execution du 8e moteur", False))
        recolte["traceback"] = traceback.format_exc()
    finally:
        if ancien is None:
            os.environ.pop("GABRIEL_RECURSIVE", None)
        else:
            os.environ["GABRIEL_RECURSIVE"] = ancien

    ok = 0
    echecs: list[tuple[str, str]] = []
    for libelle, passe in checks:
        if passe:
            ok += 1
            print(f"  OK   {libelle}")
        else:
            detail = str(recolte.get("traceback") or "assertion echouee")
            echecs.append((f"moteur8 :: {libelle}", detail))
            print(f"  ECHEC {libelle}")
    return ok, echecs


if __name__ == "__main__":
    raise SystemExit(main())

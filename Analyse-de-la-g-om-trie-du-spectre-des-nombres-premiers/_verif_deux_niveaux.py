#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verification du contrat cognitif a deux niveaux (rapports 1/2 et 1/k)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "agent-multiloop-Gabriel-local"))

# Console Windows cp1252 : forcer UTF-8 pour les sorties du module.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # pragma: no cover
    pass

OUT = ROOT / "_verif_deux_niveaux.txt"
buf: list[str] = []


def log(*args: object) -> None:
    buf.append(" ".join(str(a) for a in args))


from src.core.spectral_core import SpectralMethodCore  # noqa: E402
from src.core.pipeline import Pipeline  # noqa: E402
from src.multiloop.refinement_loop import RefinementLoop  # noqa: E402
from src.engines.generalization.generalizer import Generalizer  # noqa: E402
from src.spectral import rapports_non_typiques as rnt  # noqa: E402

core = SpectralMethodCore()

log("#" * 90)
log("# A. RAPPORTS NON TYPIQUES 1/k<>1/2 — criteres obligatoires a deux niveaux")
log("#" * 90)

for k, n in ((5, 10), (13, 10), (81, 10), (79, 17), (50, 16), (27, 19)):
    log("")
    log("=" * 90)
    log(f"  RAPPORT 1/{k}  n={n}")
    log("=" * 90)
    r = core.rapport_convolutif_non_typique(f"1/{k}", n)

    log(f"  ancrage_niveau_1 = {r.get('ancrage_niveau_1')}")
    log(f"  ancrage_niveau_2 = {r.get('ancrage_niveau_2')}")
    log(f"  ancrage_retourne = {r.get('ancrage_retourne')}  (aucun_ancrage={r.get('aucun_ancrage')})")

    n1 = r.get("niveau_1") or {}
    log(f"  --- NIVEAU 1 (entier) : {n1.get('termes')}")
    for p in n1.get("possibilites", []):
        log(f"      {p['branche']:10s} Digamma={p['digamma']:<22} "
            f"C={str(p['C']):<24} {p['verdict']}")

    n2 = r.get("niveau_2") or {}
    log(f"  --- NIVEAU 2 (geometrique) : facteur_g={n2.get('facteur_g')}")
    for b in n2.get("branches_reelles", []):
        log(f"      {b['branche']:14s} C={str(b['C']):<24} {b['verdict']}")
    rpr = n2.get("reconstruction_par_rang") or {}
    log(f"      rang: base={rpr.get('premier_base')}@{rpr.get('rang_base')} -> "
        f"cible={rpr.get('premier_cible')}@{rpr.get('rang_cible')} verifie={rpr.get('verifie')}")

    log("  --- POINTS OBLIGATOIRES ---")
    log(f"  {r.get('point_1_niveau_1')}")
    log(f"  {r.get('point_2_niveau_2')}")
    log(f"  {r.get('point_3_verdict')}")

log("")
log("#" * 90)
log("# B. RAPPORT TYPIQUE 1/2 — les memes criteres doivent etre presents")
log("#" * 90)
for n in (10, 27):
    log("")
    log(f"  --- 1/2, n={n} ---")
    t = core.rapport_convolutif_typique(n)
    log(f"  ancrage_niveau_1={t.get('ancrage_niveau_1')} "
        f"ancrage_niveau_2={t.get('ancrage_niveau_2')} "
        f"ancrage_retourne={t.get('ancrage_retourne')}")
    for p in (t.get("niveau_1") or {}).get("possibilites", []):
        log(f"      {p['branche']:10s} C={str(p['C']):<24} {p['verdict']}")
    log(f"  {t.get('point_1_niveau_1')}")
    log(f"  {t.get('point_2_niveau_2')}")
    log(f"  {t.get('point_3_verdict')}")

log("")
log("#" * 90)
log("# C. INTEGRATION PIPELINE : resume deterministe + prompt")
log("#" * 90)

facts = core.rapport_convolutif_non_typique("1/81", 10)
facts["model"] = "1/81"
facts["equation_holds"] = False
resume = Pipeline._append_convolution_summary("Reponse.", facts)
log("")
log("--- resume deterministe (1/81) ---")
log(resume)
log("")
log("  Contient '### Criteres convolutifs obligatoires' :",
    "### Critères convolutifs obligatoires" in resume)
log("  Contient 'Niveau 1' :", "Niveau 1" in resume)
log("  Contient 'Niveau 2' :", "Niveau 2" in resume)
log("  Contient 'aucun ancrage' :", "aucun ancrage" in resume.lower())


class Ctx:
    metadata: dict = {}
    raw_question = "Reconstruire le rapport 1/81 pour n=10"


general = Generalizer().generalize(facts, {"intent": "reconstruction", "model": "1/81"})
prompt = Pipeline._build_base_prompt(
    Pipeline.__new__(Pipeline), Ctx(), {"model": "1/81"}, general, [], facts
)
rendered = RefinementLoop._build_prompt(
    RefinementLoop.__new__(RefinementLoop), Ctx(), facts, prompt, "", 1
)
log("")
log("--- prompt : presence des criteres ---")
log("  'CRITÈRES CONVOLUTIFS OBLIGATOIRES' dans prompt :",
    "CRITÈRES CONVOLUTIFS OBLIGATOIRES" in prompt)
log("  'point_1_niveau_1' dans prompt :", "point_1_niveau_1" in prompt)
log("  'point_2_niveau_2' dans prompt :", "point_2_niveau_2" in prompt)
log("  'point_3_verdict' dans prompt :", "point_3_verdict" in prompt)
log("  'niveau_2' cle transmise dans CHIFFRES CALCULES :", '"niveau_2"' in rendered)

log("")
log("#" * 90)
log("# D. TOTAL DES TESTS INTERNES DU MODULE")
log("#" * 90)
log("  verifier_exemples() :", rnt.verifier_exemples())

OUT.write_text("\n".join(buf), encoding="utf-8")
print("Verification ecrite :", OUT)
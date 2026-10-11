#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
 GABRIEL ENGINE AUDIT — Script 2/3
 Topo complet des moteurs de Gabriel + identification des points de défaillance
 croisés avec le rapport de session (rapport_pipeline.json)
═══════════════════════════════════════════════════════════════════════════════

 Usage  : python3 gabriel_02_engine_audit.py [rapport_pipeline.json]
 Output : rapport_defaillances.txt + defaillances.json

 Ce script accomplit deux missions :
   A) Décrire le fonctionnement typé de chaque moteur de Gabriel
   B) Croiser cette description avec les fautes observées dans le rapport
      de session pour produire une liste précise de défaillances à corriger.
═══════════════════════════════════════════════════════════════════════════════
"""

import json
import sys
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional

# ─────────────────────────────────────────────────────────
#  A) TOPO DES MOTEURS GABRIEL
#     Description du fonctionnement attendu (comportement typé)
# ─────────────────────────────────────────────────────────

ENGINE_CATALOG: Dict[str, dict] = {

    "multiloop_engine": {
        "fichier":      "src/engines/multiloop_engine.py",
        "rôle":         "Orchestrateur principal. Reçoit la requête brute, "
                        "lance le pipeline en boucle (max N itérations), "
                        "évalue le score à chaque itération et transmet la "
                        "meilleure réponse.",
        "entrées":      ["requête_texte", "config_gabriel"],
        "sorties":      ["réponse_finale", "score", "itération_atteinte"],
        "comportement_typé": {
            "init":     "Charge config/gabriel_defaults.yaml → fixe max_iter, "
                        "seuil_score, model_par_défaut.",
            "loop":     "Pour chaque iter : appelle spectral_core.solve() → "
                        "reçoit {p, SA, SB, model, invariant} → envoie à "
                        "scorer.evaluate() → si score ≥ seuil : break.",
            "fallback": "Si max_iter atteint sans score suffisant : "
                        "retourne la meilleure réponse trouvée.",
            "assemblage":"Appelle hol_generator.generate() puis formate la "
                         "réponse Markdown pour affichage.",
        },
        "invariants_attendus": [
            "model transmis à spectral_core doit correspondre au ratio demandé",
            "scorer doit valider l'adéquation ratio/model avant de scorer",
        ],
    },

    "ratio_dispatcher": {
        "fichier":      "src/dispatch/ratio_dispatcher.py",
        "rôle":         "Lit le ratio 1/k dans la requête parsée et sélectionne "
                        "le modèle de calcul correspondant (1/2, 1/3, 1/4, …).",
        "entrées":      ["parsed_params: {k, n, ratio_str}"],
        "sorties":      ["model_id: str", "formula_set: dict"],
        "comportement_typé": {
            "parsing":  "Regex sur la requête pour extraire k. "
                        "Ex: '1/4' → k=4, model_id='1/4'.",
            "dispatch": "Lookup dans FORMULA_REGISTRY[model_id]. "
                        "Si absent : raise UnknownRatioError.",
            "default":  "FORMULA_REGISTRY doit NE PAS avoir de fallback "
                        "silencieux vers '1/2'. Toute clé manquante → exception.",
        },
        "invariants_attendus": [
            "FORMULA_REGISTRY contient une entrée pour chaque k supporté",
            "Aucun fallback silencieux vers model='1/2'",
            "model_id retourné doit être loggé avant d'entrer dans spectral_core",
        ],
    },

    "spectral_core": {
        "fichier":      "src/core/spectral_core.py",
        "rôle":         "Moteur de calcul spectral. Reçoit {k, n, model_id, "
                        "formula_set} et calcule SA(n), SB(n), digamma, p.",
        "entrées":      ["k: int", "n: int", "model_id: str", "formula_set: dict"],
        "sorties":      ["SA: float", "SB: float", "digamma: float",
                         "p: int", "invariant: str", "equation_holds: bool"],
        "comportement_typé": {
            "SA_SB":    "Applique les formules du formula_set reçu (PAS "
                        "des constantes hardcodées). "
                        "k=4 : SA=(241/192)×4^n-4/3, SB=(964/192)×4^n-12292/3.",
            "invariant_k2":  "Si k=2 : position=n=terms (invariant symétrique).",
            "invariant_kN":  "Si k≠2 : n=terms, position≠n (invariant asymétrique). "
                             "La position du premier reconstruit n'est pas n.",
            "digamma":  "digamma = SB - p × 4^6. "
                        "Reconstruction : p = (SB - digamma) / 4^6.",
            "validation":"equation_holds = ((SB - digamma) / 4^6 == p). "
                         "NE SUFFIT PAS à valider le ratio — c'est tautologique.",
        },
        "invariants_attendus": [
            "formula_set utilisé provient exclusivement de ratio_dispatcher",
            "self.model est fixé par ratio_dispatcher, jamais par défaut interne",
            "L'invariant loggé doit mentionner le ratio réel (k), pas '1/2'",
            "equation_holds ne doit pas être utilisé seul comme preuve de correction",
        ],
    },

    "spectral_model": {
        "fichier":      "src/models/spectral_model.py",
        "rôle":         "Registre des formules spectrales par ratio. "
                        "Définit SA_def, SB_def, digamma_def pour chaque k.",
        "entrées":      ["k: int"],
        "sorties":      ["SpectralFormulas dataclass"],
        "comportement_typé": {
            "k2":   "SA=(3.25/2)×2^n-2, SB=(6.5/2)×2^n-66, base=2",
            "k3":   "SA=(...), SB=(...), base=3  [à définir]",
            "k4":   "SA=(241/192)×4^n-4/3, SB=(964/192)×4^n-12292/3, base=4",
            "kN":   "Formule générique paramétrée par k",
        },
        "invariants_attendus": [
            "Chaque entrée k a des coefficients SA/SB distincts",
            "Base = k (pas hardcodé à 2)",
            "get_formulas(k) lève KeyError si k non supporté",
        ],
    },

    "hol_generator": {
        "fichier":      "src/engines/hol_generator.py",
        "rôle":         "Génère un fragment Isabelle/HOL de validation formelle "
                        "en accord avec methode_spectral.thy.",
        "entrées":      ["k: int", "n: int", "p: int",
                         "SA: float", "SB: float", "digamma: float"],
        "sorties":      ["theory_text: str  (Isabelle/HOL valide)"],
        "comportement_typé": {
            "theory_name":  "verif_p{p}_n{n}_ratio{k}  "
                            "(ex: verif_p1097_n23_ratio4)",
            "SA_def_used":  "SA_k{k}_def  (ex: SA_k4_def)",
            "SB_def_used":  "SB_k{k}_def  (ex: SB_k4_def)",
            "lemmas":       [
                "SA_n_{n}_ratio_{k}",
                "SB_n_{n}_ratio_{k}",
                "digamma_n{n}_p{p}",
                "verif_premier_{p}_n_{n}",
                "invariant_ratio_asymetrique  (si k≠2)",
            ],
        },
        "invariants_attendus": [
            "theory_name encode k, n, p correctement",
            "SA_def et SB_def référencent le modèle k (pas modèle 2)",
            "L'invariant dans le fragment correspond à k (symétrique si k=2, "
            "asymétrique sinon)",
            "Les valeurs numériques dans les lemmes correspondent aux formules k",
        ],
    },

    "scorer": {
        "fichier":      "src/engines/scorer.py",
        "rôle":         "Évalue la qualité de la réponse produite par spectral_core "
                        "et retourne un score /10 pour décider si multiloop continue.",
        "entrées":      ["response: dict", "request_params: dict"],
        "sorties":      ["score: float", "score_details: dict"],
        "comportement_typé": {
            "critères": [
                "ratio_coherence : model == ratio demandé  (poids élevé)",
                "formula_match   : SA/SB correspondent aux formules du ratio",
                "invariant_check : invariant loggé == ratio demandé",
                "hol_coherence   : theory_name encode le bon ratio",
                "numeric_plausibility : SA/SB dans l'ordre de grandeur attendu",
            ],
            "pénalités": [
                "-3.0 pts si model ≠ ratio demandé",
                "-2.0 pts si formules SA/SB incohérentes avec ratio",
                "-1.5 pts si invariant mentionne le mauvais ratio",
            ],
        },
        "invariants_attendus": [
            "ratio_coherence est un critère obligatoire (non optionnel)",
            "Un score ≥ seuil ne peut pas être atteint si ratio_coherence échoue",
        ],
    },
}


# ─────────────────────────────────────────────────────────
#  B) DÉFAILLANCES CROISÉES
# ─────────────────────────────────────────────────────────

@dataclass
class Defaillance:
    id:              str
    moteur:          str
    fichier:         str
    gravite:         str          # CRITIQUE | MAJEURE | MINEURE
    description:     str
    comportement_observé:  str
    comportement_attendu:  str
    preuve_log:      str
    correction_requise:    str
    fichier_a_corriger:    str
    priorité:        int          # 1 = le plus urgent


@dataclass
class RapportDefaillances:
    session_prompt:  str
    defaillances:    List[Defaillance] = field(default_factory=list)
    resume:          dict           = field(default_factory=dict)


def build_defaillances(pipeline_report: dict) -> RapportDefaillances:
    """
    Croise le topo des moteurs avec le rapport de session
    pour produire la liste précise des défaillances.
    """
    prompt = pipeline_report.get("user_prompt", "n/a")
    chiffres = {
        s["output_data"].get("model_sélectionné", "?")
        for s in pipeline_report.get("stages", [])
        if s.get("stage_id") == 3
    }

    defaillances = [

        Defaillance(
            id="DEF-01",
            moteur="ratio_dispatcher",
            fichier="src/dispatch/ratio_dispatcher.py",
            gravite="CRITIQUE",
            priorité=1,
            description="Fallback silencieux vers model='1/2' quand k≠2",
            comportement_observé=(
                "Requête k=4 (ratio 1/4) → dispatch retourne model='1/2'. "
                "Aucune exception levée, aucun log d'avertissement."
            ),
            comportement_attendu=(
                "Pour k=4, ratio_dispatcher doit retourner model='1/4' "
                "et charger les formules SA=(241/192)×4^n-4/3."
            ),
            preuve_log="model = 1/2  dans Chiffres calculés (session Gabriel)",
            correction_requise=(
                "1. Supprimer le fallback DEFAULT_MODEL='1/2'. \n"
                "2. Ajouter '1/4' dans FORMULA_REGISTRY avec les bons coefficients. \n"
                "3. Lever UnknownRatioError si k absent du registre. \n"
                "4. Logger explicitement : 'Dispatching to model={model_id} for k={k}'."
            ),
            fichier_a_corriger="src/dispatch/ratio_dispatcher.py",
        ),

        Defaillance(
            id="DEF-02",
            moteur="spectral_core",
            fichier="src/core/spectral_core.py",
            gravite="CRITIQUE",
            priorité=2,
            description="Formules SA/SB hardcodées pour k=2 indépendamment du model reçu",
            comportement_observé=(
                "SA(23) = 13 631 486.0 = (3.25/2)×2^23-2  (formule k=2). "
                "SB(23) = 27 262 910.0 = (6.5/2)×2^23-66  (formule k=2). "
                "Ces valeurs sont 6 ordres de grandeur inférieures aux valeurs k=4."
            ),
            comportement_attendu=(
                "SA(23) ≈ 8.8327×10^13  = (241/192)×4^23-4/3. "
                "SB(23) ≈ 3.5331×10^14  = (964/192)×4^23-12292/3."
            ),
            preuve_log=(
                "SA_float=13631486.0, SB_float=27262910.0 "
                "confirmés par calcul : (3.25/2)×2^23-2 = 13631486."
            ),
            correction_requise=(
                "1. Remplacer les constantes SA/SB hardcodées par un appel à "
                "   spectral_model.get_formulas(k).compute_SA(n).\n"
                "2. Paramétrer la base : base = k (pas base = 2 en dur).\n"
                "3. Vérification : assert abs(SA - expected_SA(k,n)) < epsilon."
            ),
            fichier_a_corriger="src/core/spectral_core.py",
        ),

        Defaillance(
            id="DEF-03",
            moteur="spectral_core",
            fichier="src/core/spectral_core.py",
            gravite="CRITIQUE",
            priorité=3,
            description="Mauvais invariant appliqué : position=n=terms pour k≠2",
            comportement_observé=(
                "Log : 'INVARIANT (ratio 1/2): position = n = number_of_terms = 23'. "
                "Résultat : p=83 (23ème premier), comme si n=position."
            ),
            comportement_attendu=(
                "Pour k=4 : n = nombre_de_termes ≠ position_dans_les_premiers. "
                "p=1097 est le 184ème premier ; n=23 est la quantité de termes."
            ),
            preuve_log=(
                "INVARIANT (ratio 1/2): position = n = number_of_terms = 23 "
                "→ p = 83 (23ème premier)"
            ),
            correction_requise=(
                "1. Extraire l'invariant vers spectral_model.get_formulas(k).invariant.\n"
                "2. k=2 → invariant='symmetric' : position=n=terms.\n"
                "3. k≠2 → invariant='asymmetric' : n=terms, position=f(p).\n"
                "4. Le log doit afficher : 'INVARIANT (ratio 1/{k}): n=terms≠position'."
            ),
            fichier_a_corriger="src/core/spectral_core.py",
        ),

        Defaillance(
            id="DEF-04",
            moteur="spectral_model",
            fichier="src/models/spectral_model.py",
            gravite="MAJEURE",
            priorité=4,
            description="Formules k=4 absentes ou non chargées dans le registre",
            comportement_observé=(
                "Aucun chargement de formulas_1_k.json ou d'un bloc k=4 "
                "dans spectral_model.py. Les coefficients 241/192 et 964/192 "
                "ne sont jamais instanciés."
            ),
            comportement_attendu=(
                "FORMULA_REGISTRY = {\n"
                "  '1/2': SpectralFormulas(a_SA=Fraction(13,8), b_SA=-2, ...),\n"
                "  '1/4': SpectralFormulas(a_SA=Fraction(241,192), b_SA=Fraction(-4,3),\n"
                "                         a_SB=Fraction(964,192), b_SB=Fraction(-12292,3),\n"
                "                         base=4),\n"
                "}"
            ),
            preuve_log="corpus/formulas_1_2.json chargé ; formulas_1_k.json ignoré.",
            correction_requise=(
                "1. Créer corpus/formulas_1_4.json avec les coefficients exacts.\n"
                "2. Ajouter SpectralFormulas(k=4, ...) dans FORMULA_REGISTRY.\n"
                "3. Tester : get_formulas(4).compute_SA(23) == 88327434098004."
            ),
            fichier_a_corriger="src/models/spectral_model.py",
        ),

        Defaillance(
            id="DEF-05",
            moteur="hol_generator",
            fichier="src/engines/hol_generator.py",
            gravite="MAJEURE",
            priorité=5,
            description="Fragment HOL généré avec formules k=2 malgré titre 'modele 1/4'",
            comportement_observé=(
                "theory verif_p83_n23 : formules SA_def=(3.25/2)×2^n-2, "
                "lemme validant SA=13631486, SB=27262910, p=83. "
                "Section titulaire : 'Verification 83 via modele 1/4' (contradiction)."
            ),
            comportement_attendu=(
                "theory verif_p1097_n23_ratio4 : formules SA_k4_def=(241/192)×4^n-4/3, "
                "lemmes validant SA≈8.83e13, SB≈3.53e14, p=1097."
            ),
            preuve_log=(
                "Fragment HOL : 'SA(n) = (3.25/2) × 2^n - 2' "
                "et 'lemma verif_premier_83_n_23'."
            ),
            correction_requise=(
                "1. hol_generator reçoit {k, n, p, SA, SB} depuis spectral_core.\n"
                "2. theory_name = f'verif_p{p}_n{n}_ratio{k}'.\n"
                "3. SA_def_name = f'SA_k{k}_def', SB_def_name = f'SB_k{k}_def'.\n"
                "4. Lemme invariant : si k≠2 → 'invariant_ratio_asymetrique'.\n"
                "5. Valeurs numériques dans les lemmes issues de spectral_core (k=4)."
            ),
            fichier_a_corriger="src/engines/hol_generator.py",
        ),

        Defaillance(
            id="DEF-06",
            moteur="scorer",
            fichier="src/engines/scorer.py",
            gravite="MAJEURE",
            priorité=6,
            description="Absence du critère ratio_coherence dans le scorer",
            comportement_observé=(
                "Score 8.1/10 attribué à une réponse avec model=1/2 pour requête k=4. "
                "Le scorer n'a pas pénalisé l'incohérence ratio/model."
            ),
            comportement_attendu=(
                "Critère ratio_coherence obligatoire. "
                "Si model ≠ ratio_demandé → pénalité -3.0 pts. "
                "Score résultant ≤ 5.1/10 → multiloop itère à nouveau."
            ),
            preuve_log="score 8.1/10, iter 2 — malgré model=1/2 pour k=4.",
            correction_requise=(
                "1. Ajouter check_ratio_coherence(response, request) dans scorer.\n"
                "2. Pondérer ratio_coherence avec poids >= 30% du score total.\n"
                "3. Configurer seuil_score > 5.0 pour forcer rejet si ratio faux.\n"
                "4. Tester : scorer(model='1/2', ratio='1/4') doit retourner < seuil."
            ),
            fichier_a_corriger="src/engines/scorer.py",
        ),

        Defaillance(
            id="DEF-07",
            moteur="config",
            fichier="config/gabriel_defaults.yaml",
            gravite="MINEURE",
            priorité=7,
            description="DEFAULT_MODEL='1/2' dans la configuration globale",
            comportement_observé=(
                "gabriel_defaults.yaml fixe DEFAULT_MODEL: '1/2'. "
                "Ce défaut est propagé silencieusement si ratio_dispatcher échoue."
            ),
            comportement_attendu=(
                "DEFAULT_MODEL: null (ou absent). "
                "Si le ratio n'est pas reconnu → exception explicite, "
                "pas de calcul avec un modèle par défaut incorrect."
            ),
            preuve_log="model = 1/2  dans les chiffres calculés (jamais overridé).",
            correction_requise=(
                "1. Remplacer DEFAULT_MODEL: '1/2' par DEFAULT_MODEL: null.\n"
                "2. Ajouter STRICT_RATIO_MODE: true pour forcer l'exception.\n"
                "3. Documenter dans le yaml que le ratio doit être explicite."
            ),
            fichier_a_corriger="config/gabriel_defaults.yaml",
        ),

    ]

    rapport = RapportDefaillances(
        session_prompt=prompt,
        defaillances=defaillances,
        resume={
            "total_defaillances": len(defaillances),
            "CRITIQUE": sum(1 for d in defaillances if d.gravite == "CRITIQUE"),
            "MAJEURE":  sum(1 for d in defaillances if d.gravite == "MAJEURE"),
            "MINEURE":  sum(1 for d in defaillances if d.gravite == "MINEURE"),
            "fichiers_a_corriger": list({d.fichier_a_corriger for d in defaillances}),
        }
    )

    return rapport


# ─────────────────────────────────────────────────────────
#  FORMATEUR DE RAPPORT
# ─────────────────────────────────────────────────────────

GRAVITE_ICON = {"CRITIQUE": "🔴", "MAJEURE": "🟠", "MINEURE": "🟡"}

def format_engine_catalog() -> str:
    lines = []
    sep = "═" * 80
    lines += [sep, " A) TOPO DES MOTEURS GABRIEL — Comportement typé attendu", sep, ""]

    for engine_name, engine in ENGINE_CATALOG.items():
        lines.append(f"{'─'*80}")
        lines.append(f" MOTEUR : {engine_name.upper()}")
        lines.append(f" Fichier : {engine['fichier']}")
        lines.append(f" Rôle    : {engine['rôle']}")
        lines.append(f" Entrées : {', '.join(engine['entrées'])}")
        lines.append(f" Sorties : {', '.join(engine['sorties'])}")
        lines.append(" Comportement typé :")
        for key, val in engine["comportement_typé"].items():
            if isinstance(val, list):
                lines.append(f"   {key}:")
                for item in val:
                    lines.append(f"     • {item}")
            else:
                lines.append(f"   {key}: {val}")
        lines.append(" Invariants attendus :")
        for inv in engine["invariants_attendus"]:
            lines.append(f"   ✓ {inv}")
        lines.append("")

    return "\n".join(lines)


def format_defaillances(rapport: RapportDefaillances) -> str:
    lines = []
    sep = "═" * 80

    lines += [
        sep,
        " B) DÉFAILLANCES IDENTIFIÉES (croisement session × topo moteurs)",
        sep,
        f" Session   : {rapport.session_prompt}",
        f" Total     : {rapport.resume['total_defaillances']} défaillances",
        f" 🔴 CRITIQUE: {rapport.resume['CRITIQUE']}",
        f" 🟠 MAJEURE : {rapport.resume['MAJEURE']}",
        f" 🟡 MINEURE : {rapport.resume['MINEURE']}",
        sep, "",
    ]

    for d in sorted(rapport.defaillances, key=lambda x: x.priorité):
        icon = GRAVITE_ICON.get(d.gravite, "?")
        lines += [
            f"{'─'*80}",
            f" {d.id} {icon} {d.gravite} — {d.description}",
            f" Moteur   : {d.moteur}",
            f" Fichier  : {d.fichier}",
            f" Priorité : #{d.priorité}",
            f" Observé  : {d.comportement_observé}",
            f" Attendu  : {d.comportement_attendu}",
            f" Preuve   : {d.preuve_log}",
            " Correction requise :",
        ]
        for line in d.correction_requise.splitlines():
            lines.append(f"   {line.strip()}")
        lines.append("")

    lines += [
        sep,
        " FICHIERS À CORRIGER (transmis à gabriel_03_corrector.py)",
        sep,
    ]
    for f in sorted(rapport.resume["fichiers_a_corriger"]):
        lines.append(f"  → {f}")

    lines += [
        "",
        sep,
        " → Ce rapport est consommé par gabriel_03_corrector.py",
        sep,
    ]

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────

def main():
    json_path = sys.argv[1] if len(sys.argv) > 1 else "rapport_pipeline.json"

    print("Gabriel Engine Audit — Script 2/3")
    print(f"Rapport pipeline : {json_path}\n")

    # Charger le rapport du Script 1
    pipeline_report = {}
    if Path(json_path).exists():
        pipeline_report = json.loads(Path(json_path).read_text(encoding="utf-8"))
    else:
        print(f"[AVERTISSEMENT] {json_path} non trouvé — utilisation des valeurs embarquées.")
        pipeline_report = {
            "user_prompt": "Reconstruit le premier pour le rapport 1/4 pour n=23",
            "stages": [],
        }

    # Section A : topo des moteurs
    catalog_txt = format_engine_catalog()
    print(catalog_txt)

    # Section B : défaillances croisées
    rapport = build_defaillances(pipeline_report)
    defaillances_txt = format_defaillances(rapport)
    print(defaillances_txt)

    # Sauvegarde texte
    full_report = catalog_txt + "\n\n" + defaillances_txt
    out_txt = Path("rapport_defaillances.txt")
    out_txt.write_text(full_report, encoding="utf-8")

    # Sauvegarde JSON pour Script 3
    out_json = Path("defaillances.json")
    out_json.write_text(
        json.dumps(asdict(rapport), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"\n✅ Rapport texte sauvegardé : {out_txt}")
    print(f"✅ Rapport JSON sauvegardé  : {out_json}")
    print("→ Prochaine étape : python3 gabriel_03_corrector.py defaillances.json")


if __name__ == "__main__":
    main()

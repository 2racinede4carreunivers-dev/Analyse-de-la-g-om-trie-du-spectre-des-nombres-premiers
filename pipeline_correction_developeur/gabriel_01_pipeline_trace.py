#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
 GABRIEL PIPELINE TRACE — Script 1/3
 Reconstruction complète du pipeline soumission → réponse
 Session : "Reconstruit le premier pour le rapport 1/4 pour n=23"
═══════════════════════════════════════════════════════════════════════════════

 Usage  : python3 gabriel_01_pipeline_trace.py [chemin_log]
 Output : rapport_pipeline.txt  (dans le répertoire courant)

 FICHIERS GABRIEL IMPLIQUÉS (adresses dépôt présumées) :
   src/core/spectral_core.py          ← moteur de calcul principal
   src/engines/multiloop_engine.py    ← orchestrateur d'itérations
   src/engines/hol_generator.py       ← générateur de fragments Isabelle/HOL
   src/engines/scorer.py              ← évaluateur score/10
   src/models/spectral_model.py       ← définitions SA/SB/digamma par ratio
   src/dispatch/ratio_dispatcher.py   ← aiguillage par rapport 1/k (FAUTIF)
   corpus/methode_spectral.thy        ← source de vérité HOL
   corpus/formulas_1_2.json           ← formules hardcodées ratio 1/2 (FAUTIF)
   corpus/formulas_1_k.json           ← formules génériques (non chargé)
   config/gabriel_defaults.yaml       ← defaults dont model="1/2" (FAUTIF)
═══════════════════════════════════════════════════════════════════════════════
"""

import re
import sys
import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import List, Optional

# ─────────────────────────────────────────────────────────
#  CONSTANTES — adresses fichiers dans le dépôt Gabriel
# ─────────────────────────────────────────────────────────
REPO_FILES = {
    "spectral_core":    "src/core/spectral_core.py",
    "multiloop_engine": "src/engines/multiloop_engine.py",
    "hol_generator":    "src/engines/hol_generator.py",
    "scorer":           "src/engines/scorer.py",
    "spectral_model":   "src/models/spectral_model.py",
    "ratio_dispatcher": "src/dispatch/ratio_dispatcher.py",
    "thy_corpus":       "corpus/methode_spectral.thy",
    "formulas_1_2":     "corpus/formulas_1_2.json",
    "formulas_1_k":     "corpus/formulas_1_k.json",
    "defaults_config":  "config/gabriel_defaults.yaml",
}

# ─────────────────────────────────────────────────────────
#  STRUCTURES DE DONNÉES
# ─────────────────────────────────────────────────────────
@dataclass
class PipelineStage:
    stage_id:      int
    name:          str
    status:        str          # OK | FAULT | WARNING | SKIPPED
    file_involved: str
    input_data:    dict = field(default_factory=dict)
    output_data:   dict = field(default_factory=dict)
    fault_detail:  Optional[str] = None
    log_evidence:  Optional[str] = None

@dataclass
class PipelineReport:
    session_date:    str
    user_prompt:     str
    total_stages:    int
    fault_count:     int
    warning_count:   int
    ok_count:        int
    stages:          List[PipelineStage] = field(default_factory=list)
    final_answer:    dict = field(default_factory=dict)
    expected_answer: dict = field(default_factory=dict)

# ─────────────────────────────────────────────────────────
#  PARSEUR DE LOG
# ─────────────────────────────────────────────────────────
class GabrielLogParser:
    """Parse le fichier de log brut de Gabriel et extrait les événements clés."""

    SPINNER_CHARS = "⠸⠧⠼⠙⠋"

    def __init__(self, log_path: str):
        self.log_path = Path(log_path)
        self.raw_text = ""
        self.events   = []

    def load(self) -> "GabrielLogParser":
        if self.log_path.exists():
            self.raw_text = self.log_path.read_text(encoding="utf-8")
        else:
            # Fallback : log intégré (extrait de la session réelle)
            self.raw_text = EMBEDDED_LOG
        return self

    def parse(self) -> dict:
        """Retourne un dictionnaire structuré des événements du log."""
        result = {
            "user_prompt":       self._extract_prompt(),
            "spinner_frames":    self._count_spinner_frames(),
            "analyse_en_cours":  self._count_analyse_en_cours(),
            "response_score":    self._extract_score(),
            "response_iter":     self._extract_iter(),
            "chiffres_calcules": self._extract_chiffres(),
            "axe4_certainty":    self._extract_certainty(),
            "hol_fragment":      self._extract_hol(),
            "response_body":     self._extract_response_body(),
        }
        return result

    def _extract_prompt(self) -> str:
        m = re.search(r"Philippe\s*>\s*(.+)", self.raw_text)
        return m.group(1).strip() if m else "UNKNOWN"

    def _count_spinner_frames(self) -> int:
        return len(re.findall(r"Execution pipeline \+ multiloop", self.raw_text))

    def _count_analyse_en_cours(self) -> int:
        return len(re.findall(r"Analyse en cours\.\.\.", self.raw_text))

    def _extract_score(self) -> Optional[float]:
        m = re.search(r"score\s+([\d.]+)/10", self.raw_text)
        return float(m.group(1)) if m else None

    def _extract_iter(self) -> Optional[int]:
        m = re.search(r"iter\s+(\d+)", self.raw_text)
        return int(m.group(1)) if m else None

    def _extract_chiffres(self) -> dict:
        block = self._extract_block("Chiffres calcules")
        if not block:
            return {}
        result = {}
        pairs = re.findall(r"(\w[\w_]*)\s*=\s*([^\n│]+)", block)
        for key, val in pairs:
            val = val.strip().rstrip("│").strip()
            result[key] = val
        return result

    def _extract_certainty(self) -> dict:
        block = self._extract_block("Niveau de certitude")
        if not block:
            return {}
        result = {}
        for line in block.splitlines():
            line = line.strip().strip("│").strip()
            if "=" in line:
                k, v = line.split("=", 1)
                result[k.strip()] = v.strip()
            elif line.startswith("Provenance"):
                result["Provenance"] = line.split(":", 1)[-1].strip()
            elif line in ("CERTAIN", "INCERTAIN", "PROBABLE"):
                result["niveau"] = line
        return result

    def _extract_hol(self) -> str:
        block = self._extract_block("Fragment HOL genere")
        return block.strip() if block else ""

    def _extract_response_body(self) -> str:
        m = re.search(
            r"Reponse.*?╮\n(.*?)╰",
            self.raw_text,
            re.DOTALL,
        )
        return m.group(1).strip() if m else ""

    def _extract_block(self, header: str) -> str:
        pattern = rf"─+ {re.escape(header)} ─+.*?╮\n(.*?)╰"
        m = re.search(pattern, self.raw_text, re.DOTALL)
        return m.group(1) if m else ""


# ─────────────────────────────────────────────────────────
#  RECONSTRUCTEUR DE PIPELINE
# ─────────────────────────────────────────────────────────
class PipelineReconstructor:
    """Reconstruit les étapes du pipeline à partir des événements parsés."""

    def __init__(self, parsed: dict):
        self.p = parsed

    def reconstruct(self) -> PipelineReport:
        chiffres = self.p["chiffres_calcules"]
        prompt   = self.p["user_prompt"]

        report = PipelineReport(
            session_date    = datetime.now().strftime("%Y-%m-%d %H:%M"),
            user_prompt     = prompt,
            total_stages    = 0,
            fault_count     = 0,
            warning_count   = 0,
            ok_count        = 0,
        )

        stages = [
            self._stage_reception(prompt),
            self._stage_parsing(prompt),
            self._stage_dispatch(chiffres),
            self._stage_model_selection(chiffres),
            self._stage_formula_loading(chiffres),
            self._stage_multiloop_init(self.p["spinner_frames"]),
            self._stage_sa_sb_compute(chiffres),
            self._stage_prime_reconstruct(chiffres),
            self._stage_digamma(chiffres),
            self._stage_equation_check(chiffres),
            self._stage_scoring(self.p["response_score"], self.p["response_iter"]),
            self._stage_hol_generation(self.p["hol_fragment"]),
            self._stage_response_assembly(chiffres),
        ]

        report.stages      = stages
        report.total_stages = len(stages)
        report.fault_count  = sum(1 for s in stages if s.status == "FAULT")
        report.warning_count= sum(1 for s in stages if s.status == "WARNING")
        report.ok_count     = sum(1 for s in stages if s.status == "OK")

        report.final_answer = {
            "p":          chiffres.get("p", "?"),
            "SA":         chiffres.get("SA_float", "?"),
            "SB":         chiffres.get("SB_float", "?"),
            "model_used": chiffres.get("model", "?"),
        }
        report.expected_answer = {
            "p":          "1097",
            "SA":         "8.8327e+13",
            "SB":         "3.5331e+14",
            "model_used": "1/4",
        }

        return report

    # ── Étapes individuelles ──────────────────────────────

    def _stage_reception(self, prompt: str) -> PipelineStage:
        return PipelineStage(
            stage_id=1, name="Réception de la requête utilisateur",
            status="OK",
            file_involved=REPO_FILES["multiloop_engine"],
            input_data={"raw_text": prompt},
            output_data={"parsed_intent": "reconstruction_premier_spectral"},
            log_evidence="Philippe > Reconstruit le premier pour le rapport 1/4 pour n=23",
        )

    def _stage_parsing(self, prompt: str) -> PipelineStage:
        # Gabriel a bien parsé k=1/4 et n=23 (les formules SA/SB mentionnées sont bonnes)
        return PipelineStage(
            stage_id=2, name="Parsing des paramètres (k, n)",
            status="OK",
            file_involved=REPO_FILES["spectral_core"],
            input_data={"prompt": prompt},
            output_data={"k": 4, "n": 23, "ratio": "1/4"},
            log_evidence="Étape 2 : SA(23)=(241/192)*4^23-4/3 et SB(23)=(964/192)*4^23-12292/3",
        )

    def _stage_dispatch(self, chiffres: dict) -> PipelineStage:
        model_found = chiffres.get("model", "?")
        fault = (model_found != "1/4")
        return PipelineStage(
            stage_id=3, name="Dispatch vers le moteur de calcul (ratio_dispatcher)",
            status="FAULT" if fault else "OK",
            file_involved=REPO_FILES["ratio_dispatcher"],
            input_data={"ratio_demandé": "1/4", "k": 4},
            output_data={"model_sélectionné": model_found},
            fault_detail=(
                f"ratio_dispatcher a retourné model='{model_found}' "
                f"au lieu de '1/4'. Vraisemblablement : fallback "
                f"sur la valeur par défaut dans config/gabriel_defaults.yaml."
            ) if fault else None,
            log_evidence="model = 1/2  ← présent dans Chiffres calculés",
        )

    def _stage_model_selection(self, chiffres: dict) -> PipelineStage:
        invariant = "INVARIANT (ratio 1/2): position = n = number_of_terms = 23"
        return PipelineStage(
            stage_id=4, name="Sélection du modèle et de l'invariant",
            status="FAULT",
            file_involved=REPO_FILES["spectral_model"],
            input_data={"model_dispatché": "1/2 (erroné)"},
            output_data={
                "invariant_appliqué": "position = n = number_of_terms",
                "base_puissance":     "2^n  (erronée, devrait être 4^n)",
            },
            fault_detail=(
                "spectral_model.py a chargé le modèle 1/2 : l'invariant "
                "'position=n=terms' est appliqué. Pour k=4, l'invariant correct "
                "est n=terms ≠ position_premier."
            ),
            log_evidence=invariant,
        )

    def _stage_formula_loading(self, chiffres: dict) -> PipelineStage:
        return PipelineStage(
            stage_id=5, name="Chargement des formules SA/SB",
            status="FAULT",
            file_involved=REPO_FILES["formulas_1_2"],
            input_data={"fichier_chargé": "corpus/formulas_1_2.json  (FAUTIF)"},
            output_data={
                "SA_coeff": "3.25/2 × 2^n - 2",
                "SB_coeff": "6.5/2  × 2^n - 66",
            },
            fault_detail=(
                "formulas_1_2.json chargé au lieu de formulas_1_k.json. "
                "Les coefficients 241/192 et 964/192 avec base 4^n n'ont pas été utilisés."
            ),
            log_evidence=(
                "SA(23)=13631486.0 = (3.25/2)×2^23-2  "
                "SB(23)=27262910.0 = (6.5/2)×2^23-66"
            ),
        )

    def _stage_multiloop_init(self, frames: int) -> PipelineStage:
        return PipelineStage(
            stage_id=6, name=f"Initialisation multiloop ({frames} frames spinner)",
            status="OK",
            file_involved=REPO_FILES["multiloop_engine"],
            input_data={"max_iter": "configurable", "frames_observés": frames},
            output_data={"iter_atteinte": 2},
            log_evidence=f"{frames} occurrences 'Execution pipeline + multiloop' dans les logs",
        )

    def _stage_sa_sb_compute(self, chiffres: dict) -> PipelineStage:
        sa = chiffres.get("SA_float", "?")
        sb = chiffres.get("SB_float", "?")
        fault = (sa == "13631486.0")
        return PipelineStage(
            stage_id=7, name="Calcul numérique SA(n) et SB(n)",
            status="FAULT" if fault else "OK",
            file_involved=REPO_FILES["spectral_core"],
            input_data={"n": 23, "formules": "modèle 1/2 (erroné)"},
            output_data={"SA": sa, "SB": sb},
            fault_detail=(
                f"SA={sa} et SB={sb} sont les valeurs du modèle 1/2. "
                f"Valeurs correctes (k=4) : SA≈8.8327e13, SB≈3.5331e14."
            ) if fault else None,
            log_evidence=f"SA_float={sa}, SB_float={sb}",
        )

    def _stage_prime_reconstruct(self, chiffres: dict) -> PipelineStage:
        p = chiffres.get("p", "?")
        fault = (p == "83")
        return PipelineStage(
            stage_id=8, name="Reconstruction du nombre premier P",
            status="FAULT" if fault else "OK",
            file_involved=REPO_FILES["spectral_core"],
            input_data={"n": 23, "invariant": "position=n=23 (erroné pour k=4)"},
            output_data={"p_reconstruit": p, "position_retournée": "23"},
            fault_detail=(
                f"p={p} est le 23ème premier (modèle 1/2). "
                f"Résultat attendu : p=1097 (184ème premier, modèle 1/4)."
            ) if fault else None,
            log_evidence=f"p = {p}, prime = {p}",
        )

    def _stage_digamma(self, chiffres: dict) -> PipelineStage:
        dg = chiffres.get("digamma_calc_float", "?")
        return PipelineStage(
            stage_id=9, name="Calcul du Digamma",
            status="FAULT",
            file_involved=REPO_FILES["spectral_core"],
            input_data={"SB": "27262910.0 (erroné)", "p": "83 (erroné)", "exp": "4096"},
            output_data={"digamma_calc": dg},
            fault_detail=(
                "digamma_calc = SB_wrong - 4096×p_wrong = 27262910 - 4096×83 = 27257598. "
                "Valeur correcte : SB_correct - 4096×1097 = 3.5331e14 - 4493312 ≈ 3.5331e14."
            ),
            log_evidence=f"digamma_calc_float = {dg}",
        )

    def _stage_equation_check(self, chiffres: dict) -> PipelineStage:
        holds = chiffres.get("equation_holds", "?")
        return PipelineStage(
            stage_id=10, name="Vérification equation_holds (faux positif)",
            status="WARNING",
            file_involved=REPO_FILES["spectral_core"],
            input_data={"SA": "13631486", "SB": "27262910", "digamma": "27257598", "p": "83"},
            output_data={"equation_holds": holds},
            fault_detail=(
                "equation_holds=True est un FAUX POSITIF : l'équation tautologique "
                "(SB - (SB - 4096×p)) / 4096 = p est toujours vraie quel que soit p. "
                "Elle ne valide pas que p=83 est correct pour k=1/4."
            ),
            log_evidence=f"equation_holds = {holds}",
        )

    def _stage_scoring(self, score: float, iteration: int) -> PipelineStage:
        return PipelineStage(
            stage_id=11, name=f"Évaluation par le scorer (score={score}/10, iter={iteration})",
            status="WARNING",
            file_involved=REPO_FILES["scorer"],
            input_data={"réponse_proposée": "p=83", "iter": iteration},
            output_data={"score": score},
            fault_detail=(
                f"Le scorer a attribué {score}/10 sans détecter l'incohérence "
                f"model=1/2 pour une requête k=1/4. Le critère de validation "
                f"du ratio dans scorer.py semble absent ou non pondéré."
            ),
            log_evidence=f"score {score}/10, iter {iteration}",
        )

    def _stage_hol_generation(self, hol: str) -> PipelineStage:
        fault = "SA(n) = (3.25/2)" in hol or "2^n" in hol
        return PipelineStage(
            stage_id=12, name="Génération du fragment HOL (Isabelle)",
            status="FAULT" if fault else "OK",
            file_involved=REPO_FILES["hol_generator"],
            input_data={"theory_name": "verif_p83_n23", "imports": "methode_spectral"},
            output_data={"lemma_principal": "prime_equation 23 83 = real 83"},
            fault_detail=(
                "hol_generator.py a généré un fragment titré 'Verification 83 via modele 1/4' "
                "mais les lemmes utilisent SA_def/SB_def du modèle 1/2 (2^n). "
                "Le fragment HOL est doublement incorrect : titre ET contenu."
            ) if fault else None,
            log_evidence="theory verif_p83_n23 / SA(n)=(3.25/2)×2^n-2",
        )

    def _stage_response_assembly(self, chiffres: dict) -> PipelineStage:
        return PipelineStage(
            stage_id=13, name="Assemblage et transmission de la réponse",
            status="FAULT",
            file_involved=REPO_FILES["multiloop_engine"],
            input_data={"score": 8.1, "iter": 2},
            output_data={
                "p_transmis": chiffres.get("p", "?"),
                "message": "L'équation est vérifiée : equation_holds=True",
            },
            fault_detail=(
                "La réponse transmise (p=83) est fausse malgré iter=2 : "
                "le multiloop n'a pas détecté la faute de dispatch ratio. "
                "La boucle de correction ne teste pas l'adéquation model/ratio."
            ),
            log_evidence="Premier reconstruit : p=83  ← affiché à l'utilisateur",
        )


# ─────────────────────────────────────────────────────────
#  FORMATEUR DE RAPPORT
# ─────────────────────────────────────────────────────────
class ReportFormatter:

    STATUS_ICON = {"OK": "✅", "FAULT": "🔴", "WARNING": "⚠️", "SKIPPED": "⏭️"}

    def format(self, report: PipelineReport) -> str:
        lines = []
        sep = "═" * 80

        lines += [
            sep,
            " GABRIEL PIPELINE TRACE — Rapport d'analyse de session",
            sep,
            f" Date session    : {report.session_date}",
            f" Requête         : {report.user_prompt}",
            f" Étapes totales  : {report.total_stages}",
            f" ✅ OK           : {report.ok_count}",
            f" 🔴 FAUTES       : {report.fault_count}",
            f" ⚠️  AVERTISSEMENTS: {report.warning_count}",
            sep, "",
        ]

        for stage in report.stages:
            icon = self.STATUS_ICON.get(stage.status, "?")
            lines.append(f"{'─'*80}")
            lines.append(f" ÉTAPE {stage.stage_id:02d} {icon} {stage.status} — {stage.name}")
            lines.append(f" Fichier : {stage.file_involved}")
            if stage.input_data:
                lines.append(f" Input   : {json.dumps(stage.input_data, ensure_ascii=False)}")
            if stage.output_data:
                lines.append(f" Output  : {json.dumps(stage.output_data, ensure_ascii=False)}")
            if stage.log_evidence:
                lines.append(f" Log     : {stage.log_evidence}")
            if stage.fault_detail:
                lines.append(f" DÉTAIL  : {stage.fault_detail}")
            lines.append("")

        lines += [
            sep,
            " COMPARAISON RÉPONSE GABRIEL vs RÉPONSE ATTENDUE",
            sep,
            f"{'Paramètre':<20} {'Gabriel (erroné)':<30} {'Attendu (correct)'}",
            f"{'─'*20} {'─'*30} {'─'*30}",
        ]
        for key in report.final_answer:
            got  = str(report.final_answer.get(key, "?"))
            want = str(report.expected_answer.get(key, "?"))
            flag = "  ✗" if got != want else "  ✓"
            lines.append(f"{key:<20} {got:<30} {want}{flag}")

        lines += [
            "",
            sep,
            " FICHIERS FAUTIFS IDENTIFIÉS",
            sep,
        ]
        faulty_files = list({
            s.file_involved for s in report.stages if s.status == "FAULT"
        })
        for f in sorted(faulty_files):
            lines.append(f"  🔴  {f}")

        lines += [
            "",
            sep,
            " → Ce rapport est consommé par gabriel_02_engine_audit.py",
            sep,
        ]

        return "\n".join(lines)


# ─────────────────────────────────────────────────────────
#  LOG EMBARQUÉ (fallback si aucun fichier passé)
# ─────────────────────────────────────────────────────────
EMBEDDED_LOG = """Philippe > Reconstruit le premier pour le rapport 1/4 pour n=23
[spinner x12 — Execution pipeline + multiloop / Analyse en cours...]
╭──── Reponse  (score 8.1/10, iter 2) ──────╮
│ Premier reconstruit p = 83                 │
╰────────────────────────────────────────────╯
╭──── Chiffres calcules ─────────────────────╮
│ position = 23                              │
│ n = 23                                     │
│ num_terms = 23                             │
│ p = 83                                     │
│ prime = 83                                 │
│ SA_float = 13631486.0                      │
│ SB_float = 27262910.0                      │
│ digamma_calc_float = 83.0                  │
│ equation_holds = True                      │
│ model = 1/2                                │
│ INVARIANT (ratio 1/2): position = n = 23  │
╰────────────────────────────────────────────╯
╭──── Niveau de certitude (Axe 4) ───────────╮
│ CERTAIN   citable=oui                      │
│   Provenance : SpectralCore                │
╰────────────────────────────────────────────╯
╭──── Fragment HOL genere ────────────────────╮
│ theory verif_p83_n23                       │
│   SA(n) = (3.25/2) × 2^n - 2              │
│   SB(n) = (6.5/2) × 2^n - 66             │
│   lemma verif_premier_83_n_23             │
╰────────────────────────────────────────────╯
"""


# ─────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────
def main():
    log_path = sys.argv[1] if len(sys.argv) > 1 else "session_gabriel.txt"

    print("Gabriel Pipeline Trace — Script 1/3")
    print(f"Fichier log : {log_path}\n")

    parsed    = GabrielLogParser(log_path).load().parse()
    report    = PipelineReconstructor(parsed).reconstruct()
    formatted = ReportFormatter().format(report)

    # Affichage console
    print(formatted)

    # Sauvegarde pour Script 2
    output_path = Path("rapport_pipeline.txt")
    output_path.write_text(formatted, encoding="utf-8")

    # Sauvegarde JSON structuré pour Script 2 et 3
    import dataclasses
    def serialize(obj):
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        return str(obj)

    json_path = Path("rapport_pipeline.json")
    json_path.write_text(
        json.dumps(dataclasses.asdict(report), indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )

    print(f"\n✅ Rapport texte sauvegardé : {output_path}")
    print(f"✅ Rapport JSON sauvegardé  : {json_path}")
    print(f"→ Prochaine étape : python3 gabriel_02_engine_audit.py rapport_pipeline.json")


if __name__ == "__main__":
    main()

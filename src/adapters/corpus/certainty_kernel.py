"""
CertaintyKernel — Noyau de Certitude Spectral.

Distillat MINIMAL des 4 sources de verite :
  1. theories/methode_spectral.thy  (definitions et axiomes Isabelle/HOL)
  2. theories/validation_hol_unifiee.thy  (NOUVELLE: contre-validation formelle)
  3. theories/geometrie_spectre_premier.thy  (structures geometriques v2)
  4. spectral_knowledge.py  (plan cognitif injecte dans le prompt LLM)

Le kernel expose uniquement les INVARIANTS PROUVES (axiomatises ou lemmes
demonstres) qui constituent la verite spectrale d'urgence : c'est sur ces
elements que le Slow-Motion Debugger se replie quand une incoherence
est detectee dans le pipeline normal.

PHILOSOPHIE :
  - Aucun calcul probabiliste, aucune inference LLM.
  - Chaque entree porte une PROVENANCE (fichier.thy + ligne, ou plan).
  - Si une question peut etre repondue uniquement avec le kernel,
    la reponse est CERTAINE (pas d'hallucination possible).
  - validation_hol_unifiee.thy sert de contre-validation indépendante.
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


logger = logging.getLogger(__name__)


@dataclass
class Certainty:
    """Une certitude atomique extraite des sources."""
    key: str                      # identifiant court ex: "SA_def", "INVARIANT_1_2"
    statement: str                # enonce textuel court et autonome
    formula: Optional[str] = None # formule mathematique si applicable
    provenance: list[str] = field(default_factory=list)  # ["methode_spectral.thy:21", "validation_hol_unifiee.thy:45"]
    domain: str = "general"       # "ratio_1_2" | "ratio_1_3" | "ratio_1_4" | "geometry" | "general"
    confidence: float = 1.0       # 1.0 = prouve, 0.95 = axiomatise

    def cite(self) -> str:
        """Citation lisible avec provenance."""
        prov = " + ".join(self.provenance) if self.provenance else "kernel"
        return f"[{prov}] {self.statement}"


class CertaintyKernel:
    """
    Noyau de Certitude : agrege et indexe les invariants des 4 sources.
    
    Methodes principales :
      - get(key)             : recupere une certitude par sa cle
      - by_domain(domain)    : toutes les certitudes d'un domaine
      - search(keywords)     : recherche par mots-cles
      - applicable_to(question) : selection automatique selon une requete
      - emergency_summary(domain) : resume minimal certifie d'un domaine
    """

    def __init__(self, theories_dir: str | Path = "/home/agent/app/theories"):
        self.theories_dir = Path(theories_dir)
        self.certainties: dict[str, Certainty] = {}
        self._build_kernel()
        logger.info("CertaintyKernel: %d certitudes chargees (4 sources)", len(self.certainties))

    # ---------- Construction ----------

    def _build_kernel(self) -> None:
        """Construit le noyau a partir des 4 sources."""
        self._load_methode_spectral_thy()
        self._load_validation_hol_unifiee()  # NOUVELLE SOURCE
        self._load_geometrie_spectre_thy()
        self._load_cognitive_plan()
        self._add_distilled_invariants()

    def _load_methode_spectral_thy(self) -> None:
        """Extrait definitions + axiomes de methode_spectral.thy."""
        path = self.theories_dir / "methode_spectral.thy"
        if not path.exists():
            logger.warning("methode_spectral.thy introuvable a %s", path)
            return
        text = path.read_text(encoding="utf-8")

        # Definitions stables
        defs = [
            ("SA_def", "SA(n) = (3.25/2) * 2^n - 2",
             "SA n = (3.25 / 2) * (2 ^ n) - 2", "ratio_1_2"),
            ("SB_def", "SB(n) = (6.5/2) * 2^n - 66",
             "SB n = (6.5 / 2) * (2 ^ n) - 66", "ratio_1_2"),
            ("RsP_def", "Rapport spectral RsP(n1,n2) = (SA(n1)-SA(n2)) / (SB(n1)-SB(n2)) = 1/2",
             "RsP n1 n2 = 1/2", "ratio_1_2"),
            ("digamma_calc_def", "digamma_calc(n,p) = SB(n) - 64*p",
             "digamma_calc n p = SB n - 64 * p", "ratio_1_2"),
            ("prime_equation_identity",
             "Identite : prime_equation(n,p) = p  (lemme prouve)",
             "(SB(n) - digamma_calc(n,p)) / 64 = p", "ratio_1_2"),
            ("A_1_4_def", "A_1_4(n) = ((241/16)/12) * 4^n - 4/3",
             "A_1_4 n = ((241/16)/12) * (4^n) - 4/3", "ratio_1_4"),
            ("B_1_4_def", "B_1_4(n) = ((964/16)/12) * 4^n - 3073*(4/3)",
             "B_1_4 n = ((964/16)/12) * (4^n) - 3073*(4/3)", "ratio_1_4"),
            ("A_1_3_def", "A_1_3(n) = ((73/9)/12) * 3^n - 1.5",
             "A_1_3 n = ((73/9)/12) * (3^n) - 1.5", "ratio_1_3"),
            ("B_1_3_def", "B_1_3(n) = ((219/9)/12) * 3^n - 487*1.5",
             "B_1_3 n = ((219/9)/12) * (3^n) - 487*1.5", "ratio_1_3"),
        ]
        for key, statement, formula, domain in defs:
            # Verifie que la definition existe textuellement dans le fichier
            base = key.split("_")[0]
            if base in text or statement.split("(")[0].strip() in text:
                line = self._find_line(text, base)
                self.certainties[key] = Certainty(
                    key=key, statement=statement, formula=formula,
                    provenance=[f"methode_spectral.thy:{line}"],
                    domain=domain, confidence=1.0,
                )

        # Axiomes (confidence 0.95 - postules)
        axioms = [
            ("spectral_postulate_pos",
             "Pour tout n>=1 et p premier : prime_equation(n,p) = p",
             "n>=1 AND prime(p) => prime_equation(n,p) = p", "ratio_1_2"),
            ("spectral_postulate_1_4",
             "Pour tout n>0 et p premier : (B_1_4(n) - (B_1_4(n) - 4096*p))/4096 = p",
             "(B_1_4(n) - (B_1_4(n) - 4096p))/4096 = p", "ratio_1_4"),
            ("spectral_postulate_1_3",
             "Pour tout n>0 et p premier : (B_1_3(n) - (B_1_3(n) - 729*p))/729 = p",
             "(B_1_3(n) - (B_1_3(n) - 729p))/729 = p", "ratio_1_3"),
        ]
        for key, statement, formula, domain in axioms:
            if key in text:
                line = self._find_line(text, key)
                self.certainties[key] = Certainty(
                    key=key, statement=statement, formula=formula,
                    provenance=[f"methode_spectral.thy:{line}"],
                    domain=domain, confidence=0.95,
                )

    def _load_validation_hol_unifiee(self) -> None:
        """Extrait invariants de validation HOL unifiee (contre-validation)."""
        path = self.theories_dir / "validation_hol_unifiee.thy"
        if not path.exists():
            logger.warning("validation_hol_unifiee.thy introuvable a %s", path)
            return
        text = path.read_text(encoding="utf-8")

        entries = [
            ("validation_digamma_formula",
             "VALIDATION: Formule digamma correcte = B(n) - 64*P (avec soustraction obligatoire)",
             "digamma_validation n p = B_validation n - 64 * (real p)", "ratio_1_2"),
            ("validation_prime_reconstruction",
             "Identité formelle seulement: la reconstruction vaut n et ne certifie pas que n est premier",
             "prime_nth_reconstruction n = real n", "ratio_1_2"),
            ("validation_A_growth",
             "VALIDATION: A(n) croit exponentiellement et strictement",
             "∀ n m. n < m ⟶ A_validation n < A_validation m", "ratio_1_2"),
            ("validation_B_growth",
             "VALIDATION: B(n) croit exponentiellement et strictement",
             "∀ n m. n < m ⟶ B_validation n < B_validation m", "ratio_1_2"),
            ("rsa_convergence_is_definition_only",
             "La convergence RSA est définie comme prédicat, mais aucun théorème de convergence ne la prouve ici",
             "rsa_converges_to_half blockA blockB", "ratio_1_2"),
            ("validation_Sr2_normalization",
             "VALIDATION: Constante Sr2 = 1.5 agit comme facteur de normalisation",
             "Sr2_validation = 3 / 2", "ratio_1_2"),
            ("validation_riemann_eigenvalues",
             "Le modèle ne démontre pas la correspondance: le théorème formel réfute la propriété pour l’opérateur défini",
             "¬ riemann_zeros_as_eigenvalues", "geometry"),
            ("validation_coherence_A_B",
             "VALIDATION: Coherence prouvee entre A(n) et B(n) dans la geometrie",
             "2 * A_validation n = B_validation n + 62", "ratio_1_2"),
        ]
        for key, statement, formula, domain in entries:
            keyword = key.split("_")[1] if "_" in key else key
            if keyword in text or key.replace("_", "").lower() in text.lower().replace("_", ""):
                line = self._find_line(text, keyword)
                conf = 1.0 if "validation" in key.lower() else 0.95
                self.certainties[key] = Certainty(
                    key=key, statement=statement, formula=formula,
                    provenance=[f"validation_hol_unifiee.thy:{line}"],
                    domain=domain, confidence=conf,
                )

    def _load_geometrie_spectre_thy(self) -> None:
        """Extrait invariants geometriques + lemme reconstruction_P."""
        path = self.theories_dir / "geometrie_spectre_premier.thy"
        if not path.exists():
            logger.warning("geometrie_spectre_premier.thy introuvable a %s", path)
            return
        text = path.read_text(encoding="utf-8")

        entries = [
            ("Z_def", "Constante Z = 64 (rapport 1/2)", "Z = 64", "ratio_1_2"),
            ("D_def", "D(n,P) = SB(n) - SA(n) - Z*P", "D n P = SB n - SA n - Z*P", "ratio_1_2"),
            ("Dc_def", "Digamma calcule Dc(n,P) = SA(n) + D(n,P)",
             "Dc n P = SA n + D n P", "ratio_1_2"),
            ("P_reconstruit_def",
             "P_reconstruit(n,P) = (SB(n) - Dc(n,P)) / Z",
             "P_reconstruit n P = (SB n - Dc n P) / Z", "ratio_1_2"),
            ("reconstruction_P_lemma",
             "LEMME PROUVE : P_reconstruit(n,P) = P pour tout n et P",
             "P_reconstruit n P = P", "ratio_1_2"),
            ("comparaison_symetrique_nxn",
             "Comparaison nxn : |NA|=|NB|, |NC|=|ND|, NA!=NB, NC!=ND",
             "len(NA)=len(NB) AND len(NC)=len(ND) AND NA!=NB AND NC!=ND",
             "geometry"),
            ("comparaison_asym_ordonnee",
             "Asym ordonnee : blocs croissants + AO<BO + CO<DO (decalage chronologique)",
             "croissante(AO,BO,CO,DO) AND max(AO)<min(BO) AND max(CO)<min(DO)",
             "geometry"),
            ("SA_signed_def",
             "Extension signee : SA_signed(k>0)=SA(k), SA_signed(k<0)=3.25*2^k - 2",
             "SA_signed k = ...", "negatives"),
            ("SB_signed_def",
             "Extension signee : SB_signed(k>0)=SB(k), SB_signed(k<0)=6.5*2^k - 66",
             "SB_signed k = ...", "negatives"),
        ]
        for key, statement, formula, domain in entries:
            keyword = key.split("_")[0] if "_" in key else key
            if keyword in text or key.replace("_", "").lower() in text.lower().replace("_", ""):
                line = self._find_line(text, keyword)
                conf = 1.0 if "lemma" in key or "lemme" in statement.lower() else 0.95
                self.certainties[key] = Certainty(
                    key=key, statement=statement, formula=formula,
                    provenance=[f"geometrie_spectre_premier.thy:{line}"],
                    domain=domain, confidence=conf,
                )

    def _load_cognitive_plan(self) -> None:
        """Charge les regles du plan cognitif (spectral_knowledge.py)."""
        rules = [
            ("INVARIANT_1_2",
             "INVARIANT (rapport 1/2) : position_du_premier = n = nombre_de_termes_dans_A_et_B",
             "position = n = num_termes", "ratio_1_2"),
            ("RULE_n_1_3",
             "Rapport 1/3 : n est le nombre de termes (PAS la position du premier)",
             "n = num_termes ; n != position", "ratio_1_3"),
            ("RULE_n_1_4",
             "Rapport 1/4 : n est le nombre de termes (PAS la position du premier)",
             "n = num_termes ; n != position", "ratio_1_4"),
            ("RULE_no_dismissive",
             "Vocabulaire interdit : incoherent, absurde, faux, errone, invalide",
             None, "general"),
            ("RULE_prime_table",
             "Une table des 1000 premiers nombres premiers est disponible : "
             "nth_prime(N) retourne le N-eme premier sans calcul approximatif.",
             None, "general"),
        ]
        for key, statement, formula, domain in rules:
            self.certainties[key] = Certainty(
                key=key, statement=statement, formula=formula,
                provenance=["plan_cognitif"],
                domain=domain, confidence=1.0,
            )

    def _add_distilled_invariants(self) -> None:
        """
        DISTILLAT FINAL : les certitudes les plus utiles pour le debugger.
        Citent toutes leurs sources d'origine pour la traçabilite.
        """
        self.certainties["KERNEL_INVARIANT_RECONSTRUCTION_1_2"] = Certainty(
            key="KERNEL_INVARIANT_RECONSTRUCTION_1_2",
            statement=(
                "Pour reconstruire le N-ieme nombre premier p en rapport 1/2 : "
                "il faut prendre n = N termes dans les suites A et B. "
                "L'equation (SB(n) - digamma_calc(n,p)) / 64 = p est PROUVEE."
            ),
            formula="N -> nth_prime(N)=p ; SA(N), SB(N) ; (SB(N) - (SB(N)-64p))/64 = p",
            provenance=[
                "methode_spectral.thy::prime_equation_identity",
                "validation_hol_unifiee.thy::validation_prime_reconstruction",
                "geometrie_spectre_premier.thy::reconstruction_P",
                "plan_cognitif::INVARIANT_1_2",
            ],
            domain="ratio_1_2",
            confidence=1.0,
        )
        self.certainties["KERNEL_INVARIANT_Z_64"] = Certainty(
            key="KERNEL_INVARIANT_Z_64",
            statement="Pour le rapport 1/2 : la constante diviseuse est Z = 64 (= 2^6).",
            formula="Z = 64",
            provenance=[
                "geometrie_spectre_premier.thy::Z_def",
                "methode_spectral.thy::digamma_calc_def",
                "validation_hol_unifiee.thy::validation_digamma_formula",
            ],
            domain="ratio_1_2",
            confidence=1.0,
        )
        self.certainties["KERNEL_INVARIANT_Z_4096"] = Certainty(
            key="KERNEL_INVARIANT_Z_4096",
            statement="Pour le rapport 1/4 : la constante diviseuse est 4096 (= 4^6).",
            formula="Z_1_4 = 4096",
            provenance=["methode_spectral.thy::spectral_postulate_1_4"],
            domain="ratio_1_4",
            confidence=0.95,
        )
        self.certainties["KERNEL_INVARIANT_Z_729"] = Certainty(
            key="KERNEL_INVARIANT_Z_729",
            statement="Pour le rapport 1/3 : la constante diviseuse est 729 (= 3^6).",
            formula="Z_1_3 = 729",
            provenance=["methode_spectral.thy::spectral_postulate_1_3"],
            domain="ratio_1_3",
            confidence=0.95,
        )
        # NOUVELLES CERTITUDES : Configurations spectrales (PDF p.26-29 + .thy)
        self.certainties["KERNEL_CONFIG_1X1"] = Certainty(
            key="KERNEL_CONFIG_1X1",
            statement=(
                "Configuration 1*1 (cas classique) : RsP(n1,n2) = (SA(n1)-SA(n2))/(SB(n1)-SB(n2)) = 1/2 "
                "TOUJOURS, pour tout n1, n2 >= 1 avec n1 != n2."
            ),
            formula="RsP(n1,n2) = (SA(n1)-SA(n2)) / (SB(n1)-SB(n2)) = 1/2",
            provenance=[
                "methode_spectral.thy::RsP_un_demi_general (lemme prouve)",
                "validation_hol_unifiee.thy::validation_A_growth, validation_B_growth",
                "analyse_hypothese_riemann_savard.pdf::page_26",
            ],
            domain="ratio_1_2",
            confidence=1.0,
        )
        self.certainties["KERNEL_CONFIG_NXN_SYM"] = Certainty(
            key="KERNEL_CONFIG_NXN_SYM",
            statement=(
                "Hypothese experimentale : pour deux blocs A et B de meme longueur n>=2, "
                "le rapport RsP_nn(A,B) est attendu proche de 1/2; ce n'est pas un resultat "
                "demontre par validation_hol_unifiee.thy."
            ),
            formula="RsP_nn(A,B) = sum_list(map SA A) / sum_list(map SB B), avec |A|=|B|",
            provenance=[
                "methode_spectral.thy::RsP_nn (definition formelle)",
                "validation_hol_unifiee.thy::rsa_converges_to_half (definition seulement)",
                "analyse_hypothese_riemann_savard.pdf::page_26",
            ],
            domain="ratio_1_2",
            confidence=0.5,
        )
        self.certainties["KERNEL_CONFIG_ASYM_ORD"] = Certainty(
            key="KERNEL_CONFIG_ASYM_ORD",
            statement=(
                "Configuration asymetrique ORDONNEE : |B| = |A|+1, listes en ordre chronologique "
                "croissant strict, max(A) < min(B). Le rapport RsP_bloc(A,B) S'ECARTE de 1/2 "
                "(par ex. -1/6 pour A=(2,3) B=(5,7,11)). "
                "L'origine theorique precise de cet ecart reste en cours d'investigation "
                "et ne doit pas etre affirmee par Gabriel."
            ),
            formula="|B|=|A|+1 ; A,B strict croissants ; max(A)<min(B) ; RsP_bloc != 1/2",
            provenance=[
                "methode_spectral.thy::asymetrique_ordonnee_nat",
                "analyse_hypothese_riemann_savard.pdf::page_27 (exemple A=(2,3) B=(5,7,11))",
            ],
            domain="ratio_1_2",
            confidence=1.0,
        )
        self.certainties["KERNEL_CONFIG_ASYM_CHAOS"] = Certainty(
            key="KERNEL_CONFIG_ASYM_CHAOS",
            statement=(
                "Configuration asymetrique CHAOTIQUE : |A| != |B|, ordre quelconque. "
                "Le rapport RsP_bloc(A,B) = (sum_SA(A)-sum_SA(B)) / (sum_SB(A)-sum_SB(B)) "
                "REVIENT a 1/2 avec un faible reste numerique. "
                "L'origine theorique precise de cet ecart residuel reste en cours "
                "d'investigation et ne doit pas etre affirmee par Gabriel."
            ),
            formula="(sum_SA(A) - sum_SA(B)) / (sum_SB(A) - sum_SB(B)) ~= 1/2",
            provenance=[
                "methode_spectral.thy::RsP_bloc_1_2",
                "analyse_hypothese_riemann_savard.pdf::page_28 (exemple chaotique = 0.498311)",
            ],
            domain="ratio_1_2",
            confidence=1.0,
        )
        self.certainties["KERNEL_FALLBACK_PROCEDURE"] = Certainty(
            key="KERNEL_FALLBACK_PROCEDURE",
            statement=(
                "PROCEDURE D'URGENCE : si une question demande le N-ieme premier "
                "en rapport 1/2, la reponse certaine est : "
                "1) p = nth_prime(N)  2) n = N  3) SA(N), SB(N) calcules  "
                "4) Verification (SB(N) - (SB(N)-64p))/64 = p."
            ),
            formula=None,
            provenance=[
                "methode_spectral.thy",
                "validation_hol_unifiee.thy",
                "geometrie_spectre_premier.thy",
                "plan_cognitif",
            ],
            domain="ratio_1_2",
            confidence=1.0,
        )

    # ---------- Accès ----------

    def get(self, key: str) -> Optional[Certainty]:
        return self.certainties.get(key)

    def by_domain(self, domain: str) -> list[Certainty]:
        return [c for c in self.certainties.values() if c.domain == domain]

    def search(self, keywords: list[str]) -> list[Certainty]:
        """Recherche les certitudes contenant un des mots-cles."""
        result = []
        kws = [k.lower() for k in keywords]
        for cert in self.certainties.values():
            blob = (cert.statement + " " + (cert.formula or "") + " " + cert.key).lower()
            if any(kw in blob for kw in kws):
                result.append(cert)
        return result

    def applicable_to(self, question: str) -> list[Certainty]:
        """Selectionne les certitudes pertinentes pour une requete."""
        q = question.lower()
        domains: list[str] = []
        if "1/2" in q or "rapport 1/2" in q or ("premier" in q and "1/3" not in q and "1/4" not in q):
            domains.append("ratio_1_2")
        if "1/3" in q:
            domains.append("ratio_1_3")
        if "1/4" in q:
            domains.append("ratio_1_4")
        if "negatif" in q or "negative" in q or "-" in q:
            domains.append("negatives")
        if "geomet" in q or "compar" in q or "bloc" in q:
            domains.append("geometry")
        # Par defaut : general + ratio_1_2 (le plus utilise)
        if not domains:
            domains = ["ratio_1_2", "general"]
        domains.append("general")
        seen = set()
        result: list[Certainty] = []
        for d in domains:
            for c in self.by_domain(d):
                if c.key not in seen:
                    seen.add(c.key)
                    result.append(c)
        return result

    def emergency_summary(self, domain: str = "ratio_1_2") -> str:
        """
        Resume minimal certifie d'un domaine, sous forme de bloc texte
        compact que le Slow-Motion Debugger injecte dans sa reponse.
        """
        certs = self.by_domain(domain)
        kernel_first = sorted(certs, key=lambda c: (not c.key.startswith("KERNEL_"), c.key))
        if not kernel_first:
            return f"(aucune certitude pour le domaine '{domain}')"
        lines = [f"NOYAU DE CERTITUDE — {domain.upper()}"]
        for c in kernel_first[:6]:  # max 6 entrees pour rester court
            prefix = "★" if c.key.startswith("KERNEL_") else "•"
            lines.append(f"  {prefix} {c.statement}")
            if c.formula:
                lines.append(f"      formule : {c.formula}")
            lines.append(f"      source  : {', '.join(c.provenance)}")
        return "\n".join(lines)

    # ---------- Helpers ----------

    @staticmethod
    def _find_line(text: str, keyword: str) -> int:
        """Trouve la 1re ligne contenant le keyword (1-indexed)."""
        for i, line in enumerate(text.splitlines(), start=1):
            if keyword in line:
                return i
        return 0

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports

"""Dictionnaire Spectral Savard - 9 regimes mathematiques structures.

Source de verite officielle (conforme `theories/methode_spectral.thy`).

Chaque regime est une entite ontologique compose de :
  - concepts_cles       : mots-cles caracteristiques
  - patterns_detection  : regex pour identification automatique RAG
  - definitions_hol     : equations Isabelle/HOL formelles
  - lemmes_certifies    : theoremes prouves
  - regles_cognitives   : regles d'inference strictes
  - avertissements      : pieges et cas limites critiques
  - exemples_valides    : exemples numeriques verifies
  - ratio_attendu       : rapport spectral cible (Fraction ou None)

Total : 13 regimes (9 documentes officiellement + 'suites_finies' + XI/XII + Pont Savard XIII).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Optional


@dataclass
class Regime:
    """Une entite ontologique du dictionnaire spectral."""
    nom: str                                # identifiant systeme (snake_case)
    titre: str                              # titre lisible (humain)
    concepts_cles: list[str] = field(default_factory=list)
    patterns_detection: list[str] = field(default_factory=list)
    definitions_hol: dict[str, str] = field(default_factory=dict)
    lemmes_certifies: list[str] = field(default_factory=list)
    regles_cognitives: list[str] = field(default_factory=list)
    avertissements: list[str] = field(default_factory=list)
    exemples_valides: list[str] = field(default_factory=list)
    ratio_attendu: Optional[Fraction] = None

    def to_prompt_context(self) -> str:
        """Genere un bloc texte injectable dans le prompt LLM."""
        lines = [
            "+--- REGIME: " + self.titre.upper() + " " + "-" * (max(0, 50 - len(self.titre))) + "+",
            "|",
        ]
        if self.regles_cognitives:
            lines.append("| REGLES COGNITIVES CRITIQUES:")
            for i, r in enumerate(self.regles_cognitives, 1):
                lines.append(f"| {i}. {r}")
            lines.append("|")
        if self.definitions_hol:
            lines.append("| DEFINITIONS HOL:")
            for nom, defi in self.definitions_hol.items():
                lines.append(f"|   {nom}: {defi}")
            lines.append("|")
        if self.lemmes_certifies:
            lines.append("| LEMMES CERTIFIES:")
            for lem in self.lemmes_certifies:
                lines.append(f"|   [X] {lem}")
            lines.append("|")
        if self.avertissements:
            lines.append("| AVERTISSEMENTS CRITIQUES:")
            for av in self.avertissements:
                lines.append(f"|   ! {av}")
            lines.append("|")
        if self.ratio_attendu is not None:
            lines.append(f"| RATIO ATTENDU : {self.ratio_attendu}")
            lines.append("|")
        lines.append("+" + "-" * 60 + "+")
        return "\n".join(lines)


# ==========================================================================
# DICTIONNAIRE SPECTRAL OFFICIEL - 10 REGIMES
# ==========================================================================
DICTIONNAIRE_SPECTRAL: dict[str, Regime] = {

    # --------------------------------------------------------------------
    "regime_1_2_positif": Regime(
        nom="regime_1_2_positif",
        titre="Regime 1/2 Positif (Base SA, SB)",
        concepts_cles=["SA", "SB", "reconstruction", "ratio 1/2", "1/2"],
        patterns_detection=[
            r"\b1/2\b", r"\breconstruct", r"\bSA\b", r"\bSB\b",
            r"premier\s+(2[09]|31|47)", r"\bratio\s+1/2\b",
        ],
        definitions_hol={
            "SA": "SA n = (13/8) * (2^n) - 2",
            "SB": "SB n = (13/4) * (2^n) - 66",
            "digamma_calc": "digamma_calc n p = SB n - 64 * p",
            "prime_equation": "(SB n - digamma_calc n p) / 64 = p",
            "RsP": "RsP n1 n2 = (SA n1 - SA n2) / (SB n1 - SB n2) = 1/2",
            # [BQ-Q10] Formes générales alternatives (equivalentes) issues du fichier methode_spectral.thy
            "SA_general_Q10": "SA(n) = (3.25/2) * 2^n - 2  (equivalent a (13/8)*2^n - 2)",
            "SB_general_Q10": "SB(n) = (6.5/2) * 2^n - 66  (equivalent a (13/4)*2^n - 66)",
            # [BQ-Q6] Ratio spectral local entre termes consecutifs
            "ratio_spectral_local_Q6": "terme_spectral(i) = 1/2^i => terme_spectral(i+1)/terme_spectral(i) = 1/2",
            # [BQ-Q8] Postulat spectral positif (fondement axiomatique)
            "spectral_postulate_pos_Q8": "forall n>=1, forall p premier, prime_equation(n, p) = real(p)",
        },
        lemmes_certifies=[
            "reconstruction_p29_n5: (SB(5) - digamma(5,29)) / 64 = 29",
            "reconstruction_p31_n6: factor 64 verifie pour p=31",
            "reconstruction_p47_n15: extension validee pour n=15",
            "RsP_invariance_1_2: ratio EXACT = 1/2 pour 1x1 et nxn sym",
            # [BQ-Q5] Reconstruction du 12eme premier = 37 (banque Q&R validee Philippe)
            "[BQ-Q5] p37_n12: SB(12)=13246, SA(12)+digamma(37)=10878, (13246-10878)/64 = 37",
            # [BQ-Q6] Rapport spectral local entre termes consecutifs
            "[BQ-Q6] ratio_spectral_local: rapport termes consecutifs = 1/2 (via ratio_puissances_de_deux)",
            # [BQ-Q8] Axiome de validite positive
            "[BQ-Q8] spectral_postulate_pos: valide toutes les configurations spectrales du regime positif",
            # [BQ-Q10] Forme generale demontree
            "[BQ-Q10] RsP_un_demi_general: SA/SB en forme (a/2)*2^n - c => RsP = 1/2 par annulation des constantes",
        ],
        regles_cognitives=[
            "Facteur de reconstruction TOUJOURS = 64",
            "SA et SB sont definis sur N (positifs uniquement)",
            "Pour reconstruction : utiliser (SB - digamma) / 64",
            "Le ratio 1/2 est EXACT quand |A_pos| == |B_pos|",
        ],
        avertissements=[
            "Le ratio par SOMMES ne converge pas vers 1/2 ; utiliser DIFFERENCES",
            "Pour n grand (n>50), passer en log10 pour visualisation",
            "Le facteur 64 ET la formule digamma_calc(n,p) = SB(n) - 64*p SONT EXCLUSIFS au rapport 1/2 (k=2). Pour tout rapport 1/k non-typique (k != 2), le facteur de reconstruction est k^6 (ex. 14^6 = 7529536, 23^6 = 148035889, 50^6 = 282429536481) : JAMAIS recycler 64. Les equations A/B doivent etre reconstitues pour le k demande.",
        ],
        exemples_valides=[
            "prime(26) = 101 via SA(26), SB(26), factor 64",
            "RsP(3, 5) = 1/2 EXACT (cas 1x1)",
            # [BQ-Q5] Exemple canonique de reconstruction (position 12 -> 37)
            "[BQ-Q5] p=37 (12e premier) : (13246 - 10878) / 64 = 37 ; SB(12)=13246, SA(12)+digamma(37)=10878",
        ],
        ratio_attendu=Fraction(1, 2),
    ),

    # --------------------------------------------------------------------
    "regime_mixte": Regime(
        nom="regime_mixte",
        titre="Suites Mixtes (Asymptote K6)",
        concepts_cles=["mixte", "asymptote", "K6", "SA_mix", "frontiere"],
        patterns_detection=[
            r"\bmixte\b", r"\basymptot", r"\bK6\b",
            r"\bSA_mix\b", r"\bfronti[eè]re\b", r"-?\d+\s+et\s+\d+",
        ],
        definitions_hol={
            "K6": "K6 = -(37127/256) - SA_mix(6)",
            "SA_mix": "Suite SA etendue aux indices negatifs via powr",
            "SB_mix": "Suite SB etendue aux indices negatifs via powr",
            # [BQ-Q15] Formalisation Isabelle/HOL de l'ecart mixte
            "gap_mix_val_Q15": "gap_mix_val = (A_next - (B_high - D_high) - D_low) / 64",
            # [BQ-Q4/Q15] Valeurs spectrales exactes pour l'exemple canonique (-31, 17)
            "SA_m29_val_Q15": "SA_m29_val = -40895 / 20480  (suite A pour indice -10, prochain de -31 vers zero)",
            "SB_p17_val_Q15": "SB_p17_val = 350  (= (6.5/2)*2^7 - 66)",
            "D_p17_val_Q15": "D_p17_val = -738  (digamma pour 17)",
            "D_m31_val_Q15": "D_m31_val = 39280705 / 20480  (digamma pour -31)",
        },
        lemmes_certifies=[
            "K6_invariance: K6 = constante asymptotique pour 6 termes negatifs",
            "SA_mix_continuity: SA_mix continu sur intervalle [-13, 47]",
            "frontier_crossing: passage par n=0 inclus en mixte",
            "asymptote_validity: K6 valide pour mode 1/2 mixte",
            "mixed_lower_bound: borne inferieure stable sous K6",
            # [BQ-Q4] Ecart calcule sur exemple manuel Philippe (reference du fix pont ZERO)
            "[BQ-Q4] ecart_m31_17_calcule: (-22323135/20480 - 39280705/20480) / 64 = -47 nombres entre -31 et 17",
            # [BQ-Q15] Lemme Isabelle/HOL correspondant
            "[BQ-Q15] gap_m31_17: unfolding SA_m29_val, SB_p17_val, D_p17_val, D_m31_val + simp => -47",
        ],
        regles_cognitives=[
            "En mixte : zero EST inclus dans le decompte",
            "K6 = -(37127/256) - SA_mix(6) est une CONSTANTE rigide",
            "Utiliser powr (puissance continue) pour indices negatifs",
            "Asymptote K6 = horizon limite des suites mixtes",
        ],
        avertissements=[
            "K6 n'est PAS interpolable : utiliser sa valeur exacte",
            "Le passage frontiere n=0 change la formule applicable",
            "JAMAIS d'interpolation entre indices positifs et negatifs",
        ],
        exemples_valides=[
            "6 termes negatifs : SA_mix(-6..-1) convergent vers K6",
            "gap_mixed(-13, 47) = -59 (zero inclus, comptabilite spectrale)",
            # [BQ-Q4/Q15] Exemple canonique validee par calcul manuel Philippe
            "[BQ-Q4/Q15] gap_mixed(-31, 17) = -47 (30 negatifs + 0[1] + 16 positifs = 47)",
        ],
        ratio_attendu=Fraction(1, 2),
    ),

    # --------------------------------------------------------------------
    "regime_1_4": Regime(
        nom="regime_1_4",
        titre="Regime 1/4 (Extension Quartique)",
        concepts_cles=["1/4", "quartique", "947", "4096"],
        patterns_detection=[
            r"\b1/4\b", r"\bquartique\b", r"\b947\b", r"\b4096\b",
            r"A_1_4", r"B_1_4",
        ],
        definitions_hol={
            "A_1_4": "A_1_4 n = (241/192) * (4^n) - 4/3",
            "B_1_4": "B_1_4 n = (964/192) * (4^n) - 12292/3",
            "prime_eq_1_4": "(B_1_4 n - (B_1_4 n - 4096 * p)) / 4096 = p",
            "RsP_1_4": "(A_1_4 n1 - A_1_4 n2) / (B_1_4 n1 - B_1_4 n2) = 1/4",
            # [BQ-Q14] Valeurs concretes du modele 1/4 (exemple 947)
            "suite_A_1_4_somme_Q14": "suite_A_1_4_somme = 1316180",
            "suite_B_1_4_somme_Q14": "suite_B_1_4_somme = 5260628",
            "digamma_1_4_Q14": "digamma_1_4 = 65536",
            "digamma_calcule_1_4_Q14": "digamma_calcule_1_4 = suite_A_1_4_somme + digamma_1_4 = 1381716",
        },
        lemmes_certifies=[
            "p947_reconstruction_1_4: factor 4096 valide a haute position",
            "RsP_1_4_exact: ratio EXACT = 1/4 pour blocs symetriques",
            # [BQ-Q14] Preuve formelle du premier 947 en modele 1/4
            "[BQ-Q14] preuve_premier_947: (5260628 - 1381716) / 4096 = 947 (3878912 / 4096 = 947)",
        ],
        regles_cognitives=[
            "Facteur de reconstruction = 4096 (= 64^2)",
            "Puissance de base = 4 (extension quartique de la base 2)",
            "Coefficients : 241/192 et 964/192 (jamais arrondi)",
        ],
        avertissements=[
            "Ne pas confondre 4096 (regime 1/4) avec 64 (regime 1/2)",
            "Les coefficients sont RIGIDES : aucune simplification",
        ],
        exemples_valides=[
            "p=947 reconstruit via A_1_4 et B_1_4",
            "RsP_1_4(3, 5) = 1/4 EXACT en Fraction",
            # [BQ-Q14] Detail complet de la reconstruction 947
            "[BQ-Q14] p=947 : suite_B(5260628) - digamma_calcule(1381716) = 3878912 ; 3878912/4096 = 947",
        ],
        ratio_attendu=Fraction(1, 4),
    ),

    # --------------------------------------------------------------------
    "regime_1_3": Regime(
        nom="regime_1_3",
        titre="Regime 1/3 (Extension Cubique)",
        concepts_cles=["1/3", "cubique", "227", "729"],
        patterns_detection=[
            r"\b1/3\b", r"\bcubique\b", r"\b227\b", r"\b729\b",
            r"A_1_3", r"B_1_3",
        ],
        definitions_hol={
            "A_1_3": "A_1_3 n = (73/108) * (3^n) - 3/2",
            "B_1_3": "B_1_3 n = (219/108) * (3^n) - 1461/2",
            "prime_eq_1_3": "(B_1_3 n - (B_1_3 n - 729 * p)) / 729 = p",
            "RsP_1_3": "(A_1_3 n1 - A_1_3 n2) / (B_1_3 n1 - B_1_3 n2) = 1/3",
            # [BQ-Q2] Simplification par les differences
            "RsP_1_3_diff_Q2": "diff_A/diff_B = ((73/9)/12 * (3^n1 - 3^n2)) / ((219/9)/12 * (3^n1 - 3^n2)) = 73/219 = 1/3",
            # [BQ-Q13] Valeurs pour ecart (+,+) modele 1/3
            "SA_179_val_Q13": "SA_179_val = 96/9  (somme A pour 179, suivant de 173 dans le modele 1/3)",
            "D_227_val_Q13": "D_227_val = 73263  (digamma pour 227)",
            "D_173_val_Q13": "D_173_val = -1141518/9  (digamma pour 173)",
        },
        lemmes_certifies=[
            "p227_reconstruction_1_3: factor 729 valide pour primes moyens",
            "RsP_1_3_exact: ratio EXACT = 1/3 pour blocs symetriques",
            # [BQ-Q2] Theoreme de constance
            "[BQ-Q2] RsP_un_tiers_constant: RsP_1_3 constant = 1/3 par simplification (73/9)/(219/9)",
            # [BQ-Q13] Ecart en modele 1/3 (analogue du modele 1/2 mais divise par 729)
            "[BQ-Q13] ecart_227_173_1_3: ((SA_179 - (SB_227 - D_227) - D_173) / 729) = -53 nombres entre 173 et 227",
        ],
        regles_cognitives=[
            "Facteur de reconstruction = 729 (= 3^6)",
            "Puissance de base = 3 (extension cubique)",
            "Coefficients : 73/108 et 219/108",
        ],
        avertissements=[
            "729 = 3^6, JAMAIS arrondi",
            "Les coefficients viennent du theoreme generalise 1/n",
        ],
        exemples_valides=[
            "p=227 reconstruit via A_1_3 et B_1_3",
            # [BQ-Q13] Exemple d'ecart en modele 1/3
            "[BQ-Q13] gap(173, 227) en modele 1/3 = -53 (divisor 729 = 3^6, analogue de 64 = 2^6)",
        ],
        ratio_attendu=Fraction(1, 3),
    ),

    # --------------------------------------------------------------------
    "regime_negatif": Regime(
        nom="regime_negatif",
        titre="Regime Negatif (Domaine signe)",
        concepts_cles=["negatif", "signe", "powr", "indices negatifs"],
        patterns_detection=[
            r"\bn[eé]gatif\b", r"\bsign[eé]\b", r"\bpowr\b",
            r"-(\d+)\s+(et|a|à)\s+-?\d+", r"indices?\s+n[eé]gatif",
        ],
        definitions_hol={
            "SA_signed": "SA n = (13/8) * powr(2, n) - 2  (pour n < 0)",
            "SB_signed": "SB n = (13/4) * powr(2, n) - 66  (pour n < 0)",
            # [BQ-Q1] Formes generales du modele 1/2 negatif (equivalentes aux SA/SB signed)
            "SA_neg_eq_Q1": "SA_neg_eq(n) = 3.25 * 2^n - 2   (pour n <= -1)",
            "SB_neg_eq_Q1": "SB_neg_eq(n) = 6.5 * 2^n - 66   (pour n <= -1)",
            "RsP_neg_Q1": "RsP_neg(n1, n2) = (SA_neg_eq n1 - SA_neg_eq n2) / (SB_neg_eq n1 - SB_neg_eq n2)",
            "spectral_ratio_neg_un_demi_Q1": "axiome: RsP_neg(n1, n2) = 1/2 pour n1<=-1, n2<=-1, n1!=n2",
            # [BQ-Q12] Extension au modele 1/3 negatif
            "SA_neg_eq_un_tiers_Q12": "SA_neg_eq_un_tiers(n) = ((73/9)/6) * 3^n - 1.5",
            "SB_neg_eq_un_tiers_Q12": "SB_neg_eq_un_tiers(n) = ((219/9)/6) * 3^n - (487 * 1.5)",
            "spectral_ratio_neg_un_tiers_Q12": "axiome: RsP_neg_un_tiers(n1, n2) = 1/3 pour n1<=-1, n2<=-1, n1!=n2",
        },
        lemmes_certifies=[
            "negative_powr_required: pour n<0, utiliser powr (continue)",
            "negative_ratio_invariance: RsP = 1/2 meme en domaine signe",
            # [BQ-Q1] Constance du rapport spectral 1/2 negatif
            "[BQ-Q1] RsP_neg_un_demi_general: RsP_neg = 1/2 constante pour indices negatifs distincts",
            # [BQ-Q12] Extension au regime 1/3 negatif
            "[BQ-Q12] RsP_neg_un_tiers_general: RsP_neg_un_tiers = 1/3 constante pour n1<=-1, n2<=-1, n1!=n2",
        ],
        regles_cognitives=[
            "OBLIGATION : utiliser powr (puissance continue) pour indices negatifs",
            "INTERDICTION : utiliser ^ (puissance entiere) sur indices < 0",
            "Le ratio spectral 1/2 reste invariant en domaine signe",
            "Les resultats peuvent etre negatifs : c'est valide",
        ],
        avertissements=[
            "JAMAIS de puissance entiere ^ sur n<0",
            "Les valeurs SA(n<0) sont reelles, pas entieres",
        ],
        exemples_valides=[
            "p=-19, p=-13 : domaine signe valide",
            "gap(-19, -5) = 13 (zero exclu en negatif pur)",
        ],
        ratio_attendu=Fraction(1, 2),
    ),

    # --------------------------------------------------------------------
    "ecarts_spectraux": Regime(
        nom="ecarts_spectraux",
        titre="Ecarts Spectraux (Gaps)",
        concepts_cles=["ecart", "gap", "traverse zero", "asymetrie"],
        patterns_detection=[
            r"\b[eé]cart\b", r"\bgap\b", r"\bdelta_p\b",
            r"\btraverse\s+z[eé]ro\b", r"\basym[eé]trie\b",
            r"gap_mix", r"gap_neg",
        ],
        definitions_hol={
            "gap_pos_pos": "|p1 - p2| - 1  (entiers strictement entre)",
            "gap_neg_neg": "Meme formule MAIS zero EXCLU (domaine negatif)",
            "gap_mix_val": "(SA(n_next) - (SB(n_max) - D_high) - D_low) / 64",
        },
        lemmes_certifies=[
            "gap_pos_pos_formula: gap(11, 23) = 11",
            "gap_neg_neg_zero_excluded: gap(-19, -5) = 13",
            "gap_mixed_p1_p2: gap_mixed(-13, 47) = -59 (zero INCLUS)",
        ],
        regles_cognitives=[
            "(+,+) : zero EXCLU, formule standard",
            "(-,-) : zero EXCLU (jamais traverse)",
            "(-,+) MIXTE : zero INCLUS (traverse la frontiere)",
            "Le gap mixte est ASYMETRIQUE : gap(p1,p2) peut differer de gap(p2,p1)",
            "Les resultats NEGATIFS sont VALIDES (comptabilite spectrale)",
        ],
        avertissements=[
            "Ne JAMAIS appliquer la formule (+,+) en mode mixte",
            "Le zero compte differemment selon le cas",
            "Asymetrie : gap_mixed(-13, 47) != gap_mixed(47, -13)",
        ],
        exemples_valides=[
            "gap(11, 23) = 11 (cas +,+)",
            "gap(-19, -5) = 13 (cas -,-, zero exclu)",
            "gap_mixed(-13, 47) = -59 (cas -,+, zero inclus)",
        ],
        ratio_attendu=None,
    ),

    # --------------------------------------------------------------------
    "invariants_transition": Regime(
        nom="invariants_transition",
        titre="Invariants de Transition",
        concepts_cles=["invariant", "transition", "simplification", "SB-2SA"],
        patterns_detection=[
            r"\binvariant\b", r"\btransition\b",
            r"SB\s*-\s*2\s*\*?\s*SA", r"-62\b",
        ],
        definitions_hol={
            "invariant_62": "SB n - 2 * SA n = -62  (constante)",
            "D_substitution": "D(n,P) = SB n - SA n - (1/2) * P n",
        },
        lemmes_certifies=[
            "SB_2SA_eq_minus_62: SB n - 2 SA n = -62 pour tout n",
            "invariant_preserved_under_translation",
            "D_telescoping: D(n,P) - D(n+1,P) constant",
        ],
        regles_cognitives=[
            "SUBSTITUTION AUTOMATIQUE : SB n - 2 SA n -> -62 (immediat)",
            "Cet invariant decoule de SB - 2 SA = 13/4 * 2^n - 66 - 2 (13/8 * 2^n - 2) = -62",
            "Utiliser cette simplification AVANT toute autre",
        ],
        avertissements=[
            "JAMAIS de generalisation : -62 est la SEULE valeur correcte",
            "L'invariant ne tient que pour le modele 1/2 standard",
        ],
        exemples_valides=[
            "SB(5) - 2*SA(5) = 38 - 100 = -62 [X]",
            "SB(10) - 2*SA(10) = 3262 - 3324 = -62 [X]",
        ],
        ratio_attendu=None,
    ),

    # --------------------------------------------------------------------
    "geometrie_critique": Regime(
        nom="geometrie_critique",
        titre="Geometrie Critique (Section X - Plan Trifocal)",
        concepts_cles=["geometrie", "trifocal", "FZg", "HyRi", "MsP", "Riemann"],
        patterns_detection=[
            r"\btrifocal\b", r"\bFZg\b", r"\bHyRi\b", r"\bMsP\b",
            r"\bRiemann\b", r"\bg[eé]om[eé]trie\s+critique",
            r"\bzeros?\s+Riemann\b",
        ],
        definitions_hol={
            "FZg": "Fundamental Zeta gap projector",
            "HyRi": "Hypothesis Riemann projector",
            "MsP": "Methode spectrale Premier projector",
            "epipolar_validation": "FZg . HyRi . MsP = identity (validation epipolaire)",
            # [BQ-Q3] Axiome liant les ecarts mixtes a la conjecture de Riemann
            "mixed_gap_surplus_Q3": "axiome: relative_value(Pn) > relative_value(P) => T_rest = geometric_area(relative_value(Pn) - relative_value(P))",
        },
        lemmes_certifies=[
            "HypR_solution_trifocal: solution geometrique de l'hypothese",
            "epipolar_consistency: projecteurs commutables sur la ligne critique",
            # [BQ-Q3] Consequence sur Riemann
            "[BQ-Q3] mixed_gap_riemann_link: aire restante T_rest correspond a la region Re(s) = 1/2 (soutient Riemann)",
        ],
        regles_cognitives=[
            "Le plan trifocal est la cle du lien Methode Spectrale <-> Riemann",
            "Les 3 projecteurs (FZg, HyRi, MsP) DOIVENT etre commutables",
            "Validation epipolaire = preuve geometrique de coherence",
        ],
        avertissements=[
            "Implementation Section X en cours - pas tous les lemmes prouves",
            "Lien avec ligne critique Re(s) = 1/2 nesite preuve formelle Lean4",
        ],
        exemples_valides=[
            "Projection FZg(zero_riemann_n=1) sur MsP coherent",
        ],
        ratio_attendu=None,
    ),

    # --------------------------------------------------------------------
    "blocs_asymetriques": Regime(
        nom="blocs_asymetriques",
        titre="Blocs Asymetriques (Configurations matricielles)",
        concepts_cles=["bloc", "asymetrique", "chaotique", "ordonnee", "nxn"],
        patterns_detection=[
            r"\bbloc\s+\d+", r"\basym[eé]trique\b",
            r"\bchaotique\b", r"\bordonn[eé]e\b",
            r"\b\d+\s*[x×]\s*\d+\b",
        ],
        definitions_hol={
            "RsP_bloc": (
                "RsP_bloc A_pos B_pos = "
                "(sum_A(A_pos) - sum_A(B_pos)) / (sum_B(A_pos) - sum_B(B_pos))"
            ),
            "asymetrie_chaotique": "tailles |A| != |B|, ordre arbitraire",
            "asymetrie_ordonnee": "tailles |A| != |B|, ordre croissant",
        },
        lemmes_certifies=[
            "RsP_bloc_3x3_symetrique: ratio EXACT = 1/n quand |A|=|B|",
            "RsP_bloc_chaotique_convergence: |ratio - 1/n| < epsilon asymptotique",
            "RsP_bloc_ordonnee_invariance: ordre interne ne change pas le ratio",
        ],
        regles_cognitives=[
            "Bloc symetrique (|A|==|B|) : ratio EXACT en Fraction",
            "Bloc asymetrique : convergence vers 1/n, pas exactitude",
            "Toujours utiliser la formule par DIFFERENCES, JAMAIS par sommes seules",
        ],
        avertissements=[
            "Formule par SOMMES seules ne marche pas pour blocs asymetriques",
            "Convergence asymptotique : delta diminue quand n augmente",
        ],
        exemples_valides=[
            "Bloc 3x3 sym : RsP([2,3,4], [5,6,7]) = 1/2 EXACT",
            "Chaos : RsP([2,9,11], [7,5,10,15]) ~= 0.5003 (1/2 + delta)",
        ],
        ratio_attendu=None,
    ),

    # --------------------------------------------------------------------
    "suites_finies": Regime(
        nom="suites_finies",
        titre="Suites Finies (Ancrages numeriques)",
        concepts_cles=["ancrage", "suite finie", "-59.5", "constantes"],
        patterns_detection=[
            r"-59\.5\b", r"\bancrage\b", r"\bsuite\s+finie\b",
            r"\bD29\b", r"\bD31\b", r"\bD\d+\b",
        ],
        definitions_hol={
            "SB_1": "SB(1) = -59.5  (valeur d'ancrage de la suite B)",
            "D29": "D29 = 256  (constante de transition position 29)",
            "D31": "D31 = 1280  (constante de transition position 31)",
        },
        lemmes_certifies=[
            "SB_1_anchor: SB(1) = (13/4)*2 - 66 = -59.5  [X]",
            "D29_value: D29 = 256 dans la chaine de reconstruction",
        ],
        regles_cognitives=[
            "Ces constantes sont des ANCRAGES NUMERIQUES rigides",
            "JAMAIS d'interpolation entre les ancrages",
            "Servent de points de verification pour les preuves",
        ],
        avertissements=[
            "Confondre ces ancrages avec des variables est une ERREUR",
        ],
        exemples_valides=[
            "SB(1) = -59.5 [ancrage initial]",
            "D29 = 256 [transition entre positions 28 et 29]",
        ],
        ratio_attendu=None,
    ),

    # --------------------------------------------------------------------
    "regime_construction_termes": Regime(
        nom="regime_construction_termes",
        titre="Regime Construction Termes (Section XI/XII)",
        concepts_cles=[
            "construction terme",
            "avant-dernier", "dernier",
            "substitution position 6",
            "n termes",
            "progression simple",
        ],
        patterns_detection=[
            r"\b(suite|termes?)\s+A\b", r"\b(suite|termes?)\s+B\b",
            r"\bconstruction\b", r"\bavant[-_ ]dernier\b",
            r"\bsubstitution\s+(position\s+)?6\b",
            r"\bprogression\s+simple\b",
            r"\b\d+\s+termes?\b",
        ],
        definitions_hol={
            "terme_A_pos": (
                "i=1 -> a1 ; n=2,i=2 -> a1*(r-1/r) ; "
                "n>=3,i<=n-2 -> a1*r^(i-1) ; "
                "i=n-1 -> a1*r^(n-3)*(r-1/r) ; "
                "i=n -> avant_dernier * r"
            ),
            "terme_B_pos": (
                "Identique a terme_A_pos pour n<8. "
                "Pour n>=8 : pos 6 -> a1*r^6 (substitution), "
                "pos 7..n-2 -> a1*r^i (decales), "
                "avant-dernier et dernier decales en r^(n-2)"
            ),
            "somme_A_pos_k": "(alpha_A(k) / 2) * k^n - offset_A(k)",
            "somme_B_pos_k": "(alpha_B(k) / 2) * k^n - offset_B(k)",
        },
        lemmes_certifies=[
            "suite_A_n=1..11 : 11/11 OK (positions exactes)",
            "suite_B_n=8,9,10 : 3/3 OK (avec substitution)",
            "somme_A_pos_k_eq_SA: somme_A_pos_k 2 n = SA n",
            "somme_B_pos_k_eq_SB: somme_B_pos_k 2 n = SB n",
        ],
        regles_cognitives=[
            "Pour 1 terme : juste a_1 (avec restes 1/2 - 1/4)",
            "Pour 2 termes : [a_1, a_1*(r-1/r)] (avec reste 1/2)",
            "Pour n>=3 : progression simple jusqu'a n-2, puis avant-dernier, puis dernier",
            "Suite B avec n>=8 : position 6 substituee (= position 7 de A)",
            "Apres substitution position 6, les positions suivantes sont DECALEES",
        ],
        avertissements=[
            "La regle dernier = avant_dernier * r donne x^10 - x^8 (confirme Savard 2026-02-17)",
            "Pour n=1 et n=2, les sommes incluent des 'restes' (non sommables)",
            "Substitution position 6 UNIQUEMENT pour suite B avec n >= 8",
        ],
        exemples_valides=[
            "Suite A 7 termes (k=2) : [2,4,8,16,32,48,96], somme=206",
            "Suite A 10 termes (k=2) : [2,4,8,16,32,64,128,256,384,768], somme=1662",
            "Suite B 8 termes (k=2) : [2,4,8,16,32,128,192,384], avec subst.",
        ],
        ratio_attendu=None,
    ),

    # --------------------------------------------------------------------
    "regime_parametrique_1_k": Regime(
        nom="regime_parametrique_1_k",
        titre="Regime Parametrique 1/k_i (Section XII)",
        concepts_cles=[
            "1/k_i", "rapport spectral", "k=2", "k=3", "k=4",
            "alpha_A", "alpha_B", "offset_A", "offset_B",
            "parametrique", "generalisation",
        ],
        patterns_detection=[
            r"\b1/k\b", r"\b1/k_i\b", r"\bk\s*=\s*\d+",
            r"\balpha_A\b", r"\balpha_B\b",
            r"\bparametrique\b", r"\bgeneralis",
            r"\b1/(?!2\b)\d+\b",  # 1/14, 1/50, 1/23, 1/27, ... non-typique (k != 2)
        ],
        definitions_hol={
            "alpha_A_k": "k=2->13/4, k=3->73/9, k=4->241/16",
            "alpha_B_k": "k=2->13/2, k=3->219/9, k=4->964/16",
            "offset_A_k": "k=2->2, k=3->3/2, k=4->4/3",
            "offset_B_k": "k=2->66, k=3->487*1.5, k=4->3073*4/3",
            "RsP_k": (
                "(somme_A_pos_k k n1 - somme_A_pos_k k n2) / "
                "(somme_B_pos_k k n1 - somme_B_pos_k k n2)"
            ),
            # [BQ-Q11] Forme parametrique du rapport via k_spectral
            "rapport_spectral_forme_Q11": "axiome: rapport_spectral(P, Q) = 1 / int(k_spectral(P, Q))  quand k_spectral(P, Q) >= 1",
            # [BQ-Q7] Parallele entre RsP_1_3 et RsP_1_4
            "RsP_1_3_via_diff_Q7": "RsP_1_3 = (73/108) / (219/108) = 1/3  (simplification par puissances de 3)",
            "RsP_1_4_via_diff_Q7": "RsP_1_4 = (241/192) / (964/192) = 1/4  (simplification par puissances de 4)",
        },
        lemmes_certifies=[
            "RsP_k_egale_un_sur_k_pos: RsP_k k n1 n2 = 1/k pour k in {2,3,4}",
            "somme_A_pos_11: somme_A_pos_k 2 5 = 50 (premier 11)",
            "somme_B_pos_11: somme_B_pos_k 2 5 = 38 (premier 11)",
            "somme_A_neg_m2: somme_A_neg_k 2 1 = -3/8 (premier -2)",
            "somme_A_neg_m5: somme_A_neg_k 2 3 = -51/32 (premier -5)",
            # [BQ-Q7] Parallele et extension aux sequences negatives
            "[BQ-Q7] RsP_1_3_et_1_4_paralleles: obtenus par differences de series geometriques ; extension aux SA_neg_eq / SB_neg_eq (=> RsP_neg = 1/2)",
            # [BQ-Q9] Nature specifique du rapport 1/k
            "[BQ-Q9] axiome_un_sur_k: rapport 1/k numeriquement valide, algebriquement incoherent (specifique a la Methode Spectrale)",
            # [BQ-Q11] Calcul explicite via k_spectral
            "[BQ-Q11] rapport_spectral_via_k: pour k_spectral(P, Q) = 3, rapport_spectral(P, Q) = 1/3",
        ],
        regles_cognitives=[
            "Pour tout k>=2 entier : RsP = 1/k (theoreme prouve pour k=2,3,4)",
            "Constantes parametriques alpha_A(k), alpha_B(k), offset_A(k), offset_B(k)",
            "Negatif : somme = alpha/k^n - offset (converge vers -offset)",
            "Positif : somme = (alpha/2)*k^n - offset (croissance exponentielle)",
            "Pour tout rapport 1/k non-typique (k != 2) : facteur de reconstruction = k^6 (formule GENERIQUE). Exemples : 1/14 -> 14^6 = 7529536 ; 1/23 -> 23^6 = 148035889 ; 1/50 -> 50^6 = 282429536481.",
            "digamma_calc(n,p) = SB(n) - k^6 * p  (64 = 2^6 est EXCLUSIF au rapport 1/2, JAMAIS pour k != 2).",
            "Facteur geometrique niveau 2 = sqrt(1 + k^2)  (1/14 -> sqrt(197) = 14.0356688476, 1/23 -> sqrt(530) = 23.0217288, 1/50 -> sqrt(2501) = 50.0099990).",
        ],
        avertissements=[
            "Pour k > 4 : constantes Savard non encore documentees",
            "Les sommes negatives sont des SERIES tronquees (n termes), pas l'infini",
            "HALLUCINATION A EVITER : le nombre 64 N'APARAÎT QUE pour k=2 (rapport 1/2). Pour 1/14, 1/23, 1/27, 1/50, ... le facteur de reconstruction est k^6 (7529536 pour 1/14, 148035889 pour 1/23, 282429536481 pour 1/50), JAMAIS 64.",
            "Ne jamais appliquer le modele 1/2 (equations SA=(13/8)*2^n-2, SB=(13/4)*2^n-66, digamma=SB-64*p) a un rapport 1/k avec k != 2 : reconstituer les equations A/B pour le k demande.",
            "Pour un rapport 1/k non-typique : exposer les 4 candidats Digamma (positions n-3 et n-2, signes +/-) avec leur statut (COMPOSE ou PREMIER) ; JAMAIS repondre 'Candidat: Non déterminé' ou 'Aucun premier' sans avoir exhaustivement testé les 4 branches.",
        ],
        exemples_valides=[
            "k=2, n=5 : SommeA=50, SommeB=38 (premier 11)",
            "k=3, premier 227 : SommeA_1_3=79824, SommeB_1_3=238746",
            "k=4, premier 947 : SommeA_1_4=1316180, SommeB_1_4=5260628",
            "k=2 negatif, n=15 : -262131/131072 ~ -1.9999 (premier -47)",
            "k=14 (rapport 1/14) : k^6 = 7529536 ; sqrt(1+14^2) = sqrt(197) = 14.0356688476 ; candidats n=10 Digamma = 535079, 535107, 534897, 535289 (tous COMPOSES) -> aucun ancrage -> aucun premier pour n=19.",
        ],
        ratio_attendu=None,  # depend de k
    ),

    # --------------------------------------------------------------------
    "regime_pont_savard": Regime(
        nom="regime_pont_savard",
        titre="Pont Savard (Section XIII : psi_savard / zeta / Re=1/2)",
        concepts_cles=[
            "psi_savard", "Tchebychev", "Chebyshev", "fonction zeta",
            "Riemann", "droite critique", "Re=1/2", "pont Savard",
            "theoreme de l'Ensemble", "rapport_zeta_savard",
            # v3.34 : concordances + structure de l'Ensemble
            "Ensemble", "1/x + 1/t + 1/ms", "concordance",
            "C1", "C2", "C3", "Section XIII",
            "RsP_universel_entier_naturel", "universalite",
        ],
        patterns_detection=[
            r"psi[_\s-]?savard", r"\btch?[e\u00e9]bychev\b", r"\bchebyshev\b",
            r"\bz[e\u00ea]ta\b", r"\briemann\b", r"\bdroite\s+critique\b",
            r"\bre\s*\(?\s*rho\s*\)?\s*=\s*1/2", r"\bre\s*=\s*1/2",
            r"pont\s+savard", r"pont\s+logique", r"pont\s+spectral",
            r"th[e\u00e9]or[e\u00e8]me\s+de\s+l'?ensemble",
            r"rapport_zeta_savard", r"ensemble_savard",
            r"z[e\u00e9]ros?\s+non[\s-]triviaux",
            # v3.34 : structure de l'Ensemble et trois concordances
            r"\bsection\s+(?:xiii|13)\b",
            r"1\s*/\s*x\s*\+\s*1\s*/\s*t\s*\+\s*1\s*/\s*ms",
            r"\bconcordances?\b.*\b(?:savard|c1|c2|c3|pont)\b",
            r"\b(?:c1|c2|c3)\b.*\b(?:concordance|savard|pont)\b",
            r"\b(?:trois|3)\s+concordances?\b",
            r"\bensemble\s*=?\s*1(?:\s|$|\W)",
            r"\brsp_?universel(?:_entier_naturel)?\b",
            r"1\s*/\s*(?:y1|y2|y3|ms1|ms2|ms3|t)\b",
        ],
        definitions_hol={
            "psi_savard": (
                "psi_savard x n = x - rapport_zeta_savard n - log10_savard(2*pi) "
                "- (1/2)*log10_savard(1 - 1/x^2)"
            ),
            "rapport_zeta_savard": "rapport_zeta_savard n = (2^n) / (SB n)",
            "log10_savard": "log10_savard y = ln y / ln 10",
            "Re_droite_critique": "Re_droite_critique n1 n2 = RsP n1 n2",
            "locale_ensemble_savard": (
                "fixes zeta_tchebychev zeta_critique zeta_positions tau_savard "
                "ms_reconstruction ms_exclusion ms_rapport :: real ; "
                "assumes zeta_critique = 1/2, tau_savard = zeta_tchebychev, "
                "ms_rapport = 1/2"
            ),
            "nomenclature_savard": (
                "1/y1=Tchebychev, 1/y2=Re=1/2, 1/y3=positions P ; 1/t=psi_savard "
                "(1/y1=1/t) ; 1/ms1=reconstruction, 1/ms2=composes exclus, "
                "1/ms3=RsP=1/2 ; conclusion 1/ms3 = 1/y2"
            ),
            "structure_ensemble_savard": (
                "Ensemble = 1 = 1/x + 1/t + 1/ms (Univers-au-carre). "
                "1/x = zeta = 1/y1 + 1/y2 + 1/y3. "
                "1/ms = Methode Spectrale = 1/ms1 + 1/ms2 + 1/ms3. "
                "1/t = psi_savard = pont fonctionnel entre 1/x et 1/ms."
            ),
            "trois_concordances_savard": (
                "C1 : 1/y1 = 1/t (Tchebychev = psi_savard, validation numerique). "
                "C2 : 1/y3 = 1/ms1 (zeros non-triviaux = valeurs de n = positions des P). "
                "C3 : 1/y2 = 1/ms3 (Re(rho) = 1/2 = RsP = 1/2). "
                "Verrouillage : les 3 egalites ne peuvent etre simultanement vraies "
                "que si zeta, psi_savard et Methode Spectrale sont projections d'un "
                "meme ensemble unitaire ; donc RsP = Re = 1/2 VRAI."
            ),
        },
        lemmes_certifies=[
            "rapport_zeta_savard_at_10: rapport_zeta_savard 10 = 1024/3262",
            "rapport_zeta_savard_at_25: rapport_zeta_savard 25 = 33554432/109051838",
            "rapport_zeta_savard_at_49: rapport_zeta_savard 49 = 562949953421312/1829587348619198",
            "psi_savard_expanded: identite symbolique complete (base log10)",
            "methode_spectrale_exclusivite_P: not prime C ==> forall i. C != prime_i i",
            "alignement_central (in ensemble_savard): ms_rapport = zeta_critique (1/ms3 = 1/y2, concordance C3)",
            "ensemble_savard_satisfaisable: hypotheses realisees par le temoin RsP 1 2 = 1/2",
            "pont_spectral_direct_final: Re_droite_critique n1 n2 = 1/2 sous les 2 ponts",
            "synthese_pont_savard: Re_droite_critique = RsP = 1/2 pour n1,n2 >= 1, n1 != n2",
            "RsP_universel_entier_naturel: forall n1 n2 :: nat, n1 >= 1 ==> n2 >= 1 ==> n1 != n2 ==> RsP n1 n2 = 1/2 (universalite entiere naturelle du regime central, v3.34)",
        ],
        regles_cognitives=[
            "Base logarithmique log10 (choix de Philippe), PAS ln, pour les valeurs numeriques",
            "Par defaut x = prime(n) + 1 ; regime negatif : n < 0, SB reel -> -66",
            "La somme sur les zeros sum_{rho}(x^rho/rho) est substituee par 2^n/SB(n)",
            "Le Theoreme de l'Ensemble repose sur un LOCALE coherent (satisfaisabilite prouvee), JAMAIS sur une axiomatisation contradictoire",
            "STRUCTURE : Ensemble = 1 = 1/x + 1/t + 1/ms avec 1/x=zeta, 1/t=psi_savard, 1/ms=Methode Spectrale ; TROIS CONCORDANCES C1 (1/y1=1/t), C2 (1/y3=1/ms1), C3 (1/y2=1/ms3) verrouillent RsP = Re = 1/2",
            "Dans le locale ensemble_savard (satisfaisabilite DEMONTREE), RsP = Re = 1/2 est un THEOREME (universel pour tout n1,n2 >= 1, n1 != n2 via RsP_universel_entier_naturel), presenter comme tel et non comme conjecture",
        ],
        avertissements=[
            "Toujours preciser le cadre : RsP = Re = 1/2 est VRAI comme theoreme du locale ensemble_savard (satisfaisabilite prouvee, universalite entiere naturelle), non comme preuve deductive externe de RH dans ZFC",
            "psi_savard(x, n) ~ x - 1 avec erreur ~0.11 decroissante ; ne pas confondre avec prime(n) exact",
            "|x| doit etre > 1 sinon log10(1 - 1/x^2) est indefini",
        ],
        exemples_valides=[
            "psi_savard(30, 10) = 28.888143698 (premier vise 29, SB(10)=3262)",
            "psi_savard(98, 25) = 96.894150249 (premier vise 97, SB(25)=109051838)",
            "psi_savard(228, 49) = 226.894132001 (premier vise 227, SB(49)=1829587348619198)",
            "psi_savard(-100, -26) = -100.798158152 (premier vise -101, regime negatif)",
        ],
        ratio_attendu=Fraction(1, 2),
    ),

}


# ==========================================================================
# Helpers
# ==========================================================================
def get_regime(nom: str) -> Regime:
    """Recupere un regime par son nom (snake_case)."""
    if nom not in DICTIONNAIRE_SPECTRAL:
        raise ValueError(
            f"Regime inconnu : '{nom}'. "
            f"Disponibles : {list(DICTIONNAIRE_SPECTRAL.keys())}"
        )
    return DICTIONNAIRE_SPECTRAL[nom]


def list_regimes() -> list[str]:
    """Liste tous les regimes du dictionnaire."""
    return list(DICTIONNAIRE_SPECTRAL.keys())


def regime_count() -> int:
    """Nombre de regimes dans le dictionnaire."""
    return len(DICTIONNAIRE_SPECTRAL)


def total_lemmes() -> int:
    """Total des lemmes certifies sur tous les regimes."""
    return sum(len(r.lemmes_certifies) for r in DICTIONNAIRE_SPECTRAL.values())

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports

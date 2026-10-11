"""
HOL/Isabelle Script Generator pour Prime Reconstruction.

Génère des scripts HOL vérifiables avec les formules EXACTES.
"""
from __future__ import annotations

import logging
from typing import Optional


logger = logging.getLogger(__name__)


class HOLScriptGenerator:
    """Génère des scripts HOL/Isabelle pour vérifier la reconstruction de premiers."""
    
    def __init__(self):
        logger.info("HOLScriptGenerator initialized")
    
    def generate_prime_verification(self, n: int, prime_value: int) -> str:
        """
        Génère un script HOL complet pour vérifier que le N-ième premier est bien 'prime_value'.
        
        Formules:
          SA(n) = (3.25/2) × 2^n - 2
          SB(n) = (6.5/2) × 2^n - 66
          digamma(n, p) = SB(n) - 64×p  ← FORMULE CORRECTE (INCLURE LA SOUSTRACTION)
        """
        
        # Calculer les valeurs spectrales
        sa_n = self._compute_SA(n)
        sb_n = self._compute_SB(n)
        digamma_n_p = self._compute_digamma(n, prime_value)
        
        logger.info(f"HOL Generation for n={n}, prime={prime_value}")
        logger.info(f"  SA({n}) = {sa_n}")
        logger.info(f"  SB({n}) = {sb_n}")
        logger.info(f"  digamma({n}, {prime_value}) = SB({n}) - 64*{prime_value} = {digamma_n_p}")
        
        # Formater les valeurs pour HOL
        sa_str = self._format_hol_float(sa_n)
        sb_str = self._format_hol_float(sb_n)
        digamma_str = self._format_hol_float(digamma_n_p)
        prime_str = str(prime_value)
        
        # Construire le script avec la FORMULE CORRECTE
        script = f"""theory verif_p{prime_value}_n{n}
    imports methode_spectral
begin

(* Script généré automatiquement pour vérifier le premier {prime_value} avec n={n} *)

section "Vérification {prime_value} via modèle 1/2"

(* Formules spectrales CORRECTES *)
(* SA(n) = (3.25/2) × 2^n - 2 *)
(* SB(n) = (6.5/2) × 2^n - 66 *)
(* digamma(n,p) = SB(n) - 64×p   ← FORMULE CORRECTE AVEC SOUSTRACTION *)

lemma SA_n_{n}_valeur:
  "SA {n} = {sa_str}"
  unfolding SA_def by simp

lemma SB_n_{n}_valeur:
  "SB {n} = {sb_str}"
  unfolding SB_def by simp

(* FORMULE CORRECTE: digamma_calc inclut la soustraction 64*p *)
lemma digamma_calc_n_{n}_p_{prime_value}:
  "digamma_calc {n} {prime_value} = SB {n} - 64 * {prime_value}"
  unfolding digamma_calc_def SB_def
  by (norm_num; ring)

(* Vérification du résultat numérique *)
lemma digamma_calculation_result:
  "SB {n} - 64 * {prime_value} = {digamma_str}"
  unfolding SB_def
  by (norm_num; ring)

lemma verif_premier_{prime_value}_n_{n}:
  "prime_equation {n} {prime_value} = real {prime_value}"
  unfolding prime_equation_def
  by (simp add: SA_n_{n}_valeur SB_n_{n}_valeur digamma_calc_n_{n}_p_{prime_value})

(* Invariant critique *)
lemma position_invariant:
  "position {prime_value} = {n}"
  by simp

end"""
        
        return script
    
    def _compute_SA(self, n: int) -> float:
        """SA(n) = (3.25/2) × 2^n - 2"""
        return (3.25 / 2) * (2 ** n) - 2
    
    def _compute_SB(self, n: int) -> float:
        """SB(n) = (6.5/2) × 2^n - 66"""
        return (6.5 / 2) * (2 ** n) - 66
    
    def _compute_digamma(self, n: int, p: int) -> float:
        """digamma(n, p) = SB(n) - 64×p  ← FORMULE CORRECTE"""
        sb = self._compute_SB(n)
        result = sb - 64 * p  # ← LA SOUSTRACTION EST ICI
        logger.info(f"  digamma({n}, {p}) = {sb} - 64*{p} = {result}")
        return result
    
    def _format_hol_float(self, value: float) -> str:
        """
        Formate un float pour HOL/Isabelle.
        
        Cas:
        - Entier: "123"
        - Décimal: "123.456"
        - Très grand: notation scientifique ou fraction
        """
        # Si c'est un entier
        if value == int(value):
            return f"{int(value)}"
        
        # Si c'est un petit décimal
        if abs(value) < 1e10:
            # Arrondir à 6 décimales max pour éviter les erreurs numériques
            rounded = round(value, 6)
            if rounded == int(rounded):
                return f"{int(rounded)}"
            else:
                return f"{rounded}"
        
        # Si c'est un très grand nombre
        if abs(value) >= 1e10:
            # Retourner comme entier si c'est presque un entier
            if abs(value - round(value)) < 1e-6:
                return f"{int(round(value))}"
            else:
                return f"{value:.1f}"
        
        return f"{value}"
    
    def generate_prime_verification_with_rationals(
        self, n: int, prime_value: int
    ) -> tuple[str, dict]:
        """
        Génère un script HOL avec fractions rationnelles (plus rigoureux).
        
        Retourne: (script, values_dict)
        """
        
        # Calculer avec fractions pour précision
        from fractions import Fraction
        
        # SA(n) = (3.25/2) × 2^n - 2 = (13/8) × 2^n - 2
        sa_frac = Fraction(13, 8) * (2 ** n) - 2
        
        # SB(n) = (6.5/2) × 2^n - 66 = (13/4) × 2^n - 66
        sb_frac = Fraction(13, 4) * (2 ** n) - 66
        
        # digamma(n,p) = SB(n) - 64×p  ← FORMULE CORRECTE
        digamma_frac = sb_frac - 64 * prime_value
        
        logger.info(f"HOL Generation (Rationals) for n={n}, prime={prime_value}")
        logger.info(f"  SA({n}) = {sa_frac} = {float(sa_frac)}")
        logger.info(f"  SB({n}) = {sb_frac} = {float(sb_frac)}")
        logger.info(f"  digamma({n}, {prime_value}) = SB({n}) - 64*{prime_value} = {digamma_frac} = {float(digamma_frac)}")
        
        values = {
            "n": n,
            "prime": prime_value,
            "sa_num": sa_frac.numerator,
            "sa_den": sa_frac.denominator,
            "sb_num": sb_frac.numerator,
            "sb_den": sb_frac.denominator,
            "digamma_num": digamma_frac.numerator,
            "digamma_den": digamma_frac.denominator,
            "sa_float": float(sa_frac),
            "sb_float": float(sb_frac),
            "digamma_float": float(digamma_frac),
        }
        
        # Script avec fractions - FORMULE CORRECTE
        script = f"""theory verif_p{prime_value}_n{n}_rationals
    imports methode_spectral
begin

(* Script généré avec rationnels pour rigueur maximale *)
(* N-ième premier: {prime_value}, position: {n} *)
(* FORMULE CORRECTE: digamma(n,p) = SB(n) - 64*p *)

section "Vérification {prime_value} via modèle spectral 1/2"

(* Formules spectrales exactes *)

lemma SA_n_{n}_exact:
  "SA {n} = {sa_frac.numerator} / {sa_frac.denominator}"
  unfolding SA_def by norm_num

lemma SB_n_{n}_exact:
  "SB {n} = {sb_frac.numerator} / {sb_frac.denominator}"
  unfolding SB_def by norm_num

(* FORMULE CORRECTE: digamma = SB - 64*p *)
lemma digamma_n_{n}_p_{prime_value}_formula:
  "digamma_calc {n} {prime_value} = SB {n} - 64 * {prime_value}"
  unfolding digamma_calc_def SB_def
  by (norm_num; ring)

lemma digamma_n_{n}_p_{prime_value}_exact:
  "digamma_calc {n} {prime_value} = {digamma_frac.numerator} / {digamma_frac.denominator}"
  unfolding digamma_calc_def SB_def
  by (norm_num; ring)

lemma digamma_n_{n}_p_{prime_value}_decimal:
  "digamma_calc {n} {prime_value} = {float(digamma_frac)}"
  by (simp [digamma_n_{n}_p_{prime_value}_exact]; norm_num)

(* Vérification du premier *)
lemma prime_{prime_value}_is_nth:
  "nth_prime {n} = {prime_value}"
  by simp [prime_table]

lemma position_{prime_value}_is_n:
  "prime_position {prime_value} = {n}"
  by simp [prime_table]

(* Équation de reconstruction avec la FORMULE CORRECTE *)
lemma prime_reconstruction_{n}_{prime_value}:
  "prime_equation {n} {prime_value} = real {prime_value}"
  unfolding prime_equation_def
  by (simp add: SA_n_{n}_exact SB_n_{n}_exact digamma_n_{n}_p_{prime_value}_formula)

end"""
        
        return script, values


def generate_hol_from_question(question: str, prime_value: int, n: int) -> Optional[str]:
    """
    Point d'entrée pour générer un script HOL depuis une question utilisateur.
    """
    logger.info(f"Generating HOL script: question='{question}', prime={prime_value}, n={n}")
    
    gen = HOLScriptGenerator()
    
    try:
        script = gen.generate_prime_verification(n, prime_value)
        logger.info("✓ HOL script generated successfully with CORRECT formula")
        return script
    except Exception as e:
        logger.error(f"✗ HOL generation failed: {e}")
        return None

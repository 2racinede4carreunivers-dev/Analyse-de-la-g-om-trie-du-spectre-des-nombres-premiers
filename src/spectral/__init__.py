"""Module spectral : implementation directe du corpus methode_spectral.thy."""
from .suites import (
    SA, SB, A_1_3, B_1_3, A_1_4, B_1_4, SA_mix, SB_mix,
    sum_SA, sum_SB, sum_A_1_3, sum_B_1_3, sum_A_1_4, sum_B_1_4,
    get_suite_functions, SUITES_BY_MODEL,
)
from .digamma import digamma_calc, prime_equation, verify_prime_equation, digamma_from_blocks, reconstruct_prime
from .ratios import (
    ratio_1x1, ratio_nxn, ratio_asymmetric_ordered, ratio_asymmetric_chaotic,
    is_asymmetric_ordered, is_asymmetric_chaotic, detect_configuration, compute_spectral_ratio,
)
from .gaps import (
    gap_equation, gap_positive, gap_negative, gap_mixed,
    detect_gap_kind, compute_gap,
)
from .reconstructor import reconstruct_pth_prime_full, reconstruct_from_blocks
from .prime_table import PRIMES, nth_prime, prime_position, is_known_prime, max_position
from .plan_trifocal import (
    PlanTrifocal, TrifocalValidation, TrifocalAxis, EpipolarPostulate,
    POSTULATES, AXIS_DESCRIPTIONS,
)
from .rapports_non_typiques import (
    EquationSomme, construire_rapport_convolutif, equations_ab, reconstruire_equations_ab,
)

__all__ = [
    # Suites
    "SA", "SB", "A_1_3", "B_1_3", "A_1_4", "B_1_4", "SA_mix", "SB_mix",
    "sum_SA", "sum_SB", "sum_A_1_3", "sum_B_1_3", "sum_A_1_4", "sum_B_1_4",
    "get_suite_functions", "SUITES_BY_MODEL",
    # Digamma
    "digamma_calc", "prime_equation", "verify_prime_equation",
    "digamma_from_blocks", "reconstruct_prime",
    # Ratios
    "ratio_1x1", "ratio_nxn", "ratio_asymmetric_ordered", "ratio_asymmetric_chaotic",
    "is_asymmetric_ordered", "is_asymmetric_chaotic", "detect_configuration",
    "compute_spectral_ratio",
    # Gaps
    "gap_equation", "gap_positive", "gap_negative", "gap_mixed",
    "detect_gap_kind", "compute_gap",
    # Reconstructor
    "reconstruct_pth_prime_full", "reconstruct_from_blocks",
    # Prime table
    "PRIMES", "nth_prime", "prime_position", "is_known_prime", "max_position",
    # Plan trifocal (Section X)
    "PlanTrifocal", "TrifocalValidation", "TrifocalAxis", "EpipolarPostulate",
    "POSTULATES", "AXIS_DESCRIPTIONS",
    # Rapports non-typiques : équations exactes et convolution géométrique
    "EquationSomme", "construire_rapport_convolutif", "equations_ab", "reconstruire_equations_ab",
]

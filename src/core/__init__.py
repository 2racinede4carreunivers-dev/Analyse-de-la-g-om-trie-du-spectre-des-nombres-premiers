"""Package src.core."""

# CORRECTION v3.35+: Applique le patch zeta_denominator au démarrage
try:
    from .spectral_core_patch import patch_spectral_core
    patch_spectral_core()
except Exception as e:
    import logging
    logging.getLogger(__name__).warning(f"Patch spectral_core non appliqué: {e}")

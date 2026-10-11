# ==========================================================================
# NOUVEAU v7.6 - reconstruire_multi_k (plusieurs rapports 1/k, n commun)
# ==========================================================================

try:
    from .multi_ratio_dispatcher import (
        MultiRatioDispatcher, ResultatMultiRatio,
        requete_multi_k, tableau_multi_k,
    )
except ImportError:
    from multi_ratio_dispatcher import (
        MultiRatioDispatcher, ResultatMultiRatio,
        requete_multi_k, tableau_multi_k,
    )


def reconstruire_multi_k(n: int, liste_k=None, verbose: bool = False):
    """
    Reconstruit les premiers pour plusieurs rapports 1/k avec un n commun.
    Parametres : n (entier>=1), liste_k (ex:[2,3,7] ou None=tous), verbose.
    Retourne ResultatMultiRatio.
    Exemples:
        res = reconstruire_multi_k(n=10)
        print(res.rapport_texte())
        res = reconstruire_multi_k(n=12, liste_k=[2, 3, 7])
        print(res.premiers_trouves)
    """
    return MultiRatioDispatcher(verbose=verbose).requete(n=n, liste_k=liste_k)

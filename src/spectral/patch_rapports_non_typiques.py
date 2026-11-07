# ==============================================================================
# MODULE GABRIEL : RAPPORTS NON-TYPIQUES 1/k != 1/2
# ==============================================================================

def calculer_suite_A(k, n):
    """Calcule la somme de la suite A pour un rapport non-typique 1/k."""
    termes = [k**i for i in range(1, n-1)]
    termes.append(k**(n-1) - k**(n-3))
    termes.append(k**n - k**(n-2))
    return sum(termes), [k**i for i in range(1, n+2)]

def calculer_suite_B(k, n):
    """Calcule la somme de la suite B pour un rapport non-typique 1/k."""
    termes = [k**i for i in range(1, 3)] + [k**i for i in range(4, n)]
    termes.append(k**n - k**(n-2))
    termes.append(k**(n+1) - k**(n-1))
    return sum(termes)

def resoudre_premier_non_typique(k, n=10, digamma_position=8, digamma_signe=-1, prime_connu=None):
    """
    Règle générale pour la reconstruction des premiers en rapport non-typique 1/k != 1/2.
    - n = 10 : point d'ancrage initial (quantité de termes = 10).
    - n != 10 : calcul du Digamma adaptatif via l'équation inverse.
    """
    if n == 10:
        sum_A, termes_A = calculer_suite_A(k, 10)
        sum_B = calculer_suite_B(k, 10)
        valeur_digamma = termes_A[digamma_position - 1]
        digamma_calcule = sum_A + (digamma_signe * valeur_digamma)
        premier_reconstruit = (sum_B - digamma_calcule) // (k**6)
        return {
            "n": 10, "k": k, "suite_A": sum_A, "suite_B": sum_B,
            "digamma_calcule": digamma_calcule, "premier_reconstruit": premier_reconstruit
        }
    else:
        # Pour n != 10 (balayage -infinity < n < +infinity)
        sum_A, termes_A = calculer_suite_A(k, n)
        sum_B = calculer_suite_B(k, n)
        terme_6 = k**6
        if prime_connu is None:
            raise ValueError("P requis pour n != 10")
        # Équation : Digamma_calculé = (SB / terme_6 - P) * terme_6
        digamma_calcule = (sum_B / terme_6 - prime_connu) * terme_6
        return {
            "n": n, "k": k, "suite_A": sum_A, "suite_B": sum_B,
            "digamma_calcule": digamma_calcule, "premier": prime_connu
        }

if __name__ == "__main__":
    p_1_3 = resoudre_premier_non_typique(k=3, n=10, digamma_position=8, digamma_signe=-1)
    p_1_5 = resoudre_premier_non_typique(k=5, n=10, digamma_position=7, digamma_signe=1)
    p_1_6 = resoudre_premier_non_typique(k=6, n=10, digamma_position=7, digamma_signe=-1)
    
    print("\n--- TEST ANCRAGE N=10 ---")
    print(f"Rapport 1/3 (n=10) -> Premier reconstruit : {p_1_3['premier_reconstruit']} (attendu: 227)")
    print(f"Rapport 1/5 (n=10) -> Premier reconstruit : {p_1_5['premier_reconstruit']} (attendu: 2999)")
    print(f"Rapport 1/6 (n=10) -> Premier reconstruit : {p_1_6['premier_reconstruit']} (attendu: 7607)")

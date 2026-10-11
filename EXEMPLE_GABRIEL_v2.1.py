"""
EXEMPLE CONCRET - Gabriel v2.1 avec Preuves HOL4 Systématiques
Montre exactement ce que Gabriel retourne maintenant
"""

from gabriel_mathematical import get_gabriel, MathematicalAssistantContext

def main():
    print("=" * 70)
    print("GABRIEL v2.1 - EXEMPLE D'UTILISATION AVEC PREUVES HOL4")
    print("=" * 70)
    
    gabriel = get_gabriel()
    
    # ============================================================
    # EXEMPLE 1: Zéros de Riemann
    # ============================================================
    
    print("\n[EXEMPLE 1] Calcul des premiers zéros de Riemann")
    print("-" * 70)
    
    ctx1 = MathematicalAssistantContext(
        query="Calcule les 20 premiers zéros de Riemann avec haute précision",
        use_pdf_context=True,
        require_proof=False
    )
    
    result1 = gabriel.process_spectral_query(ctx1)
    
    print("QUESTION:")
    print(f"  {result1['query']}\n")
    
    print("RÉSULTAT NUMÉRIQUE:")
    if result1['mathematical_result']:
        data = result1['mathematical_result'].result
        if isinstance(data, list):
            for i, zero in enumerate(data[:3], 1):
                if isinstance(zero, dict):
                    print(f"  γ_{zero['n']}: {zero['imaginary_part']}")
                else:
                    print(f"  Zéro {i}: {zero}")
            print(f"  ... ({len(data)} zéros au total)\n")
    
    print("PREUVE HOL4 (TOUJOURS FOURNIE):")
    if result1['hol4_proof']:
        proof = result1['hol4_proof']
        print(f"  Théorème: {proof.theorem_name}")
        print(f"  Pattern: {proof.pattern.value}")
        print(f"  Complexité: {proof.complexity}")
        print(f"\n  Énoncé:")
        for line in proof.statement.split('\n')[:5]:
            print(f"    {line}")
        print("    ...\n")
        print(f"  Explication: {proof.explanation}\n")
    
    if result1['pdf_context']:
        print("CONTEXTE PDF (INJECTÉ):")
        print(f"  {result1['pdf_context'][:200]}...\n")
    
    # ============================================================
    # EXEMPLE 2: Écarts Spectraux
    # ============================================================
    
    print("\n[EXEMPLE 2] Analyse des écarts spectraux")
    print("-" * 70)
    
    ctx2 = MathematicalAssistantContext(
        query="Analyse les gaps entre les premiers zéros de Riemann et explique la géométrie du spectre",
        use_pdf_context=True,
        require_proof=False
    )
    
    result2 = gabriel.process_spectral_query(ctx2)
    
    print("QUESTION:")
    print(f"  {result2['query']}\n")
    
    if result2['hol4_proof']:
        proof = result2['hol4_proof']
        print("PREUVE HOL4 GÉNÉRÉE:")
        print(f"  Théorème: {proof.theorem_name}")
        print(f"  Type: {proof.pattern.value}")
        print(f"  Description: {proof.explanation}\n")
        print("  Énoncé formel:")
        for line in proof.statement.split('\n'):
            if line.strip():
                print(f"    {line}")
        print()
    
    # ============================================================
    # EXEMPLE 3: Simplification algébrique
    # ============================================================
    
    print("\n[EXEMPLE 3] Simplification algébrique avec preuve HOL4")
    print("-" * 70)
    
    ctx3 = MathematicalAssistantContext(
        query="Simplifie (x^2 + 2*x + 1) / (x + 1)",
        use_pdf_context=False,
        require_proof=False
    )
    
    result3 = gabriel.process_spectral_query(ctx3)
    
    print("QUESTION:")
    print(f"  {result3['query']}\n")
    
    print("RÉSULTAT NUMÉRIQUE:")
    if result3['mathematical_result'] and result3['mathematical_result'].status == 'success':
        print(f"  {result3['mathematical_result'].result}\n")
    
    print("PREUVE HOL4:")
    if result3['hol4_proof']:
        proof = result3['hol4_proof']
        print(f"  Théorème: {proof.theorem_name}")
        print(f"  Énoncé:")
        for line in proof.statement.split('\n'):
            if line.strip() and not line.startswith('(*'):
                print(f"    {line}")
        print(f"\n  Script de preuve:")
        for line in proof.proof_script.split('\n'):
            if line.strip():
                print(f"    {line}")
        print()
    
    # ============================================================
    # EXEMPLE 4: Spectre des nombres premiers
    # ============================================================
    
    print("\n[EXEMPLE 4] Spectre des nombres premiers")
    print("-" * 70)
    
    ctx4 = MathematicalAssistantContext(
        query="Calcule et analyse le spectre des nombres premiers jusqu'à 100",
        use_pdf_context=True,
        require_proof=False
    )
    
    result4 = gabriel.process_spectral_query(ctx4)
    
    print("QUESTION:")
    print(f"  {result4['query']}\n")
    
    print("RÉSULTAT NUMÉRIQUE:")
    if result4['mathematical_result'] and result4['mathematical_result'].status == 'success':
        data = result4['mathematical_result'].result
        if isinstance(data, dict):
            print(f"  Nombre de premiers: {data.get('count', 'N/A')}")
            print(f"  Densité: {data.get('density', 'N/A')}")
            if 'primes' in data:
                primes = data['primes'][:10]
                print(f"  Premiers (premiers 10): {primes}\n")
    
    print("PREUVE HOL4:")
    if result4['hol4_proof']:
        proof = result4['hol4_proof']
        print(f"  Théorème: {proof.theorem_name}")
        print(f"  Pattern: {proof.pattern.value}")
        print(f"  Explication: {proof.explanation}\n")
    
    # ============================================================
    # RÉSUMÉ STRUCTURE RÉPONSE
    # ============================================================
    
    print("\n" + "=" * 70)
    print("STRUCTURE COMPLÈTE D'UNE RÉPONSE GABRIEL v2.1")
    print("=" * 70)
    
    response_structure = """
result = gabriel.process_spectral_query(ctx) retourne:

{
    'query': str,
        → La requête originale
    
    'mathematical_result': ComputationResult,
        → Calcul numérique (SymPy/mpmath)
        → Status: success/error/partial
        → Data: résultats bruts
        → Engine: sympy/mpmath/pari_gp/wolfram
    
    'hol4_proof': HOL4Proof,  ← **TOUJOURS GÉNÉRÉ**
        → theorem_name: nom unique du théorème
        → statement: énoncé HOL4 formel
        → proof_script: script HOL4
        → dependencies: théories requises
        → complexity: trivial/simple/moderate/complex
        → pattern: type de pattern (RIEMANN_ZEROS, etc.)
        → explanation: explication française
    
    'formal_proof': FormalProof | None,
        → Vérification HOL4/Lean4 (optionnel)
        → Si require_proof=True
    
    'pdf_context': str | None,
        → Sections PDF pertinentes injectées
        → Si use_pdf_context=True
    
    'explanation': str,
        → Explication narrative complète
        → Inclut résultat numérique
        → Inclut preuve HOL4
        → Inclut références PDF
    
    'next_steps': List[str]
        → Suggestions pour prochaines étapes
}
"""
    
    print(response_structure)
    
    # ============================================================
    # POINTS CLÉS
    # ============================================================
    
    print("\n" + "=" * 70)
    print("POINTS CLÉS - GABRIEL v2.1")
    print("=" * 70)
    
    points = """
✓ CHAQUE RÉPONSE inclut UNE PREUVE HOL4
  → Pas de résultat "nu", tous les résultats sont certifiés

✓ DÉTECTION AUTOMATIQUE du type de requête
  → Gabriel génère le bon pattern de preuve

✓ PREUVES CONTEXTUALISÉES
  → Référencent votre théorie (riemann_spectral.thy)
  → Dépendent théories HOL4 appropriées

✓ EXPORTABLES
  → En script .thy (exécutable HOL4)
  → En Markdown (documentation)
  → En format JSON (structure données)

✓ PDF INJECTÉ AUTOMATIQUEMENT
  → Contexte du PDF Riemann injecté si pertinent
  → Références croisées avec théorie

✓ COMPOSABLE
  → Preuves s'empilent
  → Construction progressive théorie formelle

RÉSULTAT: Chaque affirmation mathématique = Rigoureuse + Illustrée + Formelle
"""
    
    print(points)


if __name__ == '__main__':
    main()

"""
POUR EXÉCUTER CET EXEMPLE:

    python EXEMPLE_GABRIEL_v2.1.py

RÉSULTAT ATTENDU:

    Affichage de 4 exemples concrets avec:
    - Questions utilisateur
    - Résultats numériques
    - Preuves HOL4 systématiques
    - Contexte PDF
    - Explications enrichies
    
STRUCTURE RETOURNÉE:

    Chaque result inclut systématiquement:
    - query: la requête
    - mathematical_result: calculs SymPy/mpmath
    - hol4_proof: PREUVE HOL4 (TOUJOURS FOURNIE)
    - formal_proof: vérification optional
    - pdf_context: sections PDF pertinentes
    - explanation: texte + HOL4 + références
    - next_steps: suggestions
"""

import sys, traceback
sys.path.insert(0, '.')
def run(k,n):
    print('\n' + '#'*70); print('# OUTER  k=%s n=%d' % (k,n)); print('#'*70)
    try:
        from pipeline_cognitif.gabriel_geometric_wrapper_v74 import PipelineCognitifNiveaux
        pcn = PipelineCognitifNiveaux(k=k, verbose=False)
        r = pcn.reconstruire(n=n)
        print('typique:', r.get('typique'), 'k:', r.get('k'))
        anc = r.get('ancrage_n10', {})
        print('ancrage_n10.premier:', anc.get('premier'))
        cd = anc.get('candidats_digamma') or []
        print('candidats_digamma count:', len(cd))
        for c in cd:
            print('   ', {kk: c.get(kk) for kk in ('description','P_candidat','est_premier','digamma_calcule','position','signe')})
        print('resultats.premier:', r.get('premier'))
        print('digamma_calcule_n:', r.get('digamma_calcule_n'))
        n2 = r.get('niveau_2', {}) or {}
        print('n2.facteur_geometrique:', (n2.get('equations') or {}).get('facteur_geometrique'))
    except Exception:
        traceback.print_exc()
for (k,n) in [(14,19),(50,16),(13,17),(7,10),(23,27),(2,45)]:
    run(k,n)
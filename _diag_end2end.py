import sys, traceback
sys.path.insert(0, 'agent-multiloop-Gabriel-local')
from src.core.spectral_core import SpectralMethodCore
from src.core.pipeline import Pipeline
smc = SpectralMethodCore()
def show(rs, n):
    print('\n' + '#'*74)
    print('# SRC END2END  %s n=%d' % (rs,n))
    print('#'*74)
    try:
        f = smc.rapport_convolutif_non_typique(rs, n)
        print('keys:', sorted(f.keys()))
        print('aucun_ancrage:', f.get('aucun_ancrage'), '| premier_indetermine:', f.get('premier_indetermine'))
        ref = f.get('reference_n10') or {}
        cib = f.get('cible') or {}
        print('ref_n10: n=%s premier=%s SA=%s SB=%s' % (ref.get('n'), ref.get('premier'), ref.get('somme_A'), ref.get('somme_B')))
        print('cible: n=%s premier=%s SA=%s SB=%s' % (cib.get('n'), cib.get('premier'), cib.get('somme_A'), cib.get('somme_B')))
        print('eqA:', (f.get('equation_A') or {}).get('forme'))
        print('eqB:', (f.get('equation_B') or {}).get('forme'))
        n1 = (f.get('niveau_1') or {}).get('possibilites', [])
        print('niveau_1 poss (count=%d):' % len(n1))
        for p in n1:
            print('   ', {kk: p.get(kk) for kk in ('position','signe','C','verdict','est_premier','digamma_calcule','branche')})
        summ = Pipeline._append_convolution_summary('Reponse.', f)
        print('--- SUMMARY ---')
        print(summ)
        print('>>> 64?', '64' in summ, '| NonDet?', 'Non déterminé' in summ, '| AucunPrem?', 'Aucun premier' in summ)
    except Exception:
        traceback.print_exc()
for (rs,n) in [('1/14',19),('1/50',16),('1/23',27),('1/2',45)]:
    show(rs,n)
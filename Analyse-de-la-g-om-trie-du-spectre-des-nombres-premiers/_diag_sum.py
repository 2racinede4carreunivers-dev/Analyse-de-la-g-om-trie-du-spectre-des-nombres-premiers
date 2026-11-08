import sys, traceback
sys.path.insert(0, '.')
from src.core.spectral_core import SpectralMethodCore
from src.core.pipeline import Pipeline
smc = SpectralMethodCore()
for (rs,n) in [('1/14',19),('1/50',16),('1/23',27),('1/2',45)]:
    print('\n' + '#'*72)
    print('# %s n=%d' % (rs,n))
    print('#'*72)
    try:
        f = smc.rapport_convolutif_non_typique(rs, n)
        f['model'] = rs
        f['equation_holds'] = False
        summ = Pipeline._append_convolution_summary('Reponse.', f)
        print(summ)
        print('>>> 64?', '64' in summ, '| NonDet?', 'Non déterminé' in summ, '| AucunPrem?', 'Aucun premier' in summ, '| A(7)+?', 'A(7)+' in summ)
    except Exception:
        traceback.print_exc()
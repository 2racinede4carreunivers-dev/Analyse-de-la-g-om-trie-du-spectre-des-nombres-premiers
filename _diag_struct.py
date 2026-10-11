import sys, traceback
sys.path.insert(0, 'agent-multiloop-Gabriel-local')
from src.core.spectral_core import SpectralMethodCore
from src.core.pipeline import Pipeline
from src.spectral.rapports_non_typiques import construire_rapport_convolutif
smc = SpectralMethodCore()
rs, n = '1/14', 19
print('# STRUCT  %s n=%d' % (rs,n))
r = construire_rapport_convolutif(rs, n)
print('keys:', sorted(r.keys()))
n1 = r.get('niveau_1') or {}
print('niveau_1 keys:', sorted(n1.keys()) if isinstance(n1,dict) else n1)
poss = (n1.get('possibilites', []) if isinstance(n1,dict) else [])
print('niveau_1.possibilites count:', len(poss))
for p in poss:
    print('   ', {kk: p.get(kk) for kk in ('position','signe','C','verdict','est_premier','branche','digamma_calcule')})
crit = r.get('criteres_obligatoires')
print('criteres_obligatoires type:', type(crit).__name__)
if isinstance(crit, dict):
    print('  ancrage_niveau_1:', crit.get('ancrage_niveau_1'), '| aucun_ancrage:', crit.get('aucun_ancrage'))
    n1c = crit.get('niveau_1') or {}
    print('  niveau_1.ancrage_retourne:', n1c.get('ancrage_retourne'))
    print('  niveau_1.demarche:', str(n1c.get('demarche',''))[:200])
ref = r.get('reference_n10') or {}
cib = r.get('cible') or {}
print('reference_n10:', {kk: ref.get(kk) for kk in ('n','premier','somme_A','somme_B','digamma_calcule')})
print('cible:', {kk: cib.get(kk) for kk in ('n','premier','somme_A','somme_B','digamma_calcule','methode','position_premier')})
print('note:', r.get('note'))
print('\n=== CLEAN SUMMARY (model injected) ===')
facts = dict(r); facts['model']=rs; facts['equation_holds']=False
summ = Pipeline._append_convolution_summary('Reponse.', facts)
print(summ)
print('\n>>> 64 in summary?', '64' in summ, '| NonDet?', 'Non déterminé' in summ, '| AucunPrem?', 'Aucun premier' in summ)
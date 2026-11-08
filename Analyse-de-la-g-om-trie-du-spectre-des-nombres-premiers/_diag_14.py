#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, traceback
sys.path.insert(0, 'src')

def safe(fn):
    try:
        return fn()
    except Exception as e:
        return 'EXC: ' + repr(e) + '\n' + traceback.format_exc()

from src.spectral.rapports_non_typiques import (
    construire_rapport_convolutif, suite_A, suite_B, equations_ab,
    quatre_possibilites_digamma, niveau_1_entier, niveau_2_geometrique,
    criteres_obligatoires, reconstruire_premier, reconstruire_premier_pour_n,
)
from src.core.spectral_core import SpectralMethodCore

def dump(label, obj):
    print('\n===== %s =====' % label)
    if isinstance(obj, dict):
        for kk in sorted(obj.keys()):
            vv = obj[kk]
            if isinstance(vv, dict):
                print('  %s: { %s }' % (kk, ', '.join('%s=%r' % (k2, vv[k2]) for k2 in sorted(vv.keys()))))
            elif isinstance(vv, (list, tuple)):
                print('  %s: (len %d) %s' % (kk, len(vv), vv[:8]))
            else:
                try:
                    print('  %s: %r' % (kk, vv))
                except Exception:
                    print('  %s: <unrepr>')
    else:
        print(obj)

def run(k_str, n):
    print('\n' + '#'*64)
    print('# RAPPORT %s  n=%d' % (k_str, n))
    print('#'*64)
    r = safe(lambda: construire_rapport_convolutif(k_str, n))
    dump('construire_rapport_convolutif', r)
    ka = int(k_str.split('/')[1])
    print('\n-- sommes brutes --')
    print('suite_A(%d,%d) =' % (ka,n), safe(lambda: suite_A(ka, n)))
    print('suite_B(%d,%d) =' % (ka,n), safe(lambda: suite_B(ka, n)))
    print('\n-- quatre_possibilites_digamma (n=10) --')
    dump('qp', safe(lambda: quatre_possibilites_digamma(k_str, 10)))
    print('\n-- niveau_1_entier (n=10) --')
    dump('n1', safe(lambda: niveau_1_entier(k_str, 10)))
    print('\n-- niveau_2_geometrique (n=10) --')
    n2 = safe(lambda: niveau_2_geometrique(k_str, 10))
    dump('n2', n2)
    print('\n-- criteres_obligatoires (n=10) --')
    dump('crit', safe(lambda: criteres_obligatoires(k_str, 10)))
    print('\n-- reconstruire_premier --')
    dump('reconv', safe(lambda: reconstruire_premier(k_str)))
    print('\n-- SpectralMethodCore.rapport_convolutif_non_typique --')
    smc = SpectralMethodCore()
    dump('smc_non_typique', safe(lambda: smc.reconstruire_rapport_non_typique(k_str, n=n)))

run('1/14', 19)
run('1/50', 16)
run('1/23', 27)

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports

import re, subprocess, sys
out = subprocess.run([sys.executable, '_diag_cap14.py'], capture_output=True, text=True).stdout
i = out.find('===== rapport_convolutif_non_typique 1/14')
j = out.find('=====', i + 1) if i >= 0 else -1
sec = out[i:j] if i >= 0 else ''
print('--- 1/14 summary section ---')
print(sec.strip())
print()
print('>>> "facteur 64" (64 as factor):', 'facteur 64' in sec)
print('>>> "Zeta=64" (64 as zeta):', 'Zêta=64' in sec or 'Zeta=64' in sec)
print('>>> "Candidat: Non déterminé":', 'Candidat: Non déterminé' in sec)
print('>>> SB-64 * p leak:', re.search(r'SB\s*-\s*64', sec) is not None)
print('>>> Zêta=7529536 (k^6) present:', 'Zêta=7529536' in sec)
print('>>> g(k)=1.0025477748 present:', '1.0025477748' in sec)
print('>>> 4x [COMPOSE] at n=10:', sec.count('[COMPOSE]'))
# show only tokens containing a 64 run, to expose any false-positive
print('>>> tokens containing "64":', sorted({t for t in sec.split() if '64' in t}))

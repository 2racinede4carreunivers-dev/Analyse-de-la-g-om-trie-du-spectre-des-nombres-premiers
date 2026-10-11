import re, glob, pathlib
base = pathlib.Path(r'c:\agent-multiloop-Gabriel-local\agent-multiloop-Gabriel-local\theories')
orig_lines = (base/'methode_spectral.thy').read_text(encoding='utf-8').splitlines()
print('ORIGINAL total:', len(orig_lines))
print('L1:', orig_lines[0][:80])
print('L2:', orig_lines[1][:80])
print('L5015:', orig_lines[5014][:80][:80])
orig = '\n'.join(orig_lines)
print('ORIGINAL theorem:', len(re.findall(r'(?m)^\s*theorem\b', orig)),
      'lemma:', len(re.findall(r'(?m)^\s*lemma\b', orig)),
      'definition:', len(re.findall(r'(?m)^\s*definition\b', orig)),
      'section:', len(re.findall(r'(?m)^section\b', orig)))
ts = tl = td = tsc = 0
for f in sorted(glob.glob(str(base/'MS_*.thy'))):
    t = pathlib.Path(f).read_text(encoding='utf-8')
    ts += len(re.findall(r'(?m)^\s*theorem\b', t))
    tl += len(re.findall(r'(?m)^\s*lemma\b', t))
    td += len(re.findall(r'(?m)^\s*definition\b', t))
    tsc += len(re.findall(r'(?m)^section\b', t))
print('SPLIT theorem:', ts, 'lemma:', tl, 'definition:', td, 'section:', tsc)

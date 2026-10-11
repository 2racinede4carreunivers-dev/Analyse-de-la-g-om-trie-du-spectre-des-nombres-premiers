import pathlib, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p = pathlib.Path(r'c:\agent-multiloop-Gabriel-local\agent-multiloop-Gabriel-local\theories\validation_hol_unifiee.thy')
data = p.read_bytes().decode('utf-8', 'replace')
print('taille octets:', len(data))
for off in (16169, 29981):
    print('====== offset', off, '======')
    print(repr(data[off-400:off+200]))
    print('--- lignes autour ---')
    ln = data[:off].count('\n') + 1
    lines = data.splitlines()
    for i in range(max(0, ln-12), min(len(lines), ln+4)):
        print(f'{i+1}: {lines[i][:150]}')

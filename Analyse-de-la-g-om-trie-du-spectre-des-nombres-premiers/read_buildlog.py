import sqlite3, subprocess, tempfile, pathlib, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
db = r'C:\Users\Utilisateur\.isabelle\Isabelle2025-2\heaps\polyml-5.9.2_x86_64_32-windows\log\Geometrie_Spectre_Premier_Philippe_Thomas_Savard.db'
con = sqlite3.connect(db)
row = con.execute('select ml_statistics, command_timings from isabelle_session_info').fetchone()
ZSTD = r'C:\Users\isabelle\Isabelle2025-2\contrib\cygwin\bin\zstd.exe'
for i, nm in enumerate(['ml_statistics','command_timings']):
    raw = bytes(row[i])
    print(nm, 'brut:', len(raw))
    with tempfile.NamedTemporaryFile(delete=False, suffix='.zst') as f:
        f.write(raw); tmp = f.name
    # zstd lit le framing magic tout seul
    p = subprocess.run([ZSTD, '-dc', tmp], capture_output=True)
    pathlib.Path(tmp).unlink()
    if p.returncode != 0:
        print('zstd echec:', p.stderr.decode('utf-8','replace')[:500]); continue
    txt = p.stdout.decode('utf-8', 'replace')
    print('---', nm, 'decompresse:', len(txt), 'caracteres ---')
    out = pathlib.Path(r'c:\agent-multiloop-Gabriel-local')/(nm+'.txt')
    out.write_text(txt, encoding='utf-8')
    print('ecrit:', out)
    print(txt[:2000])
    print('... FIN (dernier 1200):')
    print(txt[-1200:])
    print('======')
con.close()

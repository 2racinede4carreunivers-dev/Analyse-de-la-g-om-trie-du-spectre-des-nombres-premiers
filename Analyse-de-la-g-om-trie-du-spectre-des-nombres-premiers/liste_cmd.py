import re, pathlib, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
raw = pathlib.Path(r'c:\agent-multiloop-Gabriel-local\command_timings.txt').read_bytes().decode('utf-8', 'replace')
recs = re.findall(r'elapsed=([0-9.]+)\x06name=([^\x05\x06]+)\x06offset=(\d+)\x06file=([^\x05\x06]+)', raw)
print('total commandes:', len(recs))
proj = [r for r in recs if 'agent-multiloop' in r[3]]
print('commandes projet:', len(proj))
for el, name, off, f in proj:
    print(f'{pathlib.Path(f.strip()).name} | offset={off} | {name.strip()} | {el}s')

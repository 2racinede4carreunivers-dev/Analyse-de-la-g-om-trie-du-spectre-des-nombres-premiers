import re, pathlib, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
txt = pathlib.Path(r'c:\agent-multiloop-Gabriel-local\ml_statistics.txt').read_text(encoding='utf-8')
recs = re.findall(r'now=([0-9.]+).*?full_GCs=(\d+).*?size_heap=(\d+).*?size_heap_free_last_full_GC=(\d+).*?size_heap_free_last_GC=(\d+).*?time_elapsed=([0-9.]+)', txt)
print('echantillons ml:', len(recs))
t0 = float(recs[0][0])
print('--- 12 derniers echantillons (t, heap Go, libre/fullGC Go, fullGC) ---')
for now, fgc, heap, free_full, free_last, el in recs[-12:]:
    print(f"t={(float(now)-t0)/1:.0f}s heap={int(heap)/1e9:.2f}Go libre_full={int(free_full)/1e9:.3f}Go libre_last={int(free_last)/1e9:.3f}Go fullGC={fgc} elapsed={el}")
print()
ct = pathlib.Path(r'c:\agent-multiloop-Gabriel-local\command_timings.txt').read_text(encoding='utf-8')
cmds = re.findall(r'elapsed=([0-9.]+).*?name=(\S+).*?offset=(\d+).*?file=([^\x05\x06]+)', ct)
print('commandes:', len(cmds))
ours = [c for c in cmds if 'agent-multiloop' in c[3]]
print('commandes projet:', len(ours))
print('--- 15 dernieres commandes projet ---')
for el, name, off, f in ours[-15:]:
    print(f'{pathlib.Path(f.strip()).name} offset={off} {name} {el}s')

import os, sys
base = os.getcwd()
d = os.path.join(base, "pythonLLM")
print("=== pythonLLM EXISTS:", os.path.isdir(d), "===")
if os.path.isdir(d):
    for root, dirs, files in os.walk(d):
        rel = os.path.relpath(root, base).replace("\\", "/")
        print("DIR ", rel)
        for fn in sorted(files):
            p = os.path.join(root, fn)
            print("   FILE", fn, os.path.getsize(p), "o")
        if not dirs and not files:
            print("   (vide)")
print()
print("=== fichiers racine contenant pythonllm/computation ===")
for f in sorted(os.listdir(base)):
    if "pythonllm" in f.lower() or "computation" in f.lower():
        p = os.path.join(base, f)
        print(("D" if os.path.isdir(p) else "F"), f)
print()
print("=== tests/ mentionnant pythonLLM ===")
td = os.path.join(base, "tests")
hits = []
for root, dirs, files in os.walk(td):
    for fn in files:
        p = os.path.join(root, fn)
        try:
            t = open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        if "pythonLLM" in t or "pythonllm" in t.lower():
            hits.append(os.path.relpath(p, base).replace("\\", "/"))
print("\n".join(hits) if hits else "(aucun)")


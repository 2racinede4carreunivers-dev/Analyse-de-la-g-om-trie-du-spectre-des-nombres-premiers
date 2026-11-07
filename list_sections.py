import re, pathlib
base = pathlib.Path(r"c:\agent-multiloop-Gabriel-local\agent-multiloop-Gabriel-local\theories")
for fn in ["methode_spectral.thy","validation_hol_unifiee.thy","validation_zeta_lean.thy"]:
    t = (base/fn).read_text(encoding="utf-8", errors="replace")
    lines = t.splitlines()
    print("="*80)
    print(fn, len(lines), "lignes", len(t), "octets")
    for i,l in enumerate(lines, start=1):
        s=l.strip()
        if s.startswith("section ") or s.startswith("subsection ") or s.startswith("chapter "):
            print(f"  L{i:5d} : {s[:150]}")
    # defs/lemmas count
    for kw in ["definition ","lemma ","theorem ","axiomatization","locale ","interpretation "]:
        c = sum(1 for l in lines if l.strip().startswith(kw))
        print(f"   [{kw.strip():15s} : {c}]")

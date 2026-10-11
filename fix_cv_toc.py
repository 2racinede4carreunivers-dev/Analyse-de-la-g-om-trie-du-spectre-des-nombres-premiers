import pathlib, re
base = pathlib.Path(r"c:\agent-multiloop-Gabriel-local\agent-multiloop-Gabriel-local\theories")

def sections_of(lines):
    secs=[]
    for i,l in enumerate(lines, start=1):
        s=l.strip()
        if s.startswith("section ") or s.startswith("subsection "):
            m=re.search(r'"(.*)"',s)
            lab=m.group(1) if m else s[:110]
            kind="section" if s.startswith("section") else "subsection"
            secs.append([i,kind,lab])
    n=len(lines)
    out=[]
    for k,(ln,kind,lab) in enumerate(secs):
        nxt = secs[k+1][0]-1 if k+1<len(secs) else n
        # fin reelle : remonter avant lignes vides / 'end' final
        out.append((ln,nxt,kind,lab))
    return out

for fn in ["validation_hol_unifiee.thy","validation_zeta_lean.thy"]:
    p = base/fn
    t = p.read_text(encoding="utf-8", errors="replace")
    lines = t.splitlines()
    secs = sections_of(lines)
    toc = "\n".join([f"   L{a:4d} - L{b:4d} : [{kind}] {lab}" for a,b,kind,lab in secs])
    # remplace le bloc TOC existant (entre 'TABLE DES MATIERES' et la ligne '====...*)')
    new_t, n = re.subn(r'(TABLE DES MATIERES[^\n]*\n)(.*?)(\n   =+ \*\))',
                       lambda m: m.group(1)+toc+m.group(3),
                       t, count=1, flags=re.S)
    if n==0:
        print(fn, "!! motif TOC introuvable"); continue
    p.write_text(new_t, encoding="utf-8")
    print(fn, "TOC recalee :", len(secs), "entrees (numerotation actuelle du fichier)")
    for a,b,kind,lab in secs:
        print(f"   L{a:4d}-L{b:4d} [{kind:10s}] {lab[:95]}")

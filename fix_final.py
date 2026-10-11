import pathlib, re

p = pathlib.Path(r"c:\agent-multiloop-Gabriel-local\agent-multiloop-Gabriel-local\theories\validation_hol_unifiee.thy")
text = p.read_text(encoding="utf-8")
nl = "\r\n" if "\r\n" in text else "\n"
L = text.split(nl)

# --- 1. Repare les litteraux de chaineperdus (bug des guillemets Python)
n = 0
for k, l in enumerate(L):
    if "= EXCLU_HOL\"" in l:
        L[k] = l.replace("= EXCLU_HOL\"", "= ''EXCLU_HOL''\"")
        n += 1
print("litteraux repares :", n)

# --- 2. Bloc `cases b` : forme deterministe `from <cas> <fait> show ...`
i = next(k for k, l in enumerate(L)
         if l.strip() == "proof (intro allI)"
         and any("toutes_branches" in L[x] for x in range(max(0, k - 12), k)))
j = next(k for k in range(i, len(L)) if L[k].strip() == "qed" and L[k].startswith("  "))

BR = [("A7plus", "np1"), ("A7moins", "np2"), ("A8plus", "np3"), ("A8moins", "np4")]
blk = ["  show ?thesis", "  proof (cases b)"]
for n2, (c, hy) in enumerate(BR):
    blk.append(("    case %s" if n2 == 0 else "    next %s") % c)
    blk.append("    from %s %s show ?thesis unfolding verdict_branche_def by simp" % (c, hy))
blk.append("  qed")
L[i:j + 1] = blk

p.write_text(nl.join(L), encoding="utf-8")
print("bloc cases remplace ; lignes", i + 1, "a", j + 1)
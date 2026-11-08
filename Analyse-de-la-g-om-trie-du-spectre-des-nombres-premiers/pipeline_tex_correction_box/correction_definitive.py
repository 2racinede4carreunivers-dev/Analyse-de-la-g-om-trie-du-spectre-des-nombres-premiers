#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
correction_definitive.py — Correction robuste et définitive.

Approche : pile (stack-based) pour trouver TOUS les environnements
non fermés, puis insertion de tous les \end{env} manquants juste
avant \end{document}, en ordre inverse d'ouverture. Cela préserve
l'imbrication correcte des environnements à l'intérieur du corps
du document.
"""
from __future__ import annotations
import re
from pathlib import Path

TEX_SRC = Path(r"C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\theories\tex\Le-systeme-convolutif-Gabriel.tex")
TEX_OUT = Path(r"C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\theories\tex\Le-systeme-convolutif-Gabriel_corrige.tex")

def main() -> int:
    content = TEX_SRC.read_text(encoding="utf-8")
    lines = content.split("\n")

    # ── 1. Supprimer les backslashes isolés (ligne seule == "\") ──
    bs_removed = 0
    new_lines: list[str] = []
    for line in lines:
        if line.strip() == "\\":
            bs_removed += 1
            continue
        new_lines.append(line)
    lines = new_lines

    # ── 2. Stack-based : trouver tous les environnements ouverts ──
    begin_re = re.compile(r"\\begin\{([^}]+)\}")
    end_re = re.compile(r"\\end\{([^}]+)\}")

    stack: list[str] = []  # noms d'environnements encore ouverts
    open_positions: list[tuple[str, int]] = []  # (nom, ligne) pour rapport

    for i, line in enumerate(lines, 1):
        for m in begin_re.finditer(line):
            env_name = m.group(1)
            stack.append(env_name)
            open_positions.append((env_name, i))
        for m in end_re.finditer(line):
            env_name = m.group(1)
            # Retirer le premier élément correspondant depuis le haut de la pile
            for j in range(len(stack) - 1, -1, -1):
                if stack[j] == env_name:
                    stack.pop(j)
                    break

    unclosed = stack  # environnements toujours ouverts
    print(f"Environnements non fermés détectés : {len(unclosed)}")
    for env_name, line_no in open_positions:
        if env_name in unclosed:
            # Compter combien de fois ce nom est encore ouvert
            count = unclosed.count(env_name)
            if count > 0:
                print(f"  \\begin{{{env_name}}} à la ligne {line_no} — encore ouvert")
                unclosed.remove(env_name)

    # ── 3. Insérer les \end{env} manquants juste avant \end{document} ──
    # Ordre inverse d'ouverture (dernier ouvert = premier fermé)
    insertions = 0
    doc_end_idx = None
    for i, line in enumerate(lines):
        if "\\end{document}" in line:
            doc_end_idx = i
            break

    if doc_end_idx is None:
        print("ERREUR : \\end{document} non trouvé !")
        return 1

    # Insérer en ordre inverse (dernier ouvert en premier)
    for env_name in reversed(stack):
        lines.insert(doc_end_idx, f"\\end{{{env_name}}}")
        doc_end_idx += 1
        insertions += 1
        print(f"  \\end{{{env_name}}} inséré avant \\end{{document}}")

    # ── 4. Sauvegarder ──
    TEX_OUT.write_text("\n".join(lines), encoding="utf-8")

    print()
    print("=" * 60)
    print("CORRECTION TERMINÉE")
    print("=" * 60)
    print(f"  Fichier source : {TEX_SRC}")
    print(f"  Fichier corrigé : {TEX_OUT}")
    print(f"  Backslashes isolés supprimés : {bs_removed}")
    print(f"  \\end{{env}} insérés avant \\end{{document}} : {insertions}")
    print(f"  Lignes originales : {len(content.split(chr(10)))}")
    print(f"  Lignes finales : {len(lines)}")
    print("=" * 60)

    # ── 5. Vérification ──
    content2 = TEX_OUT.read_text(encoding="utf-8")
    # Compter begins et ends pour chaque type d'environnement
    all_begins = re.findall(r"\\begin\{([^}]+)\}", content2)
    all_ends = re.findall(r"\\end\{([^}]+)\}", content2)
    from collections import Counter
    begin_counts = Counter(all_begins)
    end_counts = Counter(all_ends)
    all_env_names = set(begin_counts.keys()) | set(end_counts.keys())
    unbalanced = {e: begin_counts.get(e, 0) - end_counts.get(e, 0)
                  for e in all_env_names if begin_counts.get(e, 0) != end_counts.get(e, 0)}

    print()
    print("VÉRIFICATION DE L'ÉQUILIBRE DES ENVIRONNEMENTS :")
    if not unbalanced:
        print("  ✅ TOUS les environnements sont équilibrés !")
    else:
        print("  ❌ Environnements encore déséquilibrés :")
        for env, diff in sorted(unbalanced.items()):
            sens = "ouverts" if diff > 0 else "fermés en excès"
            print(f"    \\begin{{{env}}} / \\end{{{env}}} : diff = {diff} ({sens})")

    return 0 if not unbalanced else 1

if __name__ == "__main__":
    raise SystemExit(main())
# Document final

- `Philippe_Thomas_Savard_@_tous_droits_réservé-2026.tex` est la source de référence.
- Le PDF compilé porte le même nom.
- Les fichiers `arborescence_*.tex`, images, graphiques et classeurs dans `assets/` sont ses dépendances et annexes.
- `Archive/` conserve les éditions précédentes et les autres documents TeX/PDF déplacés sans en supprimer le contenu.
- `Certification_primalité/` contient les scripts, manifestes et fragments vérifiables des rapports de primalité.

Le workflow GitHub Actions compile la session Isabelle déclarée dans `theories/ROOT`, compile le document TeX final, vérifie les fragments, publie les artefacts de compilation et génère une attestation de provenance SHA-256.

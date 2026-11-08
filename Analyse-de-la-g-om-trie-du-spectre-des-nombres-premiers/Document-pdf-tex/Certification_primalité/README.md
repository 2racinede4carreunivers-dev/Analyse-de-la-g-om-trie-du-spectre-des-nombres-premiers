# Certification de primalité

Les originaux intégraux restent dans `originals/` sur le poste local et ne sont pas ajoutés à Git. Les fichiers versionnés dans `parts/` sont des fragments binaires consécutifs de 90 Mio au maximum; leur concaténation restitue exactement chaque original.

`manifest.json` enregistre la taille et le SHA-256 de chaque original ainsi que la taille et le SHA-256 de chaque fragment. Pour vérifier les fragments sans créer les fichiers complets :

```powershell
python .\reassemble_parts.py verify
```

Pour reconstituer les originaux dans un nouveau dossier :

```powershell
python .\reassemble_parts.py reassemble --output-dir .\reconstructed
```

Les sorties reconstruites ne remplacent jamais les originaux existants. Les empreintes SHA-256 vérifient l’intégrité des fichiers; l’attestation de provenance du workflow GitHub est un artefact distinct qui indique le workflow ayant produit le PDF.

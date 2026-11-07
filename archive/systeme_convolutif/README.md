# Archive du systeme convolutif

Cette archive conserve les artefacts de construction remplaces par le livrable
final `../../systeme_convolutif_spectral_general.xlsx`.

| Fichier | Role historique |
| --- | --- |
| `systeme_convolutif_spectral.xlsx` | Classeur source initial. |
| `update_excel_general.py` | Mise a jour du classeur source et generation de l'etape suivante. |
| `systeme_convolutif_spectral_genere.xlsx` | Classeur intermediaire servant de source au generateur final. |
| `generate_excel_convolutif_general.py` | Generateur final conserve a la racine ; il utilise le classeur intermediaire archive. |
| `spectral_engine.py` | Prototype autonome du moteur de calcul. |
| `moteur_universel_1_k.py` | Prototype interactif autonome. |
| `build_spectral_db.py` | Generateur de la base SQLite de verification. |
| `systeme_convolutif_spectral.sqlite` | Base de verification produite par le script precedent. |

Le code applicatif maintenu et ses tests restent dans
`../../agent-multiloop-Gabriel-local/`.

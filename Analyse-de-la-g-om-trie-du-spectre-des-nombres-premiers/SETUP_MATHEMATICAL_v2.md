# Gabriel v2.0 - Configuration Moteur Mathématique Spectral

## 📋 Vue d'ensemble

Ce guide explique comment configurer Gabriel avec les nouveaux modules mathématiques:
- **Moteur symbolique** (SymPy, mpmath)
- **Vérification formelle** (HOL4, Lean4)
- **Traitement PDF RAG** (analyse_hypothese_riemann_savard.pdf)

## 📁 Structure des fichiers ajoutés

```
agent-multiloop-Gabriel-local/
├── src/
│   ├── mathematical_engine.py          # Calculs symboliques & numériques
│   ├── hol_lean_interface.py           # Vérification formelle HOL4/Lean4
│   ├── pdf_rag_processor.py            # Traitement PDF & indexation RAG
│   └── __init__.py                     # (à créer)
├── theories/
│   ├── riemann_spectral.thy            # Théorie HOL4 (nouveau)
│   ├── RiemannSpectral.lean            # Théorie Lean4 (nouveau)
│   └── *.thy                           # Théories HOL4 existantes
├── pdf/
│   └── analyse_hypothese_riemann_savard.pdf   # PDF Riemann (déjà placé)
├── data/
│   └── pdf_index.json                  # Index RAG généré
├── gabriel_mathematical.py             # Point d'entrée mathématique (nouveau)
├── config_mathematical.env             # Configuration (nouveau)
├── requirements.txt                    # Dépendances mises à jour
└── ...
```

## 🔧 Installation des dépendances Python

### Étape 1: Dépendances de base

```bash
cd agent-multiloop-Gabriel-local
pip install -r requirements.txt
```

### Étape 2: Installation HOL4 (optionnel mais recommandé)

**Sur Windows (avec WSL2 ou cygwin recommandé):**

```bash
# Via package manager
choco install hol4  # Si Chocolatey disponible

# Ou manuellement:
# Télécharger depuis: https://github.com/HOL-Theorem-Prover/HOL
# Suivre instructions dans HOL/INSTALL
```

**Sur Linux/macOS:**

```bash
sudo apt-get install hol4  # Debian/Ubuntu
# ou
brew install hol4  # macOS
```

**Vérifier installation:**

```bash
holmake --version
```

### Étape 3: Installation Lean4 (optionnel mais recommandé)

**Tout système:**

```bash
# Installer elan (Lean version manager)
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh

# Charger environnement
source $HOME/.elan/env

# Vérifier
lean --version
```

### Étape 4: PARI/GP (optionnel, pour haute précision)

**Windows:**
```bash
choco install pari-gp
```

**Linux:**
```bash
sudo apt-get install pari-gp
```

**macOS:**
```bash
brew install pari
```

### Étape 5: Wolfram Engine (optionnel, très recommandé pour haute performance)

```bash
# Télécharger gratuitement (compte Wolfram Community):
# https://www.wolfram.com/engine/free-license/

# Installation Windows:
# Exécuter l'installeur gratuit Wolfram Engine
```

## ⚙️ Configuration

### Fichier config_mathematical.env

Adapter les chemins selon votre système:

```bash
# HOL4 path
HOL4_PATH=/usr/bin/holmake  # Linux
HOL4_PATH="C:\Program Files\HOL4\holmake.exe"  # Windows

# Lean4 path
LEAN_PATH=/home/user/.elan/toolchains/leanprover--lean4---v4.0.0/bin
LEAN_PATH="/c/Users/user/.elan/toolchains/leanprover--lean4---v4.0.0/bin"  # Windows WSL

# PDF Riemann
RIEMANN_PDF_PATH=pdf/analyse_hypothese_riemann_savard.pdf

# Wolfram (si installé)
WOLFRAM_ENGINE_ENABLED=true
WOLFRAM_KERNEL_PATH=/opt/Wolfram/WolframKernel  # Linux
WOLFRAM_KERNEL_PATH="C:\Program Files\Wolfram Research\Mathematica\12.0\MathKernel.exe"  # Windows
```

### Chargement au démarrage

Ajouter à votre `main.py` existant:

```python
from gabriel_mathematical import get_gabriel, MathematicalAssistantContext

# Initialiser Gabriel mathématique
gabriel = get_gabriel()

# Utiliser pour requêtes mathématiques
ctx = MathematicalAssistantContext(
    query="Calcule les zéros de Riemann",
    use_pdf_context=True,
    require_proof=False
)
result = gabriel.process_spectral_query(ctx)
```

## 🧪 Tests de validation

### Test 1: Module mathématique

```bash
python src/mathematical_engine.py
```

Devrait afficher:
- ✓ Simplification d'expressions
- ✓ Calcul de zéros de Riemann
- ✓ Spectre des nombres premiers

### Test 2: Vérification formelle

```bash
python src/hol_lean_interface.py
```

Attendu:
- Interface HOL4 détectée ou non
- Interface Lean4 détectée ou non
- Statut vérification théorèmes

### Test 3: Traitement PDF

```bash
python src/pdf_rag_processor.py
```

Attendu:
- Chargement du PDF
- Parsing des sections
- Indexation RAG

### Test 4: Intégration Gabriel

```bash
python gabriel_mathematical.py
```

Effectue 3 tests d'intégration complète.

## 📊 Utilisation du PDF Riemann

Le PDF `analyse_hypothese_riemann_savard.pdf` est automatiquement:

1. **Chargé à l'initialisation** (construction RAG index)
2. **Parsé en sections** (auto-détection avec exclusion des sections HOL)
3. **Indexé pour recherche** (mots-clés, embeddings)
4. **Injecté en contexte** (augmentation génération pour requêtes pertinentes)

### Schéma d'injection contexte:

```
Requête utilisateur
    ↓
[Recherche RAG sur PDF] → Top 3 sections pertinentes
    ↓
[Injection contexte] → Préfixe de prompt Gabriel avec extraits PDF
    ↓
[Traitement] → Gabriel génère réponse enrichie par PDF
    ↓
Réponse + références PDF + calculs mathématiques
```

### Sections du PDF automatiquement exclues:

Les sections contenant: `HOL`, `Isabelle`, `theorem`, `proof` sont excluées par défaut.
À modifier dans `config_mathematical.env`:

```
HOL_SECTIONS_SKIP=HOL,Isabelle,theorem,proof,your_section
```

## 🔗 Intégration avec théorie "L'univers est au carré"

Gabriel peut désormais:

1. **Référencer votre théorie** (5 chapitres + 499 pages PDF disponibles)
2. **Vérifier formellement** les propositions mathématiques
3. **Analyser la géométrie spectrale** des nombres premiers
4. **Générer code** HOL4/Lean4 pour preuves assistées

Configuration spécifique:

```bash
THEORY_CONTEXT=L_univers_au_carre
CHAPTER_FOCUS=geometric_riemann_spectrum
```

## 🚀 Utilisation avancée

### 1. Requête avec preuve formelle:

```python
ctx = MathematicalAssistantContext(
    query="Prouve que tous les zéros de Riemann ont Re(s) = 1/2",
    require_proof=True,     # Génère preuve HOL4/Lean4
    use_pdf_context=True    # Injecte PDF contexte
)
result = gabriel.process_spectral_query(ctx)
print(result['formal_proof'])
```

### 2. Calcul haute précision:

```python
from src.mathematical_engine import MathematicalEngine

engine = MathematicalEngine(precision_bits=1024)  # 1024 bits!
zeros = engine.compute_riemann_zeros(count=1000, precision_digits=500)
```

### 3. Analyse spectre premiers personnalisée:

```python
spectrum = engine.compute_prime_spectrum(max_prime=10000)
gaps = [spectrum['primes'][i+1] - spectrum['primes'][i] 
        for i in range(len(spectrum['primes'])-1)]
print(f"Écart moyen: {sum(gaps)/len(gaps)}")
```

## 📚 Documentation modules

### mathematical_engine.py

Classes:
- `MathematicalEngine`: Moteur symbolique/numérique multimodal
- `ComputationResult`: Résultat standardisé

Méthodes principales:
- `compute_riemann_zeros(count, precision_digits)` → Liste zéros
- `compute_spectral_gap(zero_indices)` → Écarts spectraux
- `compute_prime_spectrum(max_prime)` → Spectre premiers
- `simplify_expression(expr_str)` → Simplification symbolique

### hol_lean_interface.py

Classes:
- `HOL4Interface`: Vérification théorèmes HOL4
- `Lean4Interface`: Vérification théorèmes Lean4
- `FormalVerificationPipeline`: Pipeline dual

Méthodes:
- `verify_theorem(name, statement, proof_script)` → FormalProof
- `load_theory_file(path)` → Dict[théorèmes, définitions]

### pdf_rag_processor.py

Classes:
- `PDFSection`: Représentation section
- `PDFRAGProcessor`: Traitement PDF + indexation

Méthodes:
- `parse_sections()` → List[PDFSection]
- `search(query, top_k)` → Sections pertinentes
- `generate_context_prompt(query)` → String contexte

## 🐛 Dépannage

### Erreur: "HOL4 non disponible"
→ HOL4 n'est pas installé. Soit installer (voir Étape 2), soit laisser fonctionnel avec Lean4 uniquement.

### Erreur: "PDF non trouvé"
→ Placer `analyse_hypothese_riemann_savard.pdf` dans `pdf/`

### Erreur: "PyPDF2 not installed"
→ `pip install PyPDF2>=4.0.0`

### Performance lente pour Riemann
→ Réduire `RIEMANN_ZEROS_COUNT` ou augmenter `MATH_PRECISION_BITS` seulement si nécessaire

## ✅ Checklist déploiement

- [ ] `pip install -r requirements.txt`
- [ ] Placer PDF: `pdf/analyse_hypothese_riemann_savard.pdf`
- [ ] Adapter `config_mathematical.env` (chemins HOL4/Lean4)
- [ ] Exécuter tests validation (3 tests)
- [ ] Intégrer `gabriel_mathematical` à `main.py`
- [ ] Test intégration complète
- [ ] Documentation théorie personnelle lien

## 📞 Support

Erreurs ou questions:
1. Vérifier logs: `logs/gabriel_mathematical.log`
2. Relancer tests validation
3. Consulter documentation HOL4/Lean4 officielles

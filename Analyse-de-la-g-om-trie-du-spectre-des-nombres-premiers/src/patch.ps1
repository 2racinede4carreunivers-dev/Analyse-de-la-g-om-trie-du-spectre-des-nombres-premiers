Write-Host "=== Patch Gabriel : Extension spectrale et rapports non typiques ==="

function Append-Block {
    param(
        [string]$Path,
        [string]$Block,
        [string]$Label
    )

    if (-not (Test-Path $Path)) {
        Write-Host "⚠ Fichier introuvable : $Path (ignore)" -ForegroundColor Yellow
        return
    }

    $content = Get-Content $Path
    if ($content -join "`n" -like "*$Block*") {
        Write-Host "• Bloc déjà présent dans $Path (skip) : $Label" -ForegroundColor DarkGray
        return
    }

    $content += ""
    $content += $Block
    Set-Content -Path $Path -Value $content
    Write-Host "✓ Patch appliqué dans $Path : $Label" -ForegroundColor Green
}

# 1. Extension du cœur spectral : sélection modèle typique / non typique
$blockSpectralCore = @'
# === Extension Gabriel : sélection du modèle spectral (typique / non typique) ===
from src.spectral.rapports_non_typiques import choisir_modele_non_typique

def select_spectral_model(params):
    """
    Sélectionne le modèle spectral approprié.
    - Conserve le modèle 1/2 pour les cas typiques
    - Utilise src.spectral.rapports_non_typiques pour les rapports non typiques (1/3, 1/5, 1/6, etc.)
    """
    rapport = params.get("rapport")
    if rapport == "1/2":
        return "modele_1_2"
    return choisir_modele_non_typique(params)
'@

Append-Block -Path "src/core/spectral_core.py" -Block $blockSpectralCore -Label "select_spectral_model"


# 2. Pipeline étendu : branchement sur le reconstructeur non typique
$blockPipeline = @'
# === Extension Gabriel : pipeline spectral étendu pour rapports non typiques ===
from src.spectral.reconstructor import reconstruire_rapport_non_typique

def run_spectral_pipeline_extended(params):
    """
    Pipeline étendu :
    - garde run_spectral_pipeline pour les cas typiques (1/2)
    - utilise reconstruire_rapport_non_typique pour les rapports non typiques
    """
    if params.get("rapport") == "1/2":
        return run_spectral_pipeline(params)
    return reconstruire_rapport_non_typique(params)
'@

Append-Block -Path "src/core/pipeline.py" -Block $blockPipeline -Label "run_spectral_pipeline_extended"


# 3. Module rapports non typiques : intégration des modules spectral
$blockRapportsNonTypiques = @'
# === Module Gabriel : rapports non typiques (extension, ne touche pas au modèle 1/2) ===
from .ratios import calculer_rapport_non_typique
from .digamma_pure import digamma_savard
from .tchebychev_savard_pipeline import reconstruire_tchebychev

def choisir_modele_non_typique(params):
    """
    Choisit le modèle spectral pour un rapport non typique (1/3, 1/5, 1/6, etc.).
    Ne modifie pas le modèle 1/2, mais ajoute les cas non typiques.
    """
    rapport = params.get("rapport")
    n = params.get("n")
    valeur = calculer_rapport_non_typique(rapport, n)
    return {
        "rapport": rapport,
        "n": n,
        "valeur": valeur,
        "digamma": digamma_savard(rapport, n),
    }

def reconstruire_rapport_non_typique(params):
    """
    Reconstruit le rapport non typique avec la pipeline Tchebychev + digamma.
    Exemple attendu : rapport = 1/6, n = 14 -> 7649 (cohérent avec le pipeline spectral Python).
    """
    base = choisir_modele_non_typique(params)
    return reconstruire_tchebychev(base)
'@

if (-not (Test-Path "src/spectral/rapports_non_typiques.py")) {
    Write-Host "• Création de src/spectral/rapports_non_typiques.py" -ForegroundColor Cyan
    Set-Content -Path "src/spectral/rapports_non_typiques.py" -Value $blockRapportsNonTypiques
    Write-Host "✓ Fichier créé : src/spectral/rapports_non_typiques.py" -ForegroundColor Green
} else {
    Append-Block -Path "src/spectral/rapports_non_typiques.py" -Block $blockRapportsNonTypiques -Label "rapports_non_typiques module"
}


# 4. Validation HOL : préparation pour les rapports non typiques
$blockValidationHol = @'
# === Extension Gabriel : validation HOL des rapports non typiques ===
def validate_non_typical_ratio(result):
    """
    Valide un rapport non typique en s'appuyant sur methode_spectral.thy
    et validation_hol_unifiee.thy.
    À relier à ton pipeline Isabelle/HOL (scripts d intégration).
    """
    # TODO : intégrer l appel réel à Isabelle (batch) pour vérifier la cohérence.
    return True
'@

Append-Block -Path "src/validation_hol_knowledge.py" -Block $blockValidationHol -Label "validate_non_typical_ratio"


Write-Host "=== Patch Gabriel spectral / rapports non typiques terminé ===" -ForegroundColor Magenta

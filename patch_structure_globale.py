# ============================================================
# Patch Structure Globale – Gabriel Multiloop
# Compatible avec transmission_un_clic.py
# ============================================================

import json

# Liste exacte fournie par Philippe (NE PAS MODIFIER)
FICHIERS = [
    "src/core/spectral_core.py",
    "src/core/pipeline.py",
    "src/core/plan_trifocal_avec_image.py",

    "src/complete_vision_system.py",
    "src/gabriel_vision_integration.py",
    "src/gabriel_image_interface.py",
    "src/advanced_vision_module.py",
    "src/advanced_analysis_criteria.py",

    "src/validation_hol_knowledge.py",
    "src/parametric_validation_module.py",
    "src/production_validation_system.py",

    "theories/methode_spectral.thy",
    "theories/validation_hol_unifiee.thy",

    "src/spectral/rapports_non_typiques.py",
    "src/spectral/reconstructor.py",
    "src/spectral/ratios.py",
    "src/spectral/non_typical_ratios.py",
    "src/spectral/digamma_pure.py",
    "src/spectral/tchebychev_savard_pipeline.py",
    "src/spectral/psi_savard.py"
]

# Génération du patch Dockerfile.cli
dockerfile_block = "# === Gabriel Patch : modules critiques ===\n"
for f in FICHIERS:
    if f.startswith("theories/"):
        dockerfile_block += f"COPY --chown=agent:agent {f} ./theories/\n"
    else:
        dockerfile_block += f"COPY --chown=agent:agent {f} ./{f}\n"

# Génération du patch docker-compose.yml
compose_block = ""
for f in FICHIERS:
    compose_block += f"      - ./{f}:/home/agent/app/{f}\n"

PATCH = {
    "operations": [
        {
            "type": "append_block",
            "file": "Dockerfile.cli",
            "label": "patch_dockerfile_cli",
            "block": dockerfile_block
        },
        {
            "type": "append_block",
            "file": "docker-compose.yml",
            "label": "patch_docker_compose",
            "block": compose_block
        }
    ]
}

with open("patch_structure_globale.json", "w", encoding="utf-8") as f:
    json.dump(PATCH, f, indent=4)

print("Patch structure globale généré : patch_structure_globale.json")

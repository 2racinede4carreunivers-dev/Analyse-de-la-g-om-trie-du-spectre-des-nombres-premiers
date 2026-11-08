#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APPLY_OPTIMIZATION.py - Applique la config optimisée à Gabriel

Changes:
- Ollama timeout: 60s -> 15s
- Multiloop iterations: 3 -> 2
- OpenAI prioritaire
- Cache activé
"""

import yaml
from pathlib import Path

config_file = Path(__file__).parent / "config.yaml"
optimized_file = Path(__file__).parent / "config_optimized.yaml"

print("[OPTIMIZATION] Applying performance tuning to Gabriel...")

# Load current config
with open(config_file, 'r') as f:
    config = yaml.safe_load(f) or {}

# Load optimized values
with open(optimized_file, 'r') as f:
    optimized = yaml.safe_load(f)

# Merge (optimized overwrites)
config.update(optimized)

# Save back
with open(config_file, 'w') as f:
    yaml.dump(config, f, default_flow_style=False)

print("[OK] Config updated!")
print()
print("Changes applied:")
print("  - Ollama timeout: 60s -> 15s (fallback faster)")
print("  - Multiloop iterations: 3 -> 2 (quicker refinement)")
print("  - Provider order: OpenAI first (faster)")
print("  - Cache enabled: Avoids recalculation")
print()
print("Expected latency:")
print("  - Simple question: ~5-10s (OpenAI)")
print("  - Spectral reconstruction: ~3-5s (direct calc)")
print("  - Complex multiloop: ~15-20s max")
print()
print("[INFO] Restart Docker to apply:")
print("  docker compose down")
print("  docker compose up")

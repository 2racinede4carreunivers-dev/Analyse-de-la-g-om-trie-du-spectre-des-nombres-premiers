#!/bin/bash
# Compile la validation principale methode_spectral.thy SEULE.
export HOME=/cygdrive/c/Users/Utilisateur
export LANG=en_US.UTF-8
export CHERE_INVOKING=true
ISABELLE_DIR=/cygdrive/c/Users/isabelle/Isabelle2025-2
export PATH="$ISABELLE_DIR/bin:$PATH"
cd /cygdrive/c/agent-multiloop-Gabriel-local/_build_methode_seule || exit 1
isabelle build -j1 -v -d . Methode_Spectrale_Seule
echo "BUILD_EXIT=$?"
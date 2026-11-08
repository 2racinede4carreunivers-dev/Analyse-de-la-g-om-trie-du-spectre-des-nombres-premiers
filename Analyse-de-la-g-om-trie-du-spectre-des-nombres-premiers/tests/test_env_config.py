"""Tests pour le diagnostic des fichiers .env + la commande env-check."""
from __future__ import annotations

import os
from pathlib import Path

import pytest

from src.core import config as config_module


def _find_repo_root() -> Path:
    """Trouve le repo root, que ce soit en local ou dans le container Docker.

    Cherche dans :
      1. Variable d'env GABRIEL_REPO_ROOT (override explicite)
      2. /app/agent-multiloop-Gabriel-local (chemin local de dev)
      3. /home/agent/app (chemin dans le container Docker)
      4. Path(__file__).parent.parent (relatif au fichier test)
    """
    env_root = os.environ.get("GABRIEL_REPO_ROOT")
    if env_root and Path(env_root).is_dir():
        return Path(env_root)
    for candidate in (
        Path("/app/agent-multiloop-Gabriel-local"),
        Path("/home/agent/app"),
        Path(__file__).resolve().parent.parent,
    ):
        if candidate.is_dir():
            return candidate
    return Path(__file__).resolve().parent.parent


REPO_ROOT = _find_repo_root()


# ==========================================================================
# Chargement automatique du .env de Gabriel
# ==========================================================================
class TestEnvLoading:
    def test_loaded_env_path_existe(self):
        """Le module config doit avoir charge un .env au demarrage."""
        # LOADED_ENV_PATH peut etre None si aucun .env n'existe
        # Mais ici on cree un .env canonique a /app/agent-multiloop-Gabriel-local/.env
        # donc il doit etre charge.
        expected_path = (REPO_ROOT / ".env").resolve()
        if expected_path.exists():
            assert config_module.LOADED_ENV_PATH is not None
            assert Path(config_module.LOADED_ENV_PATH).resolve() == expected_path

    def test_dotenv_charge_la_cle_groq(self):
        """Le fournisseur cloud configure doit etre charge depuis .env."""
        if not (REPO_ROOT / ".env").exists():
            pytest.skip(".env canonique absent")
        assert os.environ.get("GROQ_API_KEY") is not None


# ==========================================================================
# Contenu du .env canonique (presence des balises)
# ==========================================================================
class TestEnvContent:
    ENV_PATH = REPO_ROOT / ".env"

    # NOTE : il n'y a PAS de test qui verifie qu'un placeholder est present dans .env.
    # Ce serait absurde : le placeholder doit etre REMPLACE par la vraie cle utilisateur.
    # Si jamais on veut tester "la cle n'est pas un placeholder", c'est dans
    # src/adapters/llm/*.py qui detecte les placeholders et neutralise la cle.

    def test_groq_key_present(self):
        if not self.ENV_PATH.exists():
            pytest.skip(".env canonique absent")
        content = self.ENV_PATH.read_text(encoding="utf-8")
        assert "GROQ_API_KEY=" in content

    def test_ollama_host_present(self):
        if not self.ENV_PATH.exists():
            pytest.skip(".env canonique absent")
        content = self.ENV_PATH.read_text(encoding="utf-8")
        assert "OLLAMA_HOST=" in content
        assert "OLLAMA_MODEL=" in content

    def test_cloud_fallback_enabled(self):
        if not self.ENV_PATH.exists():
            pytest.skip(".env canonique absent")
        content = self.ENV_PATH.read_text(encoding="utf-8")
        assert "OLLAMA_ONLY=false" in content


# ==========================================================================
# Guide unique CONFIG_ENV_GUIDE.md
# ==========================================================================
class TestConfigGuide:
    GUIDE_PATH = REPO_ROOT / "CONFIG_ENV_GUIDE.md"

    def test_guide_existe(self):
        if not self.GUIDE_PATH.exists():
            pytest.skip(
                f"CONFIG_ENV_GUIDE.md non present a {self.GUIDE_PATH} "
                "(fichier optionnel - non monte dans le container Docker)"
            )
        assert self.GUIDE_PATH.exists()

    def test_guide_documente_le_mode_computationnel_desactive(self):
        if not self.GUIDE_PATH.exists():
            pytest.skip("CONFIG_ENV_GUIDE.md non present")
        content = self.GUIDE_PATH.read_text(encoding="utf-8")
        assert "COMPUTATIONAL_LLM_ENABLED=false" in content

    def test_guide_explique_chaine_llm(self):
        if not self.GUIDE_PATH.exists():
            pytest.skip("CONFIG_ENV_GUIDE.md non present")
        content = self.GUIDE_PATH.read_text(encoding="utf-8")
        assert "Ollama" in content
        assert "Groq" in content
        assert "Claude" in content
        assert "OpenAI" in content

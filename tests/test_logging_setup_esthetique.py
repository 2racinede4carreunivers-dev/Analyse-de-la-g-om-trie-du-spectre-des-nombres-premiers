"""
Tests pour la refonte esthétique du logging (v3.17).

Vérifie que :
- Par défaut, les logs INFO n'apparaissent PAS dans le terminal (stderr).
- Les logs INFO SONT écrits dans le fichier de log.
- Le mode verbose (GABRIEL_VERBOSE=1 ou verbose=True) rétablit les
  logs INFO au terminal.
- Les loggers réseau bavards (httpx, matplotlib, PIL) sont silencieux.
"""
from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.core.logging_setup import setup_logging, _env_verbose


@pytest.fixture(autouse=True)
def _cleanup_logging():
    """Reset root logger between tests."""
    yield
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)
        try:
            h.close()
        except Exception:
            pass


class TestEnvVerboseFlag:
    def test_default_false(self, monkeypatch):
        monkeypatch.delenv("GABRIEL_VERBOSE", raising=False)
        assert _env_verbose() is False

    @pytest.mark.parametrize("val", ["1", "true", "True", "TRUE", "yes", "on"])
    def test_truthy_values(self, monkeypatch, val):
        monkeypatch.setenv("GABRIEL_VERBOSE", val)
        assert _env_verbose() is True

    @pytest.mark.parametrize("val", ["0", "false", "no", "off", "", "  "])
    def test_falsy_values(self, monkeypatch, val):
        monkeypatch.setenv("GABRIEL_VERBOSE", val)
        assert _env_verbose() is False


class TestSilentByDefault:
    def test_console_handler_level_is_warning_by_default(self, tmp_path, monkeypatch):
        monkeypatch.delenv("GABRIEL_VERBOSE", raising=False)
        setup_logging(log_dir=tmp_path, verbose=False)

        root = logging.getLogger()
        # Il doit y avoir 2 handlers : file + console
        assert len(root.handlers) == 2
        levels = {h.__class__.__name__: h.level for h in root.handlers}
        assert levels.get("StreamHandler") == logging.WARNING, (
            f"Handler console doit filtrer à WARNING+ par défaut, "
            f"trouvé : {levels}"
        )
        # Le fichier doit rester à INFO pour capture complète
        assert levels.get("FileHandler") == logging.INFO

    def test_verbose_true_restores_info_on_console(self, tmp_path):
        setup_logging(log_dir=tmp_path, verbose=True)

        root = logging.getLogger()
        levels = {h.__class__.__name__: h.level for h in root.handlers}
        assert levels.get("StreamHandler") == logging.INFO, (
            "verbose=True doit remettre le StreamHandler à INFO"
        )

    def test_env_var_gabriel_verbose_activates_info(self, tmp_path, monkeypatch):
        monkeypatch.setenv("GABRIEL_VERBOSE", "1")
        setup_logging(log_dir=tmp_path, verbose=None)

        root = logging.getLogger()
        levels = {h.__class__.__name__: h.level for h in root.handlers}
        assert levels.get("StreamHandler") == logging.INFO


class TestFileHandlerCapturesInfo:
    def test_info_message_written_to_file(self, tmp_path):
        setup_logging(log_dir=tmp_path, verbose=False)
        log_file = tmp_path / "agent_cli.log"

        logging.getLogger("test.marker").info("MESSAGE_UNIQUE_ABCXYZ")

        # Flush handlers
        for h in logging.getLogger().handlers:
            h.flush()

        content = log_file.read_text(encoding="utf-8")
        assert "MESSAGE_UNIQUE_ABCXYZ" in content, (
            "Les logs INFO doivent TOUJOURS être écrits dans le fichier"
        )


class TestNoisyLoggersSilenced:
    def test_httpx_and_matplotlib_are_warning(self, tmp_path):
        setup_logging(log_dir=tmp_path, verbose=False)
        for name in ("httpx", "httpcore", "openai", "anthropic",
                     "urllib3", "matplotlib", "PIL"):
            level = logging.getLogger(name).level
            assert level >= logging.WARNING, (
                f"Logger '{name}' devrait être >= WARNING (silencieux), "
                f"trouvé level={level}"
            )


class TestMainInitBanner:
    """Verifie que main._rich_init_banner et main._rich_init_summary
    fonctionnent sans crasher (import et appel)."""

    def test_rich_init_banner_returns_console(self):
        # Import différé (main.py n'est pas dans src/)
        import importlib
        main_mod = importlib.import_module("main")
        console, _ = main_mod._rich_init_banner()
        # Rich est installé -> console doit être non-None
        assert console is not None

    def test_rich_init_summary_no_crash(self, tmp_path):
        import importlib
        import time
        main_mod = importlib.import_module("main")
        console, _ = main_mod._rich_init_banner()
        # Ne doit pas crasher
        main_mod._rich_init_summary(
            console,
            started_at=time.monotonic() - 0.5,
            log_path=tmp_path / "agent_cli.log",
            verbose=False,
        )
        main_mod._rich_init_summary(
            console,
            started_at=time.monotonic() - 0.5,
            log_path=tmp_path / "agent_cli.log",
            verbose=True,
        )

    def test_rich_init_summary_handles_none_console(self, tmp_path):
        """Si Rich indisponible, console=None -> pas de crash."""
        import importlib
        import time
        main_mod = importlib.import_module("main")
        # Ne doit pas crasher même si console est None
        main_mod._rich_init_summary(
            None,
            started_at=time.monotonic(),
            log_path=tmp_path / "agent_cli.log",
            verbose=False,
        )

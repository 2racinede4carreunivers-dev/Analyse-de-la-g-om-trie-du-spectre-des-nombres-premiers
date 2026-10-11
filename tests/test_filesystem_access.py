"""Tests filesystem_access (voir-image / lire / scan / analyser-image)."""
from __future__ import annotations

import os
import struct
import zlib
from pathlib import Path

import pytest

from src.core import filesystem_access as fa
from src.core.plan_trifocal_avec_image import PlanTrifocalAvecImage


# ------------------------------------------------------------------
# Helpers : cree une image PNG 4x4 sans dependance externe (via PIL).
# ------------------------------------------------------------------

def _make_png(path: Path, size: tuple[int, int] = (4, 4)) -> None:
    from PIL import Image
    img = Image.new("RGB", size, color=(128, 200, 64))
    img.save(path, format="PNG")


# ------------------------------------------------------------------
# lire_fichier
# ------------------------------------------------------------------

def test_lire_fichier_texte(tmp_path: Path) -> None:
    f = tmp_path / "test.md"
    f.write_text("Ligne 1\nLigne 2\nLigne 3\n", encoding="utf-8")
    r = fa.lire_fichier(str(f))
    assert r.total_lines == 3
    assert "Ligne 1" in r.content
    assert not r.truncated


def test_lire_fichier_troncation(tmp_path: Path) -> None:
    f = tmp_path / "gros.tex"
    f.write_text("\n".join(f"L{i}" for i in range(500)), encoding="utf-8")
    r = fa.lire_fichier(str(f), max_lignes=50)
    assert r.truncated
    assert r.lines_shown == 50
    assert "450 lignes supplementaires" in r.content


def test_lire_fichier_absent(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        fa.lire_fichier(str(tmp_path / "n_existe_pas.txt"))


# ------------------------------------------------------------------
# Windows path translation (regression : bug rapporte par Philippe)
# ------------------------------------------------------------------

def test_windows_path_non_mappe_leve_erreur_claire(monkeypatch) -> None:
    """Un chemin C:\\... sans mount doit lever FileNotFoundError avec
    un message d'aide clair (pas de fallback silencieux)."""
    monkeypatch.delenv("WINDOWS_MOUNT_MAP", raising=False)
    with pytest.raises(FileNotFoundError, match="Chemin Windows detecte"):
        fa.voir_image(r"C:\Users\Philippe\image_qui_nexiste_pas.png")


def test_windows_mount_map_env(tmp_path: Path, monkeypatch) -> None:
    """WINDOWS_MOUNT_MAP='C:=/tmp/mon-mount' doit rediriger C:\\... vers /tmp/mon-mount/..."""
    (tmp_path / "sub").mkdir()
    f = tmp_path / "sub" / "test.md"
    f.write_text("hello", encoding="utf-8")
    monkeypatch.setenv("WINDOWS_MOUNT_MAP", f"C:={tmp_path}")
    r = fa.lire_fichier("C:\\sub\\test.md")
    assert r.content.strip() == "hello"


def test_windows_theorie_savard_convention(tmp_path: Path, monkeypatch) -> None:
    """Le dossier canonique theorie-mathematique-philippe-thomas-savard-2026
    doit lever une erreur claire si aucun mount n'existe."""
    monkeypatch.delenv("WINDOWS_MOUNT_MAP", raising=False)
    with pytest.raises(FileNotFoundError, match="theorie-savard"):
        fa.voir_image(
            r"C:\theorie-mathematique-philippe-thomas-savard-2026\assets\images\x.png"
        )


def test_lire_fichier_refuse_binaire(tmp_path: Path) -> None:
    f = tmp_path / "binaire.dat"
    f.write_bytes(b"\x00\x01\x02\x03\x00" * 100)
    with pytest.raises(ValueError, match="binaire"):
        fa.lire_fichier(str(f))


def test_lire_fichier_refuse_binaire_avec_extension_texte(tmp_path: Path) -> None:
    """Un binaire renomme en .py doit etre refuse."""
    f = tmp_path / "programme.py"
    f.write_bytes(b"print('ok')\x00\x00 payload binaire")
    with pytest.raises(ValueError, match="binaire"):
        fa.lire_fichier(str(f))


def test_lire_fichier_borne_max_bytes(tmp_path: Path) -> None:
    """Un fichier avec une seule ligne enorme doit etre tronque en octets."""
    f = tmp_path / "enorme.md"
    # 200 KiB sur une seule ligne (aucun \n) : depasse DEFAULT_MAX_BYTES=128KiB
    f.write_text("a" * (200 * 1024), encoding="utf-8")
    r = fa.lire_fichier(str(f))
    assert r.truncated
    assert "tronque" in r.content
    # Le contenu doit etre borne autour de 128 KiB, pas 200 KiB
    assert len(r.content) < 150 * 1024


def test_lire_fichier_max_bytes_configurable(tmp_path: Path) -> None:
    f = tmp_path / "grand.txt"
    f.write_text("x" * 10_000, encoding="utf-8")
    r = fa.lire_fichier(str(f), max_bytes=1_000)
    assert r.truncated
    assert "tronque a 1000 octets" in r.content


# ------------------------------------------------------------------
# scanner_dossier
# ------------------------------------------------------------------

def test_scanner_dossier(tmp_path: Path) -> None:
    (tmp_path / "sub").mkdir()
    (tmp_path / "a.txt").write_text("aa")
    (tmp_path / "b.tex").write_text("bb")
    r = fa.scanner_dossier(str(tmp_path))
    names = [name for name, _, _ in r.entries]
    assert "sub" in names
    assert "a.txt" in names
    assert "b.tex" in names
    # Dossiers avant fichiers
    kinds = [kind for _, kind, _ in r.entries]
    assert kinds[0] == "dossier"


def test_scanner_dossier_pas_dossier(tmp_path: Path) -> None:
    f = tmp_path / "fichier.txt"
    f.write_text("x")
    with pytest.raises(NotADirectoryError):
        fa.scanner_dossier(str(f))


# ------------------------------------------------------------------
# voir_image
# ------------------------------------------------------------------

def test_voir_image_metadata(tmp_path: Path) -> None:
    p = tmp_path / "img.png"
    _make_png(p, size=(8, 8))
    r = fa.voir_image(str(p), cols=10)
    assert r.format == "PNG"
    assert r.size == (8, 8)
    assert r.file_size_bytes > 0
    assert r.ascii_preview  # non vide


def test_voir_image_absente(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        fa.voir_image(str(tmp_path / "manque.png"))


# ------------------------------------------------------------------
# analyser_image : necessite cle API valide
# ------------------------------------------------------------------

def test_analyser_image_sans_cle(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("CLAUDE_API_KEY", raising=False)
    p = tmp_path / "img.png"
    _make_png(p)
    with pytest.raises(RuntimeError, match="Cle Anthropic"):
        fa.analyser_image(str(p))


def test_analyser_image_placeholder_key(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "COLLEZ-VOTRE-CLE-ICI")
    p = tmp_path / "img.png"
    _make_png(p)
    with pytest.raises(RuntimeError, match="Cle Anthropic"):
        fa.analyser_image(str(p))


# ------------------------------------------------------------------
# PlanTrifocalAvecImage (cross-platform)
# ------------------------------------------------------------------

def test_plan_trifocal_via_env(tmp_path: Path, monkeypatch) -> None:
    p = tmp_path / "quad.png"
    _make_png(p)
    monkeypatch.setenv("TRIFOCAL_IMAGE_PATH", str(p))
    plan = PlanTrifocalAvecImage()
    assert plan.image_disponible
    assert plan.image_path == p


def test_plan_trifocal_absente(monkeypatch) -> None:
    monkeypatch.delenv("TRIFOCAL_IMAGE_PATH", raising=False)
    # Selon l'environnement, l'image peut exister via _DEFAULT_CANDIDATES.
    # On teste juste que la classe s'instancie sans erreur.
    plan = PlanTrifocalAvecImage()
    assert isinstance(plan.image_disponible, bool)


# ------------------------------------------------------------------
# Formatage
# ------------------------------------------------------------------

def test_format_scan(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text("x")
    r = fa.scanner_dossier(str(tmp_path))
    s = fa.format_scan(r)
    assert "a.md" in s
    assert "Contenu" in s


def test_format_file(tmp_path: Path) -> None:
    f = tmp_path / "t.py"
    f.write_text("print('ok')\n", encoding="utf-8")
    r = fa.lire_fichier(str(f))
    s = fa.format_file(r)
    assert "print('ok')" in s

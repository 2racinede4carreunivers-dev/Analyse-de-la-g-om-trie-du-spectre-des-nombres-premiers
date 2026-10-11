"""
Acces filesystem pour Gabriel : lecture de fichiers, scan de dossiers, affichage
et analyse d'images (Claude Vision).

Ce module donne a Gabriel la capacite d'atteindre les documents et fichiers
montes dans les volumes/conteneurs Docker (ex: /home/agent/app/data,
/home/agent/app/theories, /workspace/, etc.), et de decrire/analyser des
images en fournissant leur chemin.

Commandes CLI associees :
    voir-image <chemin>              -> apercu ASCII + metadonnees
    analyser-image <chemin> [question] -> analyse Claude Vision
    lire <chemin> [n_lignes]         -> lecture d'un fichier texte
    scan <chemin>                    -> liste un dossier
"""

from __future__ import annotations

import base64
import mimetypes
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from PIL import Image

# ------------------------------------------------------------------
# Constantes
# ------------------------------------------------------------------

# Extensions text-safe que l'on affiche en integralite (avec limite).
TEXT_EXTENSIONS = {
    ".txt", ".md", ".rst", ".log", ".csv", ".tsv",
    ".tex", ".bib", ".thy", ".ML",
    ".py", ".js", ".ts", ".jsx", ".tsx",
    ".html", ".css", ".xml", ".yaml", ".yml", ".toml", ".ini",
    ".json", ".env", ".cfg", ".sh", ".bat",
}

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tiff"}

# Taille max lue par defaut (128 KiB) pour eviter d'ecraser le terminal.
DEFAULT_MAX_BYTES = 128 * 1024
# Nombre max de lignes affichees si non specifie.
DEFAULT_MAX_LINES = 200

# Rampe ASCII (du plus sombre au plus clair) pour l'apercu image.
ASCII_RAMP = " .:-=+*#%@"


# ------------------------------------------------------------------
# Dataclasses de resultat
# ------------------------------------------------------------------

@dataclass
class FileReadResult:
    path: Path
    size_bytes: int
    lines_shown: int
    total_lines: int
    truncated: bool
    content: str
    encoding: str


@dataclass
class DirectoryScanResult:
    path: Path
    entries: list[tuple[str, str, int]]  # (name, kind, size)
    total_entries: int


@dataclass
class ImagePreviewResult:
    path: Path
    format: str
    mode: str
    size: tuple[int, int]
    file_size_bytes: int
    ascii_preview: str


# ------------------------------------------------------------------
# Utilitaires internes
# ------------------------------------------------------------------

def _resolve(chemin: str) -> Path:
    """Normalise un chemin utilisateur. Refuse les chemins vides.

    Traduit automatiquement les chemins Windows (C:\\..., D:\\...) vers les
    mounts Docker correspondants si la variable d'environnement
    WINDOWS_MOUNT_MAP est definie (format : 'C:=/host/c;D:=/host/d').
    Sinon, tente de mapper 'C:\\theorie-mathematique-philippe-thomas-savard-2026'
    vers /home/agent/app/theorie-savard/ (convention Gabriel).
    """
    if not chemin or not chemin.strip():
        raise ValueError("Chemin vide.")

    raw = chemin.strip().strip('"').strip("'")

    # Detection chemin Windows (C:\..., c:/..., D:\...) et traduction
    if len(raw) >= 3 and raw[1:3] in (":\\", ":/"):
        drive = raw[0].upper()
        rest = raw[3:].replace("\\", "/")
        # 1. Table de mapping depuis env
        env_map = os.environ.get("WINDOWS_MOUNT_MAP", "")
        mapping: dict[str, str] = {}
        for pair in env_map.split(";"):
            if "=" in pair:
                key, val = pair.split("=", 1)
                mapping[key.strip().rstrip(":").upper()] = val.strip()
        if drive in mapping:
            return Path(mapping[drive]) / rest
        # 2. Heuristique connue : dossier canonique de Philippe
        low = rest.lower()
        canonical_root = "theorie-mathematique-philippe-thomas-savard-2026"
        if low.startswith(canonical_root):
            sub = rest[len(canonical_root):].lstrip("/\\")
            # Emplacements possibles montes dans le conteneur
            for mount in ("/home/agent/app/theorie-savard",
                          "/home/agent/app/data/theorie-savard",
                          "/workspace/theorie-savard"):
                candidate = Path(mount) / sub if sub else Path(mount)
                if candidate.exists():
                    return candidate
            # Aucun mount trouve : leve une erreur explicite (pas de fallback)
            raise FileNotFoundError(
                f"Chemin Windows detecte '{raw}' mais aucun volume Docker ne "
                f"l'expose. Ajoutez dans docker-compose.yml :\n"
                f"  volumes:\n"
                f"    - C:/{canonical_root}:/home/agent/app/theorie-savard:ro\n"
                f"puis relancez : docker-compose down && docker-compose up"
            )
        # 3. Chemin Windows generique non mappe : erreur explicite
        raise FileNotFoundError(
            f"Chemin Windows detecte '{raw}' mais le lecteur '{drive}:' n'est "
            f"pas monte dans le conteneur Docker. Options :\n"
            f"  (a) definissez WINDOWS_MOUNT_MAP='{drive}=/chemin/docker' dans .env\n"
            f"  (b) ajoutez un volume dans docker-compose.yml exposant ce dossier\n"
            f"  (c) utilisez le chemin Docker direct (ex: /home/agent/app/...)"
        )

    return Path(raw).expanduser()


def _human_size(n: int) -> str:
    for unit in ("o", "Ko", "Mo", "Go"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} To"


# ------------------------------------------------------------------
# Lecture de fichier texte
# ------------------------------------------------------------------

def lire_fichier(chemin: str, max_lignes: int = DEFAULT_MAX_LINES,
                 max_bytes: int = DEFAULT_MAX_BYTES) -> FileReadResult:
    """Lit un fichier texte depuis n'importe quel chemin (volumes inclus).

    - Refuse les fichiers binaires (sondage des premiers octets, meme pour
      les extensions texte autorisees).
    - Borne la lecture a `max_bytes` (defaut 128 KiB) pour eviter de saturer
      la memoire quand une ligne est enorme.
    - Limite la sortie a `max_lignes` (defaut 200).
    """
    p = _resolve(chemin)
    if not p.exists():
        raise FileNotFoundError(f"Fichier introuvable : {p}")
    if not p.is_file():
        raise IsADirectoryError(f"'{p}' n'est pas un fichier (utilisez 'scan').")

    size = p.stat().st_size
    ext = p.suffix.lower()

    # Sonde binaire systematique (extension texte ou non) : un fichier
    # renomme en .py/.md mais contenant des NUL doit etre refuse.
    try:
        with open(p, "rb") as f:
            head = f.read(4096)
    except OSError as exc:
        raise RuntimeError(f"Impossible de lire {p} : {exc}") from exc
    if b"\x00" in head:
        raise ValueError(
            f"'{p}' semble binaire (octet NUL detecte). "
            "Utilisez 'voir-image' pour les images."
        )

    # Lecture bornee par max_bytes pour empecher qu'une ligne enorme
    # sature la memoire / le terminal.
    encoding = "utf-8"
    try:
        with open(p, "rb") as f:
            raw_bytes = f.read(max_bytes + 1)
    except OSError as exc:
        raise RuntimeError(f"Impossible de lire {p} : {exc}") from exc
    bytes_truncated = len(raw_bytes) > max_bytes
    if bytes_truncated:
        raw_bytes = raw_bytes[:max_bytes]
    raw = raw_bytes.decode(encoding, errors="replace")

    all_lines = raw.splitlines()
    total = len(all_lines) if not bytes_truncated else len(all_lines) + 1
    shown = all_lines[:max_lignes]
    truncated_lines = len(all_lines) > max_lignes
    truncated = truncated_lines or bytes_truncated

    content = "\n".join(shown)
    if truncated_lines:
        content += (
            f"\n\n... ({len(all_lines) - max_lignes} lignes supplementaires, "
            f"total_lu={len(all_lines)}. Augmentez max_lignes pour tout voir.)"
        )
    if bytes_truncated:
        content += (
            f"\n\n... (fichier tronque a {max_bytes} octets sur {size} au total. "
            "Augmentez max_bytes pour lire davantage.)"
        )

    return FileReadResult(
        path=p,
        size_bytes=size,
        lines_shown=len(shown),
        total_lines=total,
        truncated=truncated,
        content=content,
        encoding=encoding,
    )


# ------------------------------------------------------------------
# Scan de dossier (volumes montes)
# ------------------------------------------------------------------

def scanner_dossier(chemin: str, max_entries: int = 500) -> DirectoryScanResult:
    """Liste le contenu d'un dossier monte."""
    p = _resolve(chemin)
    if not p.exists():
        raise FileNotFoundError(f"Dossier introuvable : {p}")
    if not p.is_dir():
        raise NotADirectoryError(f"'{p}' n'est pas un dossier.")

    entries: list[tuple[str, str, int]] = []
    try:
        for child in sorted(p.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
            if child.is_symlink():
                kind = "symlink"
                sz = 0
            elif child.is_dir():
                kind = "dossier"
                sz = 0
            elif child.is_file():
                kind = "fichier"
                try:
                    sz = child.stat().st_size
                except OSError:
                    sz = 0
            else:
                kind = "autre"
                sz = 0
            entries.append((child.name, kind, sz))
            if len(entries) >= max_entries:
                break
    except PermissionError as exc:
        raise PermissionError(f"Acces refuse a {p} : {exc}") from exc

    return DirectoryScanResult(
        path=p, entries=entries, total_entries=len(entries),
    )


# ------------------------------------------------------------------
# Apercu image (ASCII + metadonnees)
# ------------------------------------------------------------------

def _ascii_preview(img: Image.Image, cols: int = 60, rows: int = 20) -> str:
    """Convertit une image PIL en apercu ASCII."""
    gray = img.convert("L")
    gray.thumbnail((cols, rows * 2))  # les pixels sont ~2x plus hauts que larges
    w, h = gray.size
    pixels = gray.load()
    lines = []
    for y in range(h):
        row = []
        for x in range(w):
            v = pixels[x, y]
            row.append(ASCII_RAMP[v * (len(ASCII_RAMP) - 1) // 255])
        lines.append("".join(row))
    return "\n".join(lines)


def voir_image(chemin: str, cols: int = 60) -> ImagePreviewResult:
    """Affiche les metadonnees + un apercu ASCII d'une image locale."""
    p = _resolve(chemin)
    if not p.exists():
        raise FileNotFoundError(f"Image introuvable : {p}")
    if not p.is_file():
        raise IsADirectoryError(f"'{p}' n'est pas un fichier.")
    ext = p.suffix.lower()
    if ext and ext not in IMAGE_EXTENSIONS:
        # On tente quand meme via PIL au cas ou (fichier sans extension).
        pass

    try:
        with Image.open(p) as img:
            img.load()
            fmt = img.format or "?"
            mode = img.mode
            size = img.size
            preview = _ascii_preview(img.copy(), cols=cols)
    except Exception as exc:
        raise RuntimeError(f"Impossible d'ouvrir l'image {p} : {exc}") from exc

    return ImagePreviewResult(
        path=p,
        format=fmt,
        mode=mode,
        size=size,
        file_size_bytes=p.stat().st_size,
        ascii_preview=preview,
    )


# ------------------------------------------------------------------
# Analyse image via Claude Vision
# ------------------------------------------------------------------

def analyser_image(
    chemin: str,
    question: Optional[str] = None,
    model: Optional[str] = None,
) -> str:
    """Envoie l'image a Claude (Vision) et retourne l'analyse texte.

    Pre-requis :
      - anthropic SDK installe.
      - Cle API valide dans ANTHROPIC_API_KEY ou CLAUDE_API_KEY.

    Retourne le texte d'analyse. Leve RuntimeError si la cle est absente
    ou si l'appel echoue.
    """
    p = _resolve(chemin)
    if not p.exists():
        raise FileNotFoundError(f"Image introuvable : {p}")
    if not p.is_file():
        raise IsADirectoryError(f"'{p}' n'est pas un fichier.")

    api_key = (
        os.environ.get("ANTHROPIC_API_KEY")
        or os.environ.get("CLAUDE_API_KEY")
    )
    if not api_key or api_key.startswith("COLLEZ"):
        raise RuntimeError(
            "Cle Anthropic manquante. Definissez ANTHROPIC_API_KEY "
            "(ou CLAUDE_API_KEY) dans .env avec une cle valide sk-ant-..."
        )

    mime, _ = mimetypes.guess_type(str(p))
    if not mime or not mime.startswith("image/"):
        # PIL detection de repli
        try:
            with Image.open(p) as img:
                fmt = (img.format or "PNG").lower()
                mime = f"image/{fmt}"
        except Exception:
            mime = "image/png"

    data_b64 = base64.standard_b64encode(p.read_bytes()).decode("ascii")

    prompt = question or (
        "Analyse cette image en detail (mathematique / scientifique / diagramme). "
        "Decris le contenu, les formules, les axes, les courbes, les textes visibles, "
        "et donne ton interpretation."
    )

    try:
        import anthropic
    except ImportError as exc:
        raise RuntimeError(
            "Le SDK 'anthropic' n'est pas installe. Executez : pip install anthropic"
        ) from exc

    client = anthropic.Anthropic(api_key=api_key)
    model_id = (
        model
        or os.environ.get("CLAUDE_MODEL")
        or "claude-sonnet-4-5-20250929"
    )

    try:
        response = client.messages.create(
            model=model_id,
            max_tokens=1500,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": mime,
                                "data": data_b64,
                            },
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        )
    except Exception as exc:
        raise RuntimeError(f"Appel Claude Vision echoue : {exc}") from exc

    # Concatene les blocs texte de la reponse
    parts = []
    for block in response.content:
        # anthropic renvoie des objets typed avec .text
        text = getattr(block, "text", None)
        if text:
            parts.append(text)
    return "\n".join(parts).strip() or "(reponse vide)"


# ------------------------------------------------------------------
# Formatage humain pour la CLI
# ------------------------------------------------------------------

def format_scan(result: DirectoryScanResult) -> str:
    """Formatage compact d'un scan de dossier."""
    lines = [f"[bold]Contenu de {result.path}[/bold]  ({result.total_entries} entrees)"]
    for name, kind, sz in result.entries:
        if kind == "dossier":
            lines.append(f"  [cyan]{name}/[/cyan]")
        elif kind == "fichier":
            lines.append(f"  [white]{name}[/white]  [dim]{_human_size(sz)}[/dim]")
        else:
            lines.append(f"  [yellow]{name}[/yellow]  [dim]({kind})[/dim]")
    return "\n".join(lines)


def format_file(result: FileReadResult) -> str:
    """Formatage d'un fichier lu."""
    header = (
        f"[bold]{result.path}[/bold]   "
        f"[dim]{_human_size(result.size_bytes)} | "
        f"{result.lines_shown}/{result.total_lines} lignes"
        + ("  TRONQUE" if result.truncated else "")
        + "[/dim]"
    )
    return header + "\n" + result.content


def format_image(result: ImagePreviewResult) -> str:
    """Formatage d'un apercu image."""
    header = (
        f"[bold]{result.path}[/bold]\n"
        f"  Format  : {result.format}\n"
        f"  Mode    : {result.mode}\n"
        f"  Taille  : {result.size[0]} x {result.size[1]} px\n"
        f"  Poids   : {_human_size(result.file_size_bytes)}"
    )
    return header + "\n\n[dim]Apercu ASCII :[/dim]\n" + result.ascii_preview

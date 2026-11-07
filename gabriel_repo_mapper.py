#!/usr/bin/env python3
# =============================================================================
#  gabriel_repo_mapper.py
#  Cartographe du dépôt Gabriel — Préambule du pipeline cognitif
#  Auteur  : Pipeline cognitif — Théorie L'Univers est au Carré
#  Dépôt   : C:\agent-multiloop-Gabriel-local-final
#  Usage   : python gabriel_repo_mapper.py
#          : python gabriel_repo_mapper.py --root "C:\agent-multiloop-Gabriel-local-final"
#  Sortie  : gabriel_repo_map.json  +  gabriel_repo_report.md
# =============================================================================

import os
import re
import sys
import json
import argparse
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ─────────────────────────────────────────────────────────────────────────────
#  CONFIGURATION : extensions analysées et leurs patterns de liens internes
# ─────────────────────────────────────────────────────────────────────────────

EXTENSIONS_ANALYSEES = {
    # Python
    ".py":   "python",
    # Isabelle / HOL
    ".thy":  "isabelle",
    # Données / config
    ".json": "json",
    ".yaml": "yaml",
    ".yml":  "yaml",
    ".toml": "toml",
    ".env":  "env",
    ".ini":  "ini",
    ".cfg":  "ini",
    # Texte / doc
    ".md":   "markdown",
    ".txt":  "texte",
    ".rst":  "texte",
    # Base de données
    ".db":   "sqlite",
    ".sql":  "sql",
    # LaTeX
    ".tex":  "latex",
    ".bib":  "latex",
    # Shell
    ".sh":   "shell",
    ".bash": "shell",
    # Autres code
    ".js":   "javascript",
    ".ts":   "javascript",
    ".html": "html",
    ".css":  "css",
}

# Dossiers à ignorer (caches, venv, git, etc.)
DOSSIERS_IGNORES = {
    "__pycache__", ".git", ".hg", ".svn", "node_modules",
    ".venv", "venv", "env", ".env", ".mypy_cache",
    ".pytest_cache", "dist", "build", ".eggs", ".tox",
    ".idea", ".vscode", "__MACOSX",
}

# Extensions binaires ou non-texte à ne pas lire
EXTENSIONS_BINAIRES = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".ico",
    ".pdf", ".docx", ".xlsx", ".pptx", ".odt", ".ods",
    ".zip", ".tar", ".gz", ".bz2", ".7z", ".rar",
    ".mp3", ".mp4", ".wav", ".avi", ".mov",
    ".exe", ".dll", ".so", ".dylib", ".bin", ".pkl", ".pyc",
    ".whl", ".egg",
}


# ─────────────────────────────────────────────────────────────────────────────
#  EXTRACTEURS DE RÉFÉRENCES PAR TYPE DE FICHIER
# ─────────────────────────────────────────────────────────────────────────────

def extraire_refs_python(contenu: str, fichier_courant: Path) -> list[dict]:
    """Extrait toutes les références inter-fichiers d'un script Python."""
    refs = []

    # import module / from module import ...
    for m in re.finditer(
        r'^\s*(?:from|import)\s+([\w\.]+)',
        contenu, re.MULTILINE
    ):
        refs.append({"type": "import_module", "cible": m.group(1), "ligne": contenu[:m.start()].count('\n') + 1})

    # open("chemin") ou open('chemin')
    for m in re.finditer(
        r'\bopen\s*\(\s*["\']([^"\']+)["\']',
        contenu
    ):
        refs.append({"type": "open_fichier", "cible": m.group(1), "ligne": contenu[:m.start()].count('\n') + 1})

    # Path("...") ou pathlib
    for m in re.finditer(
        r'\bPath\s*\(\s*["\']([^"\']+)["\']',
        contenu
    ):
        refs.append({"type": "Path()", "cible": m.group(1), "ligne": contenu[:m.start()].count('\n') + 1})

    # os.path.join / os.path constructions
    for m in re.finditer(
        r'os\.path\.[a-z]+\s*\(\s*["\']([^"\']+)["\']',
        contenu
    ):
        refs.append({"type": "os.path", "cible": m.group(1), "ligne": contenu[:m.start()].count('\n') + 1})

    # Chaînes ressemblant à des chemins relatifs ou absolus
    for m in re.finditer(
        r'["\'](\./[^\'"]+|/[^\'"]{4,}|[^\'"]+\.(py|thy|json|yaml|yml|db|txt|md|env|toml|sh|sql))["\']',
        contenu
    ):
        chemin = m.group(1)
        if chemin not in [r["cible"] for r in refs]:
            refs.append({"type": "chemin_litteral", "cible": chemin, "ligne": contenu[:m.start()].count('\n') + 1})

    # sqlite3.connect("...") ou create_engine("sqlite:///...")
    for m in re.finditer(
        r'(?:sqlite3\.connect|create_engine)\s*\(\s*["\']([^"\']+)["\']',
        contenu
    ):
        refs.append({"type": "base_donnees", "cible": m.group(1), "ligne": contenu[:m.start()].count('\n') + 1})

    # subprocess / os.system avec fichiers
    for m in re.finditer(
        r'(?:subprocess|os\.system|os\.popen)\s*[\.(]\s*["\']([^"\']+)["\']',
        contenu
    ):
        refs.append({"type": "subprocess", "cible": m.group(1), "ligne": contenu[:m.start()].count('\n') + 1})

    return refs


def extraire_refs_isabelle(contenu: str, fichier_courant: Path) -> list[dict]:
    """Extrait les dépendances d'un fichier Isabelle/HOL (.thy)."""
    refs = []

    # theory NomThéorie imports Dep1 Dep2 ...
    m = re.search(r'\btheory\s+(\w+)\s+imports\s+([\w\s"~./]+?)(?:\s+begin)', contenu, re.DOTALL)
    if m:
        nom_theory = m.group(1)
        imports_brut = m.group(2)
        for imp in re.findall(r'[\w~./]+|"[^"]+"', imports_brut):
            imp = imp.strip('"')
            if imp and not imp.startswith('~'):
                refs.append({"type": "thy_import", "cible": imp, "ligne": contenu[:m.start()].count('\n') + 1})
            elif imp.startswith('~'):
                refs.append({"type": "thy_import_HOL_stdlib", "cible": imp, "ligne": contenu[:m.start()].count('\n') + 1})

    # uses "fichier.ML"
    for m in re.finditer(r'\buses\s+"([^"]+)"', contenu):
        refs.append({"type": "thy_uses", "cible": m.group(1), "ligne": contenu[:m.start()].count('\n') + 1})

    # Références croisées entre fichiers thy (mentions de théories)
    for m in re.finditer(r'\b([A-Z][a-zA-Z_0-9]+)\.([a-z_][a-zA-Z_0-9]*)\b', contenu):
        refs.append({"type": "thy_ref_croisee", "cible": m.group(1), "membre": m.group(2),
                     "ligne": contenu[:m.start()].count('\n') + 1})

    return refs


def extraire_refs_json(contenu: str, fichier_courant: Path) -> list[dict]:
    """Détecte les chemins dans un fichier JSON."""
    refs = []
    for m in re.finditer(
        r'"([^"]*(?:\.py|\.thy|\.json|\.yaml|\.yml|\.db|\.txt|\.md|\.sh|\.env|\.sql)[^"]*)"',
        contenu
    ):
        refs.append({"type": "json_chemin", "cible": m.group(1), "ligne": contenu[:m.start()].count('\n') + 1})
    return refs


def extraire_refs_yaml(contenu: str, fichier_courant: Path) -> list[dict]:
    """Détecte les chemins dans un fichier YAML."""
    refs = []
    for m in re.finditer(
        r':\s+["\']?([./][^\s\'"#]+|[\w_-]+(?:\.py|\.thy|\.json|\.db|\.yaml|\.sh))["\']?',
        contenu
    ):
        refs.append({"type": "yaml_chemin", "cible": m.group(1), "ligne": contenu[:m.start()].count('\n') + 1})
    return refs


def extraire_refs_shell(contenu: str, fichier_courant: Path) -> list[dict]:
    """Détecte les appels de fichiers dans des scripts shell."""
    refs = []
    for m in re.finditer(
        r'(?:source|\.|\bpython3?\b|\bbash\b|\bsh\b)\s+([./]?[\w./_-]+(?:\.py|\.sh|\.bash|\.env)?)',
        contenu
    ):
        refs.append({"type": "shell_appel", "cible": m.group(1), "ligne": contenu[:m.start()].count('\n') + 1})
    return refs


def extraire_refs_latex(contenu: str, fichier_courant: Path) -> list[dict]:
    """Détecte les inclusions LaTeX."""
    refs = []
    for m in re.finditer(
        r'\\(?:input|include|bibliography|usepackage|includegraphics)\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}',
        contenu
    ):
        refs.append({"type": "latex_inclusion", "cible": m.group(1), "ligne": contenu[:m.start()].count('\n') + 1})
    return refs


def extraire_refs_generique(contenu: str, fichier_courant: Path) -> list[dict]:
    """Extracteur générique : capture les chemins relatifs ou absolus."""
    refs = []
    for m in re.finditer(
        r'(?:^|[\s=:"\'(,])(\./[^\s\'")\]]+|/[\w/_.-]{5,}|[\w._-]+\.(?:py|thy|json|yaml|yml|db|sh|env|sql|md|txt))',
        contenu, re.MULTILINE
    ):
        cible = m.group(1).strip()
        if len(cible) > 3:
            refs.append({"type": "ref_generique", "cible": cible, "ligne": contenu[:m.start()].count('\n') + 1})
    return refs


# Dispatch par type de fichier
EXTRACTEURS = {
    "python":     extraire_refs_python,
    "isabelle":   extraire_refs_isabelle,
    "json":       extraire_refs_json,
    "yaml":       extraire_refs_yaml,
    "shell":      extraire_refs_shell,
    "latex":      extraire_refs_latex,
    "toml":       extraire_refs_generique,
    "env":        extraire_refs_generique,
    "ini":        extraire_refs_generique,
    "markdown":   extraire_refs_generique,
    "texte":      extraire_refs_generique,
    "sql":        extraire_refs_generique,
    "html":       extraire_refs_generique,
    "javascript": extraire_refs_generique,
    "css":        lambda c, f: [],
    "sqlite":     lambda c, f: [],
}


# ─────────────────────────────────────────────────────────────────────────────
#  FONCTIONS UTILITAIRES
# ─────────────────────────────────────────────────────────────────────────────

def taille_humaine(octets: int) -> str:
    for unite in ["o", "Ko", "Mo", "Go"]:
        if octets < 1024:
            return f"{octets:.1f} {unite}"
        octets /= 1024
    return f"{octets:.1f} To"


def hash_fichier(chemin: Path) -> str:
    try:
        h = hashlib.md5()
        with open(chemin, "rb") as f:
            for bloc in iter(lambda: f.read(8192), b""):
                h.update(bloc)
        return h.hexdigest()[:12]
    except Exception:
        return "N/A"


def lire_fichier(chemin: Path) -> str | None:
    """Tente de lire un fichier texte avec plusieurs encodages."""
    for enc in ["utf-8", "latin-1", "cp1252"]:
        try:
            return chemin.read_text(encoding=enc)
        except (UnicodeDecodeError, PermissionError):
            continue
    return None


def arbre_texte(noeud: dict, prefixe: str = "", est_dernier: bool = True) -> list[str]:
    """Génère une représentation arborescente ASCII."""
    lignes = []
    connecteur = "└── " if est_dernier else "├── "
    lignes.append(f"{prefixe}{connecteur}{noeud['nom']}")
    if noeud.get("enfants"):
        extension = "    " if est_dernier else "│   "
        for i, enfant in enumerate(noeud["enfants"]):
            est_der = (i == len(noeud["enfants"]) - 1)
            lignes.extend(arbre_texte(enfant, prefixe + extension, est_der))
    return lignes


# ─────────────────────────────────────────────────────────────────────────────
#  EXPLORATEUR PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

class CartographeDepot:
    def __init__(self, racine: Path):
        self.racine = racine.resolve()
        self.fichiers: dict[str, dict] = {}       # chemin_relatif → métadonnées
        self.arborescence: dict = {}              # arbre hiérarchique
        self.graphe_liens: dict[str, list] = defaultdict(list)  # source → [liens]
        self.index_par_type: dict[str, list] = defaultdict(list)
        self.refs_cassees: list[dict] = []
        self.stats: dict = {}

    def _doit_ignorer(self, chemin: Path) -> bool:
        return any(partie in DOSSIERS_IGNORES for partie in chemin.parts)

    def _construire_arbre(self, dossier: Path) -> dict:
        nom = dossier.name or str(dossier)
        noeud = {"nom": nom, "type": "dossier", "chemin": str(dossier.relative_to(self.racine)), "enfants": []}
        try:
            entrees = sorted(dossier.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        except PermissionError:
            return noeud
        for entree in entrees:
            if self._doit_ignorer(entree):
                continue
            if entree.is_dir():
                noeud["enfants"].append(self._construire_arbre(entree))
            elif entree.is_file():
                noeud["enfants"].append({
                    "nom": entree.name,
                    "type": "fichier",
                    "chemin": str(entree.relative_to(self.racine)),
                })
        return noeud

    def explorer(self, verbeux: bool = True):
        print(f"\n{'='*70}")
        print(f"  CARTOGRAPHE DU DÉPÔT GABRIEL")
        print(f"  Racine  : {self.racine}")
        print(f"  Démarré : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")

        # 1. Arborescence
        if verbeux:
            print("  [1/3] Construction de l'arborescence...")
        self.arborescence = self._construire_arbre(self.racine)

        # 2. Analyse de chaque fichier
        if verbeux:
            print("  [2/3] Analyse des fichiers et extraction des liens...")

        tous_fichiers = list(self.racine.rglob("*"))
        nb_total = sum(1 for f in tous_fichiers if f.is_file() and not self._doit_ignorer(f))
        traites = 0

        for chemin in sorted(tous_fichiers):
            if not chemin.is_file():
                continue
            if self._doit_ignorer(chemin):
                continue

            relatif = str(chemin.relative_to(self.racine))
            ext = chemin.suffix.lower()
            type_fichier = EXTENSIONS_ANALYSEES.get(ext, "autre")

            meta = {
                "chemin_relatif": relatif,
                "chemin_absolu":  str(chemin),
                "nom":            chemin.name,
                "extension":      ext,
                "type":           type_fichier,
                "taille_octets":  chemin.stat().st_size,
                "taille_humaine": taille_humaine(chemin.stat().st_size),
                "hash_md5":       hash_fichier(chemin),
                "modifie":        datetime.fromtimestamp(chemin.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                "refs_sortantes": [],
                "lisible":        True,
            }

            # Lecture et extraction des références
            if ext not in EXTENSIONS_BINAIRES:
                contenu = lire_fichier(chemin)
                if contenu is not None:
                    extracteur = EXTRACTEURS.get(type_fichier, lambda c, f: [])
                    try:
                        refs = extracteur(contenu, chemin)
                        # Dédoublonnage
                        vues = set()
                        refs_uniques = []
                        for r in refs:
                            cle = (r["type"], r["cible"])
                            if cle not in vues:
                                vues.add(cle)
                                refs_uniques.append(r)
                        meta["refs_sortantes"] = refs_uniques
                        meta["nb_lignes"] = contenu.count('\n') + 1
                    except Exception as e:
                        meta["erreur_extraction"] = str(e)
                else:
                    meta["lisible"] = False
            else:
                meta["lisible"] = False
                meta["binaire"] = True

            self.fichiers[relatif] = meta
            self.index_par_type[type_fichier].append(relatif)
            traites += 1

            if verbeux and traites % 20 == 0:
                print(f"      → {traites}/{nb_total} fichiers analysés...")

        print(f"      → {traites}/{nb_total} fichiers analysés. ✓")

        # 3. Résolution des liens (vérification existence)
        if verbeux:
            print("  [3/3] Résolution et validation des liens inter-fichiers...")

        tous_relatifs = set(self.fichiers.keys())

        for relatif, meta in self.fichiers.items():
            chemin_source = self.racine / relatif
            for ref in meta["refs_sortantes"]:
                cible_brut = ref["cible"]

                # Tentatives de résolution
                candidats = self._resoudre_cible(cible_brut, chemin_source)

                ref["candidats_resolus"] = candidats
                if candidats:
                    ref["resolu"] = True
                    ref["cible_resolue"] = candidats[0]
                    # Enregistrer dans le graphe
                    self.graphe_liens[relatif].append({
                        "cible":  candidats[0],
                        "type":   ref["type"],
                        "ligne":  ref.get("ligne", 0),
                    })
                else:
                    ref["resolu"] = False
                    ref["cible_resolue"] = None
                    # Référence potentiellement cassée (sauf imports stdlib)
                    if ref["type"] not in ("import_module", "thy_import_HOL_stdlib", "thy_ref_croisee"):
                        self.refs_cassees.append({
                            "source": relatif,
                            "cible_brute": cible_brut,
                            "type": ref["type"],
                            "ligne": ref.get("ligne", 0),
                        })

        # 4. Statistiques
        self._calculer_stats(nb_total)
        print(f"\n  Cartographie terminée ✓\n")

    def _resoudre_cible(self, cible: str, source: Path) -> list[str]:
        """Tente de résoudre une référence en chemin relatif réel dans le dépôt."""
        candidats = []
        # Nettoyage
        cible = cible.strip().strip('"\'').strip()

        # 1. Chemin absolu direct
        if os.path.isabs(cible):
            p = Path(cible)
            if p.exists():
                try:
                    candidats.append(str(p.relative_to(self.racine)))
                except ValueError:
                    candidats.append(str(p))
            return candidats

        # 2. Relatif au fichier source
        essais = [
            source.parent / cible,
            self.racine / cible,
        ]
        # 3. Suffixes manquants courants
        for base in list(essais):
            for ext in [".py", ".thy", ".json", ".yaml", ".yml", ".db", ".sh", ".md", ".txt"]:
                essais.append(Path(str(base) + ext))

        for essai in essais:
            try:
                r = essai.resolve()
                if r.exists():
                    try:
                        rel = str(r.relative_to(self.racine))
                        if rel not in candidats:
                            candidats.append(rel)
                    except ValueError:
                        pass
            except (OSError, ValueError):
                pass

        # 4. Recherche par nom de fichier dans tout le dépôt (nom seul, sans chemin)
        nom_seul = Path(cible).name
        if nom_seul and '/' not in cible and '\\' not in cible:
            for f in self.fichiers:
                if Path(f).name == nom_seul or Path(f).stem == nom_seul:
                    if f not in candidats:
                        candidats.append(f)

        return candidats[:3]  # max 3 candidats

    def _calculer_stats(self, nb_total: int):
        nb_liens = sum(len(v) for v in self.graphe_liens.values())
        self.stats = {
            "racine":             str(self.racine),
            "date_analyse":       datetime.now().isoformat(),
            "nb_fichiers_total":  nb_total,
            "nb_types": {
                t: len(lst) for t, lst in self.index_par_type.items()
            },
            "nb_liens_resolus":   nb_liens,
            "nb_refs_cassees":    len(self.refs_cassees),
            "fichiers_les_plus_connectes": sorted(
                [(f, len(v)) for f, v in self.graphe_liens.items()],
                key=lambda x: x[1], reverse=True
            )[:10],
        }

    # ──────────────────────────────────────────────────────────────────────────
    #  EXPORT JSON
    # ──────────────────────────────────────────────────────────────────────────

    def exporter_json(self, chemin_sortie: Path):
        donnees = {
            "meta":          self.stats,
            "arborescence":  self.arborescence,
            "fichiers":      self.fichiers,
            "graphe_liens":  dict(self.graphe_liens),
            "refs_cassees":  self.refs_cassees,
            "index_par_type": dict(self.index_par_type),
        }
        with open(chemin_sortie, "w", encoding="utf-8") as f:
            json.dump(donnees, f, ensure_ascii=False, indent=2)
        print(f"  [JSON] Sauvegardé → {chemin_sortie}")

    # ──────────────────────────────────────────────────────────────────────────
    #  EXPORT RAPPORT MARKDOWN
    # ──────────────────────────────────────────────────────────────────────────

    def exporter_rapport_markdown(self, chemin_sortie: Path):
        lignes = []
        s = self.stats
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lignes += [
            "# Rapport de cartographie du dépôt Gabriel",
            f"**Racine analysée :** `{s['racine']}`  ",
            f"**Date :** {now}  ",
            f"**Fichiers analysés :** {s['nb_fichiers_total']}  ",
            f"**Liens résolus :** {s['nb_liens_resolus']}  ",
            f"**Références potentiellement cassées :** {s['nb_refs_cassees']}",
            "",
            "---",
            "",
            "## 1. Arborescence complète",
            "```",
            str(self.racine),
        ]
        # Arbre ASCII
        for enfant in self.arborescence.get("enfants", []):
            est_der = (enfant == self.arborescence["enfants"][-1])
            lignes.extend(arbre_texte(enfant, "", est_der))
        lignes += ["```", ""]

        # ── Répartition par type
        lignes += ["## 2. Répartition des fichiers par type", ""]
        lignes.append("| Type | Nombre de fichiers |")
        lignes.append("|------|--------------------|")
        for t, n in sorted(s["nb_types"].items(), key=lambda x: -x[1]):
            lignes.append(f"| {t} | {n} |")
        lignes.append("")

        # ── Top fichiers connectés
        lignes += ["## 3. Fichiers les plus connectés (hub du dépôt)", ""]
        lignes.append("| Fichier | Liens sortants résolus |")
        lignes.append("|---------|------------------------|")
        for f, n in s["fichiers_les_plus_connectes"]:
            lignes.append(f"| `{f}` | {n} |")
        lignes.append("")

        # ── Graphe des liens par fichier
        lignes += ["## 4. Graphe des liens inter-fichiers", ""]
        for source, liens in sorted(self.graphe_liens.items()):
            if not liens:
                continue
            lignes.append(f"### `{source}`")
            lignes.append(f"*{len(liens)} lien(s) sortant(s)*")
            lignes.append("")
            lignes.append("| Type de lien | Fichier cible | Ligne |")
            lignes.append("|-------------|---------------|-------|")
            for lien in liens:
                lignes.append(f"| `{lien['type']}` | `{lien['cible']}` | {lien['ligne']} |")
            lignes.append("")

        # ── Références cassées
        lignes += ["## 5. Références potentiellement non résolues", ""]
        if self.refs_cassees:
            lignes.append("| Fichier source | Référence | Type | Ligne |")
            lignes.append("|---------------|-----------|------|-------|")
            for r in self.refs_cassees:
                lignes.append(f"| `{r['source']}` | `{r['cible_brute']}` | `{r['type']}` | {r['ligne']} |")
        else:
            lignes.append("*Aucune référence cassée détectée.*")
        lignes.append("")

        # ── Détail par fichier
        lignes += ["## 6. Détail complet par fichier", ""]
        for relatif, meta in sorted(self.fichiers.items()):
            lignes.append(f"### `{relatif}`")
            lignes.append(f"- **Type :** {meta['type']}")
            lignes.append(f"- **Taille :** {meta['taille_humaine']}")
            lignes.append(f"- **Modifié :** {meta['modifie']}")
            if meta.get("nb_lignes"):
                lignes.append(f"- **Lignes :** {meta['nb_lignes']}")
            lignes.append(f"- **Hash MD5 :** `{meta['hash_md5']}`")
            refs = meta.get("refs_sortantes", [])
            if refs:
                lignes.append(f"- **Références sortantes ({len(refs)}) :**")
                for r in refs:
                    statut = "✅" if r.get("resolu") else "❓"
                    cible_res = r.get("cible_resolue") or r["cible"]
                    lignes.append(f"  - {statut} `{r['type']}` → `{cible_res}` *(l.{r.get('ligne', '?')})*")
            else:
                lignes.append("- **Références sortantes :** *(aucune)*")
            lignes.append("")

        with open(chemin_sortie, "w", encoding="utf-8") as f:
            f.write("\n".join(lignes))
        print(f"  [MARKDOWN] Sauvegardé → {chemin_sortie}")


# ─────────────────────────────────────────────────────────────────────────────
#  POINT D'ENTRÉE
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Cartographe du dépôt Gabriel — arborescence + graphe des liens internes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples :
  # Lancement direct (chemin Gabriel déjà configuré) :
  python gabriel_repo_mapper.py

  # Avec chemin explicite :
  python gabriel_repo_mapper.py --root "C:\agent-multiloop-Gabriel-local-final"

  # Avec dossier de sortie séparé :
  python gabriel_repo_mapper.py --root "C:\agent-multiloop-Gabriel-local-final" --out "C:\agent-multiloop-Gabriel-local-final\rapports"

  # Mode silencieux :
  python gabriel_repo_mapper.py --silencieux
        """
    )
    parser.add_argument(
        "--root", "-r",
        default=r"C:\agent-multiloop-Gabriel-local-final",
        help="Chemin racine du dépôt Gabriel à analyser (défaut : C:\\agent-multiloop-Gabriel-local-final)"
    )
    parser.add_argument(
        "--out", "-o",
        default=None,
        help="Dossier de sortie pour les rapports (défaut : même dossier que --root)"
    )
    parser.add_argument(
        "--silencieux", "-s",
        action="store_true",
        help="Supprime les messages de progression"
    )
    parser.add_argument(
        "--json-seulement",
        action="store_true",
        help="Génère uniquement le fichier JSON (pas le rapport Markdown)"
    )

    args = parser.parse_args()

    racine = Path(args.root)
    if not racine.exists():
        print(f"ERREUR : Le chemin '{racine}' n'existe pas.", file=sys.stderr)
        sys.exit(1)

    dossier_sortie = Path(args.out) if args.out else racine
    dossier_sortie.mkdir(parents=True, exist_ok=True)

    json_sortie = dossier_sortie / "gabriel_repo_map.json"
    md_sortie   = dossier_sortie / "gabriel_repo_report.md"

    carto = CartographeDepot(racine)
    carto.explorer(verbeux=not args.silencieux)

    # Exports
    carto.exporter_json(json_sortie)
    if not args.json_seulement:
        carto.exporter_rapport_markdown(md_sortie)

    # Résumé final
    s = carto.stats
    print(f"\n{'─'*70}")
    print(f"  RÉSUMÉ FINAL")
    print(f"{'─'*70}")
    print(f"  Fichiers analysés   : {s['nb_fichiers_total']}")
    print(f"  Liens résolus       : {s['nb_liens_resolus']}")
    print(f"  Réfs non résolues   : {s['nb_refs_cassees']}")
    print(f"  Fichiers générés    :")
    print(f"    → {json_sortie}")
    if not args.json_seulement:
        print(f"    → {md_sortie}")
    print(f"{'─'*70}")
    print(f"\n  ✅ gabriel_repo_map.json est prêt — le pipeline Python peut")
    print(f"     charger ce fichier pour connaître toutes les adresses du dépôt.")
    print(f"\n  Usage dans le pipeline :")
    print(f"    import json")
    print(f"    with open('gabriel_repo_map.json') as f:")
    print(f"        repo = json.load(f)")
    print(f"    # Accès au graphe :")
    print(f"    liens = repo['graphe_liens']")
    print(f"    fichiers = repo['fichiers']")
    print()


if __name__ == "__main__":
    main()

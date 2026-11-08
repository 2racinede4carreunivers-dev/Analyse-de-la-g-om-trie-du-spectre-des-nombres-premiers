#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib, json, os, shutil, sqlite3, sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT   = Path(os.getcwd()).resolve()
DB_PATH     = REPO_ROOT / "data" / "gabriel_repo_map.db"
RAPPORT_DIR = REPO_ROOT / "pipeline_correction"
SNAPSHOT_ID = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
BAK_DIR     = REPO_ROOT / ".gabriel_variateur" / "snapshots" / (SNAPSHOT_ID + "_hol_unicode_fix")

CORRECTIONS = [
    ("FIX_RIGHTARROW", "\u21d2".encode("utf-8"), b"\\<Rightarrow>",
     "U+21D2 (fleche double) -> \\<Rightarrow>  [consts/definition/types]"),
    ("FIX_NOTEQ", "\u2260".encode("utf-8"), b"\\<noteq>",
     "U+2260 (non-egal)      -> \\<noteq>        [assumes/axiomatization]"),
]

EXCLUDE = {".git", ".venv", "venv", "__pycache__", ".gabriel_variateur",
           "node_modules", "dist", "build", "tmp", "temp", ".github"}

SEP = "=" * 68

def sha256b(data): return hashlib.sha256(data).hexdigest()

def scan_thy():
    found = []
    for f in sorted(REPO_ROOT.rglob("*.thy")):
        if any(p in EXCLUDE for p in f.parts):
            continue
        found.append(f)
    return found

def corriger(path):
    original = path.read_bytes()
    corrige  = original
    details  = []
    for fid, old, new, desc in CORRECTIONS:
        n = corrige.count(old)
        corrige = corrige.replace(old, new)
        details.append({"id": fid, "count": n, "desc": desc})
    modifie = corrige != original
    res = {
        "fichier":     path.relative_to(REPO_ROOT).as_posix(),
        "modifie":     modifie,
        "backup":      None,
        "sha_avant":   sha256b(original),
        "sha_apres":   sha256b(corrige),
        "corrections": details,
        "total_rempl": sum(d["count"] for d in details),
        "erreur":      None,
    }
    if modifie:
        BAK_DIR.mkdir(parents=True, exist_ok=True)
        bak = BAK_DIR / (sha256b(original)[:10] + "_" + path.name + ".bak")
        shutil.copy2(path, bak)
        res["backup"] = bak.as_posix()
        path.write_bytes(corrige)
    return res

def log_sqlite(resultats):
    if not DB_PATH.exists():
        print("  [WARN] gabriel_repo_map.db absent - log SQLite ignore")
        return
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS corrections_hol (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_id  TEXT NOT NULL,
            fichier      TEXT NOT NULL,
            modifie      INTEGER NOT NULL,
            total_rempl  INTEGER NOT NULL,
            sha_avant    TEXT,
            sha_apres    TEXT,
            backup_path  TEXT,
            details_json TEXT,
            applied_at   TEXT NOT NULL
        )""")
    now = datetime.now(timezone.utc).isoformat()
    for r in resultats:
        conn.execute("""
            INSERT INTO corrections_hol
              (snapshot_id,fichier,modifie,total_rempl,sha_avant,sha_apres,
               backup_path,details_json,applied_at)
            VALUES (?,?,?,?,?,?,?,?,?)""",
            (SNAPSHOT_ID, r["fichier"], int(r["modifie"]), r["total_rempl"],
             r["sha_avant"], r["sha_apres"], r["backup"],
             json.dumps(r["corrections"], ensure_ascii=False), now))
    conn.commit()
    conn.close()
    print(f"  [DB] {len(resultats)} entrees journalisees dans corrections_hol")

def ecrire_rapport(resultats):
    RAPPORT_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        "session":        "Gabriel_Multiloop - correction HOL Unicode",
        "snapshot_id":    SNAPSHOT_ID,
        "generated_at":   datetime.now(timezone.utc).isoformat(),
        "repo_root":      str(REPO_ROOT),
        "total_fichiers": len(resultats),
        "total_modifies": sum(1 for r in resultats if r["modifie"]),
        "total_rempl":    sum(r["total_rempl"] for r in resultats),
        "corriges":       [r for r in resultats if r["modifie"]],
        "propres":        [r["fichier"] for r in resultats if not r["modifie"]],
    }
    (RAPPORT_DIR / f"rapport_hol_unicode_{SNAPSHOT_ID}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    (RAPPORT_DIR / "rapport_pipeline.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  [RAPPORT] rapport_pipeline.json")
    print(f"  [RAPPORT] rapport_hol_unicode_{SNAPSHOT_ID}.json")
    return data

print(SEP)
print("CORRECTION HOL UNICODE - Gabriel_Multiloop")
print(f"Snapshot : {SNAPSHOT_ID}")
print(f"Repo     : {REPO_ROOT}")
print(SEP)

fichiers = scan_thy()
print(f"\n{len(fichiers)} fichiers .thy detectes\n")
if not fichiers:
    print("[ERREUR] Aucun .thy trouve. Verifiez que vous etes a la racine du depot.")
    sys.exit(1)

resultats = []
for f in fichiers:
    try:
        r = corriger(f)
        resultats.append(r)
        if r["modifie"]:
            print(f"  [CORRIGE]  {r['total_rempl']:3d} rempl.  {r['fichier']}")
        else:
            print(f"  [propre ]    0         {r['fichier']}")
    except Exception as exc:
        err = {"fichier": f.relative_to(REPO_ROOT).as_posix(),
               "modifie": False, "backup": None,
               "sha_avant": "", "sha_apres": "",
               "corrections": [], "total_rempl": 0, "erreur": str(exc)}
        resultats.append(err)
        print(f"  [ERREUR]   {f.name}: {exc}")

modifies    = [r for r in resultats if r["modifie"]]
total_rempl = sum(r["total_rempl"] for r in resultats)

print(f"\n{SEP}")
print(f"Fichiers traites    : {len(resultats)}")
print(f"Fichiers modifies   : {len(modifies)}")
print(f"Total remplacements : {total_rempl}")
print(f"Backups             : {BAK_DIR}")
print(SEP)

log_sqlite(resultats)
ecrire_rapport(resultats)

print()
if total_rempl > 0:
    print("[SUCCES] Correction terminee. Prochaine etape :")
    print(f"  git add theories/ && git commit -m 'fix: HOL Unicode glyphes bruts' && git push")
    print(f"  Rollback : python orchestrator_main.py --rollback .gabriel_variateur/snapshots/{SNAPSHOT_ID}_hol_unicode_fix")
else:
    print("[INFO] Tous les fichiers etaient deja propres. Aucune modification.")
print(SEP)

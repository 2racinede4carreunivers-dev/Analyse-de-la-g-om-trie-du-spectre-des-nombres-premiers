#!/usr/bin/env python3
# =============================================================================
#  gabriel_p4_bridge.py
#  PIPELINE COGNITIF GABRIEL — ÉTAPE 4 (PONT D'INTÉGRATION)
#  Pont FastAPI entre l'Archiviste HOL et les moteurs Gabriel
#
#  Architecture : FastAPI + Motor (async MongoDB) + emergentintegrations LLM
#  Dépôt       : C:\agent-multiloop-Gabriel-local-final
#
#  INTÉGRATION dans Gabriel :
#    Dans votre main.py ou app.py existant, ajoutez simplement :
#
#      from gabriel_p4_bridge import router as hol_router, lifespan_hol
#      app.include_router(hol_router)
#
#    Puis dans vos routes LLM existantes, appelez :
#      from gabriel_p4_bridge import enrichir_prompt_hol
#      contexte = await enrichir_prompt_hol(question)
#
#  Usage autonome : python gabriel_p4_bridge.py
#  Usage test API : uvicorn gabriel_p4_bridge:app --reload --port 8010
# =============================================================================

from __future__ import annotations

import asyncio
import json
import logging
import sqlite3
import sys
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Optional

# ── FastAPI / Pydantic
from fastapi import APIRouter, FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ── Dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ── Emergentintegrations (LLM bridge de Gabriel)
try:
    from emergentintegrations.llm.chat import LlmChat, UserMessage
    EMERGENT_OK = True
except ImportError:
    EMERGENT_OK = False
    logging.warning("emergentintegrations non disponible — mode contexte seul activé")

# ── Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [GABRIEL-HOL] %(levelname)s — %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("gabriel_hol_bridge")

# ─────────────────────────────────────────────────────────────────────────────
#  CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

RACINE   = Path(r"C:\agent-multiloop-Gabriel-local-final")
DB_PATH  = RACINE / "gabriel_corpus.db"

# Modèles LLM supportés par emergentintegrations (adaptez selon votre .env)
import os
LLM_PROVIDER = os.getenv("GABRIEL_LLM_PROVIDER", "claude")   # claude | openai | ollama
LLM_MODEL    = os.getenv("GABRIEL_LLM_MODEL",    "claude-sonnet-4-5")
LLM_API_KEY  = os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY", "")

# Paramètres de recherche
TOP_K_QR    = int(os.getenv("GABRIEL_HOL_TOP_K",  "5"))
SCORE_MIN   = float(os.getenv("GABRIEL_HOL_SCORE", "0.3"))
MAX_CONTEXT = int(os.getenv("GABRIEL_HOL_CTX_MAX", "3000"))

# ─────────────────────────────────────────────────────────────────────────────
#  MODÈLES PYDANTIC (compatible Pydantic v2)
# ─────────────────────────────────────────────────────────────────────────────

class QuestionHOL(BaseModel):
    question: str = Field(..., min_length=3, max_length=2000,
                          description="Question à enrichir avec le corpus HOL Gabriel")
    top_k:    int = Field(default=5, ge=1, le=20,
                          description="Nombre de Q&R à retourner")
    avec_reponse_llm: bool = Field(default=False,
                          description="Si True, génère la réponse LLM complète via emergentintegrations")
    session_id: Optional[str] = Field(default=None,
                          description="ID de session Gabriel (pour historique MongoDB)")


class EntiteHOL(BaseModel):
    nom:        str
    type:       str
    sphere:     Optional[str]
    cercle:     Optional[int]
    occurrences: int


class QRPertinente(BaseModel):
    id:               str
    niveau:           str
    question:         str
    resume:           str
    categorie:        str
    sphere_primaire:  Optional[str]
    score_pertinence: float
    entites_hol:      list[EntiteHOL] = []


class ReponseBridge(BaseModel):
    question_brute:      str
    mots_cles:           list[str]
    spheres_activees:    list[str]
    score_confiance:     float
    qr_pertinentes:      list[QRPertinente]
    entites_activees:    list[EntiteHOL]
    contexte_hol:        str
    reponse_llm:         Optional[str] = None
    modele_utilise:      Optional[str] = None
    timestamp:           str
    db_chemin:           str


class StatsBridge(BaseModel):
    db_disponible:       bool
    db_taille_ko:        float
    nb_entites_hol:      int
    nb_qr_techniques:    int
    nb_mots_cles:        int
    nb_sessions:         int
    emergent_disponible: bool
    llm_provider:        str
    llm_model:           str
    version_bridge:      str = "1.0.0"


# ─────────────────────────────────────────────────────────────────────────────
#  ARCHIVISTE HOL ASYNC (wrapper thread-safe autour de gabriel_p3_archiviste)
# ─────────────────────────────────────────────────────────────────────────────

class ArchivisteHOLBridge:
    """
    Wrapper async/thread-safe du moteur de recherche HOL.
    Utilise sqlite3 en mode thread-safe avec un verrou.
    """

    def __init__(self):
        self._conn: Optional[sqlite3.Connection] = None
        self._lock = Lock()
        self._disponible = False

    def initialiser(self):
        if not DB_PATH.exists():
            log.warning(f"gabriel_corpus.db introuvable : {DB_PATH}")
            log.warning("Exécutez d'abord gabriel_p1, gabriel_p2, gabriel_p3")
            self._disponible = False
            return
        try:
            self._conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA foreign_keys = ON")
            self._conn.execute("PRAGMA journal_mode = WAL")
            nb = self._conn.execute("SELECT COUNT(*) FROM entites_hol").fetchone()[0]
            log.info(f"✓ gabriel_corpus.db connecté — {nb} entités HOL")
            self._disponible = True
        except Exception as e:
            log.error(f"Erreur connexion DB : {e}")
            self._disponible = False

    def fermer(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    @property
    def disponible(self) -> bool:
        return self._disponible

    # ── Normalisation
    @staticmethod
    def _normaliser(texte: str) -> str:
        import re
        return re.sub(r'\s+', ' ', texte.lower().strip())

    @staticmethod
    def _extraire_mots_cles(question: str) -> list[str]:
        import re
        STOP = {
            "le","la","les","un","une","des","de","du","est","que","qui",
            "dans","avec","pour","sur","par","en","au","aux","et","ou",
            "quel","quelle","comment","quoi","ce","cette","ces","il","elle",
        }
        tokens = re.findall(r'[a-zàâäéèêëïîôùûü_\d]+(?:/\d)?',
                            question.lower())
        return [t for t in tokens if len(t) > 2 and t not in STOP]

    # ── Recherche principale (synchrone, appelée dans un thread)
    def _rechercher_sync(self, question: str, top_k: int) -> dict:
        if not self._disponible:
            return self._resultat_vide(question)

        mots_cles = self._extraire_mots_cles(question)

        with self._lock:
            # 1. Scorer les Q&R via l'index des mots-clés
            scores: dict[str, float] = {}
            for mc in mots_cles:
                rows = self._conn.execute(
                    "SELECT qr_ids, frequence FROM index_mots_cles WHERE mot_cle LIKE ?",
                    (f"%{mc}%",)
                ).fetchall()
                for row in rows:
                    freq = row["frequence"] or 1
                    for qr_id in json.loads(row["qr_ids"] or "[]"):
                        scores[qr_id] = scores.get(qr_id, 0.0) + freq / (1 + len(mc))

            # Normaliser les scores
            max_s = max(scores.values(), default=1.0)
            scores_norm = {k: v / max_s for k, v in scores.items()}

            # 2. Récupérer les top-k Q&R
            ids_top = [k for k, _ in sorted(scores_norm.items(),
                                             key=lambda x: -x[1])[:top_k]]
            qr_list = []
            if ids_top:
                placeholders = ",".join("?" * len(ids_top))
                rows_qr = self._conn.execute(
                    f"SELECT * FROM qr_techniques WHERE id IN ({placeholders})",
                    ids_top
                ).fetchall()
                for row in rows_qr:
                    qr_id = row["id"]
                    entites = self._conn.execute("""
                        SELECT e.nom, e.type_hol, e.sphere_id,
                               e.cercle_niveau, e.occurrences, l.score
                        FROM liens_qr_entite l
                        JOIN entites_hol e ON l.entite_id = e.id
                        WHERE l.qr_id = ?
                        ORDER BY l.score DESC LIMIT 6
                    """, (qr_id,)).fetchall()
                    qr_list.append({
                        "id":              qr_id,
                        "niveau":          row["niveau"] or "avance",
                        "question":        row["question"] or "",
                        "resume":          row["resume"] or "",
                        "categorie":       row["categorie"] or "",
                        "sphere_primaire": row["sphere_primaire"] or "—",
                        "score_pertinence": round(scores_norm.get(qr_id, 0.0), 3),
                        "entites_hol":     [
                            {"nom":        e["nom"] or "",
                             "type":       e["type_hol"] or "?",
                             "sphere":     e["sphere_id"],
                             "cercle":     e["cercle_niveau"],
                             "occurrences":e["occurrences"] or 0}
                            for e in entites
                        ],
                    })

            # 3. Récupérer les entités HOL activées
            entites_actives = []
            vus = set()
            for mc in mots_cles[:8]:
                rows_e = self._conn.execute("""
                    SELECT nom, type_hol, sphere_id, cercle_niveau, occurrences
                    FROM entites_hol
                    WHERE nom LIKE ? OR nom = ?
                    ORDER BY occurrences DESC LIMIT 4
                """, (f"%{mc}%", mc)).fetchall()
                for e in rows_e:
                    if e["nom"] not in vus:
                        vus.add(e["nom"])
                        entites_actives.append({
                            "nom":         e["nom"] or "",
                            "type":        e["type_hol"] or "?",
                            "sphere":      e["sphere_id"],
                            "cercle":      e["cercle_niveau"],
                            "occurrences": e["occurrences"] or 0,
                        })

            # 4. Identifier les sphères activées
            spheres: dict[str, float] = {}
            for qr in qr_list:
                sph = qr.get("sphere_primaire", "")
                if sph and sph != "—":
                    spheres[sph] = spheres.get(sph, 0.0) + qr["score_pertinence"]
            for e in entites_actives:
                sph = e.get("sphere")
                if sph:
                    spheres[sph] = spheres.get(sph, 0.0) + 0.3
            spheres_triees = [s for s, _ in sorted(spheres.items(),
                                                    key=lambda x: -x[1])]

            # 5. Construire le contexte HOL
            contexte = self._construire_contexte(
                question, mots_cles, qr_list, entites_actives, spheres_triees
            )

            # 6. Score de confiance global
            score_conf = max(
                (qr["score_pertinence"] for qr in qr_list[:3]), default=0.0
            )

            # 7. Sauvegarder la session
            self._sauvegarder_session(
                question, mots_cles, qr_list, entites_actives, spheres_triees, score_conf
            )

        return {
            "question_brute":   question,
            "mots_cles":        mots_cles,
            "spheres_activees": spheres_triees,
            "score_confiance":  round(score_conf, 3),
            "qr_pertinentes":   qr_list,
            "entites_activees": entites_actives,
            "contexte_hol":     contexte,
            "timestamp":        datetime.now().isoformat(),
            "db_chemin":        str(DB_PATH),
        }

    def _construire_contexte(self, question: str, mots_cles: list[str],
                              qr_list: list[dict], entites: list[dict],
                              spheres: list[str]) -> str:
        """Construit le bloc de contexte HOL à injecter dans le prompt Gabriel."""
        lignes = [
            "╔══ CONTEXTE COGNITIF HOL — CORPUS SPECTRAL GABRIEL ══╗",
            f"║ Question     : {question[:100]}",
            f"║ Sphères      : {', '.join(spheres) or 'Ensemble'}",
            f"║ Équation     : Ensemble = 1  ↔  1/x + 1/t + 1/ms",
            "╠══ Q&R TECHNIQUES PERTINENTES ═══════════════════════╣",
        ]
        for i, qr in enumerate(qr_list[:5], 1):
            lignes += [
                f"║ [{i}] {qr['id']} [{qr['niveau']}] — score {qr['score_pertinence']:.3f}",
                f"║     Q: {qr['question'][:90]}",
                f"║     R: {qr['resume'][:90]}",
            ]
            if qr["entites_hol"]:
                noms = ", ".join(e["nom"] for e in qr["entites_hol"][:4])
                lignes.append(f"║     Entités HOL: {noms}")
            lignes.append("║")

        if entites:
            lignes.append("╠══ ENTITÉS HOL ACTIVÉES ══════════════════════════════╣")
            for e in entites[:6]:
                sph = e.get("sphere") or "—"
                cer = str(e.get("cercle")) if e.get("cercle") is not None else "—"
                lignes.append(f"║  • {e['nom']:35s} [{e['type']:10s}] {sph} cercle {cer}")

        lignes += [
            "╠══ INSTRUCTION ═══════════════════════════════════════╣",
            "║ Utilise ce contexte HOL pour ancrer ta réponse dans  ║",
            "║ la méthode spectrale de Philippe Savard.              ║",
            "║ Cite les entités HOL pertinentes et leurs sphères.   ║",
            "╚═══════════════════════════════════════════════════════╝",
        ]
        return "\n".join(lignes)[:MAX_CONTEXT]

    def _sauvegarder_session(self, question: str, mots_cles: list,
                              qr_list: list, entites: list,
                              spheres: list, score: float):
        try:
            self._conn.execute("""
                INSERT INTO sessions
                (question_brute, question_norm, mots_cles_detectes,
                 qr_ids_retournees, entites_activees, spheres_activees,
                 moteur_gabriel, score_confiance)
                VALUES (?,?,?,?,?,?,?,?)
            """, (
                question,
                self._normaliser(question),
                json.dumps(mots_cles[:10], ensure_ascii=False),
                json.dumps([q["id"] for q in qr_list], ensure_ascii=False),
                json.dumps([e["nom"] for e in entites[:10]], ensure_ascii=False),
                json.dumps(spheres, ensure_ascii=False),
                "gabriel_p4_bridge",
                score,
            ))
            self._conn.commit()
        except Exception as e:
            log.warning(f"Session non sauvegardée : {e}")

    @staticmethod
    def _resultat_vide(question: str) -> dict:
        return {
            "question_brute":   question,
            "mots_cles":        [],
            "spheres_activees": [],
            "score_confiance":  0.0,
            "qr_pertinentes":   [],
            "entites_activees": [],
            "contexte_hol":     "⚠ gabriel_corpus.db non disponible — exécutez P1→P2→P3 d'abord.",
            "timestamp":        datetime.now().isoformat(),
            "db_chemin":        str(DB_PATH),
        }

    # ── Interface async (exécute le code sync dans un thread du pool)
    async def rechercher(self, question: str, top_k: int = 5) -> dict:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, self._rechercher_sync, question, top_k
        )

    def stats(self) -> dict:
        """Retourne les statistiques de la DB."""
        if not self._disponible:
            return {}
        with self._lock:
            tables = ["entites_hol", "qr_techniques", "index_mots_cles", "sessions"]
            return {t: self._conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                    for t in tables}


# ─────────────────────────────────────────────────────────────────────────────
#  INSTANCE GLOBALE — partagée par tous les workers FastAPI
# ─────────────────────────────────────────────────────────────────────────────

archiviste = ArchivisteHOLBridge()


# ─────────────────────────────────────────────────────────────────────────────
#  FONCTION PUBLIQUE — à importer dans les routes Gabriel existantes
# ─────────────────────────────────────────────────────────────────────────────

async def enrichir_prompt_hol(question: str, top_k: int = TOP_K_QR) -> str:
    """
    Fonction clé d'intégration — à appeler depuis vos routes Gabriel.

    Usage dans vos routes FastAPI existantes :
        from gabriel_p4_bridge import enrichir_prompt_hol

        @router.post("/chat")
        async def chat(req: ChatRequest):
            contexte_hol = await enrichir_prompt_hol(req.message)
            prompt_complet = contexte_hol + "\\n\\nQuestion : " + req.message
            # → passer prompt_complet à emergentintegrations LlmChat
    """
    if not archiviste.disponible:
        return ""
    resultat = await archiviste.rechercher(question, top_k)
    return resultat.get("contexte_hol", "")


async def enrichir_et_repondre(
    question: str,
    session_id: Optional[str] = None,
    top_k: int = TOP_K_QR,
) -> tuple[str, str]:
    """
    Enrichit le prompt HOL ET génère la réponse LLM via emergentintegrations.
    Retourne (contexte_hol, reponse_llm).
    """
    resultat = await archiviste.rechercher(question, top_k)
    contexte = resultat.get("contexte_hol", "")

    if not EMERGENT_OK or not LLM_API_KEY:
        return contexte, ""

    try:
        session = session_id or f"hol-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        chat = LlmChat(
            provider=LLM_PROVIDER,
            session_id=session,
            system_message=(
                "Tu es Gabriel, agent expert en théorie spectrale de Philippe Savard. "
                "Réponds en français, en t'appuyant sur le contexte HOL fourni. "
                "Cite les théorèmes, lemmes et entités Isabelle/HOL pertinents. "
                "L'équation centrale est : Ensemble = 1 ↔ 1/x + 1/t + 1/ms."
            ),
        ).with_model(LLM_PROVIDER, LLM_MODEL)

        prompt_enrichi = f"{contexte}\n\n---\nQuestion : {question}"
        reponse = await chat.send_message(UserMessage(content=prompt_enrichi))
        return contexte, reponse

    except Exception as e:
        log.error(f"Erreur LLM emergentintegrations : {e}")
        return contexte, f"[Erreur LLM : {e}]"


# ─────────────────────────────────────────────────────────────────────────────
#  FASTAPI ROUTER — à inclure dans l'app Gabriel existante
# ─────────────────────────────────────────────────────────────────────────────

router = APIRouter(
    prefix="/hol",
    tags=["Corpus HOL — Méthode Spectrale Savard"],
)


@router.post("/enrichir", response_model=ReponseBridge,
             summary="Enrichit une question avec le corpus HOL Gabriel")
async def route_enrichir(payload: QuestionHOL,
                          bg: BackgroundTasks) -> ReponseBridge:
    """
    Route principale du pont HOL.
    Reçoit une question, retourne le contexte HOL + Q&R pertinentes.
    Si avec_reponse_llm=True, génère aussi la réponse via emergentintegrations.
    """
    if not archiviste.disponible:
        raise HTTPException(
            status_code=503,
            detail="gabriel_corpus.db non disponible. "
                   "Exécutez gabriel_p1, gabriel_p2, gabriel_p3 d'abord."
        )

    if payload.avec_reponse_llm:
        contexte, reponse = await enrichir_et_repondre(
            payload.question, payload.session_id, payload.top_k
        )
        resultat_raw = await archiviste.rechercher(payload.question, payload.top_k)
        resultat_raw["reponse_llm"]    = reponse
        resultat_raw["modele_utilise"] = f"{LLM_PROVIDER}/{LLM_MODEL}" if EMERGENT_OK else None
    else:
        resultat_raw = await archiviste.rechercher(payload.question, payload.top_k)
        resultat_raw["reponse_llm"]    = None
        resultat_raw["modele_utilise"] = None

    return ReponseBridge(
        question_brute=    resultat_raw["question_brute"],
        mots_cles=         resultat_raw["mots_cles"],
        spheres_activees=  resultat_raw["spheres_activees"],
        score_confiance=   resultat_raw["score_confiance"],
        qr_pertinentes=[
            QRPertinente(
                id=              q["id"],
                niveau=          q["niveau"],
                question=        q["question"],
                resume=          q["resume"],
                categorie=       q["categorie"],
                sphere_primaire= q.get("sphere_primaire"),
                score_pertinence=q["score_pertinence"],
                entites_hol=[
                    EntiteHOL(
                        nom=        e["nom"],
                        type=       e["type"],
                        sphere=     e.get("sphere"),
                        cercle=     e.get("cercle"),
                        occurrences=e.get("occurrences", 0),
                    ) for e in q.get("entites_hol", [])
                ],
            ) for q in resultat_raw["qr_pertinentes"]
        ],
        entites_activees=[
            EntiteHOL(
                nom=        e["nom"],
                type=       e["type"],
                sphere=     e.get("sphere"),
                cercle=     e.get("cercle"),
                occurrences=e.get("occurrences", 0),
            ) for e in resultat_raw["entites_activees"]
        ],
        contexte_hol=      resultat_raw["contexte_hol"],
        reponse_llm=       resultat_raw.get("reponse_llm"),
        modele_utilise=    resultat_raw.get("modele_utilise"),
        timestamp=         resultat_raw["timestamp"],
        db_chemin=         resultat_raw["db_chemin"],
    )


@router.get("/stats", response_model=StatsBridge,
            summary="Statistiques du corpus HOL")
async def route_stats() -> StatsBridge:
    stats = archiviste.stats()
    taille = DB_PATH.stat().st_size / 1024 if DB_PATH.exists() else 0.0
    return StatsBridge(
        db_disponible=       archiviste.disponible,
        db_taille_ko=        round(taille, 1),
        nb_entites_hol=      stats.get("entites_hol", 0),
        nb_qr_techniques=    stats.get("qr_techniques", 0),
        nb_mots_cles=        stats.get("index_mots_cles", 0),
        nb_sessions=         stats.get("sessions", 0),
        emergent_disponible= EMERGENT_OK,
        llm_provider=        LLM_PROVIDER,
        llm_model=           LLM_MODEL,
    )


@router.get("/sante", summary="Vérification santé du pont HOL")
async def route_sante():
    return {
        "statut":           "ok" if archiviste.disponible else "degradé",
        "db_disponible":    archiviste.disponible,
        "emergent_llm":     EMERGENT_OK,
        "timestamp":        datetime.now().isoformat(),
        "version":          "1.0.0",
    }


@router.get("/spheres", summary="Liste des sphères Ensemble = 1/x + 1/t + 1/ms")
async def route_spheres():
    if not archiviste.disponible:
        raise HTTPException(status_code=503, detail="DB non disponible")
    with archiviste._lock:
        rows = archiviste._conn.execute(
            "SELECT id, nom, equation, description, concordance, rayon FROM spheres"
        ).fetchall()
    return [dict(r) for r in rows]


@router.get("/qr", summary="Liste toutes les Q&R techniques")
async def route_qr_liste():
    if not archiviste.disponible:
        raise HTTPException(status_code=503, detail="DB non disponible")
    with archiviste._lock:
        rows = archiviste._conn.execute(
            "SELECT id, niveau, question, resume, categorie, sphere_primaire "
            "FROM qr_techniques ORDER BY id"
        ).fetchall()
    return [dict(r) for r in rows]


@router.get("/entites/{sphere_id}", summary="Entités HOL d'une sphère")
async def route_entites_sphere(sphere_id: str):
    if not archiviste.disponible:
        raise HTTPException(status_code=503, detail="DB non disponible")
    if sphere_id not in ("1/ms", "1/t", "1/x", "Ensemble"):
        raise HTTPException(status_code=400,
                            detail="sphere_id doit être : 1/ms, 1/t, 1/x ou Ensemble")
    with archiviste._lock:
        rows = archiviste._conn.execute("""
            SELECT nom, type_hol, cercle_niveau, occurrences, source_fichier
            FROM entites_hol
            WHERE sphere_id = ?
            ORDER BY cercle_niveau, occurrences DESC
        """, (sphere_id,)).fetchall()
    return [dict(r) for r in rows]


# ─────────────────────────────────────────────────────────────────────────────
#  LIFESPAN — initialisation/fermeture de l'archiviste avec l'app FastAPI
# ─────────────────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan_hol(app: FastAPI):
    """
    Gestionnaire de cycle de vie pour intégration dans l'app Gabriel.

    Usage dans votre main.py existant :
        from gabriel_p4_bridge import lifespan_hol
        # Combinez avec votre lifespan existant si vous en avez un
    """
    log.info("Initialisation du corpus HOL Gabriel...")
    archiviste.initialiser()
    if archiviste.disponible:
        s = archiviste.stats()
        log.info(f"✓ Corpus HOL prêt : {s.get('entites_hol',0)} entités, "
                 f"{s.get('qr_techniques',0)} Q&R, {s.get('index_mots_cles',0)} mots-clés")
    yield
    log.info("Fermeture du corpus HOL Gabriel...")
    archiviste.fermer()


# ─────────────────────────────────────────────────────────────────────────────
#  APP STANDALONE (pour test direct ou développement)
# ─────────────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Gabriel HOL Bridge",
    description=(
        "Pont d'intégration entre le corpus spectral HOL "
        "(methode_spectral.thy + validation_hol_unifiee.thy) "
        "et les moteurs FastAPI de Gabriel.\n\n"
        "**Équation centrale** : `Ensemble = 1 ↔ 1/x + 1/t + 1/ms`\n\n"
        "**Intégration dans Gabriel** :\n"
        "```python\n"
        "from gabriel_p4_bridge import router as hol_router, lifespan_hol\n"
        "app.include_router(hol_router)\n"
        "```"
    ),
    version="1.0.0",
    lifespan=lifespan_hol,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


# ─────────────────────────────────────────────────────────────────────────────
#  POINT D'ENTRÉE AUTONOME
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn

    print("\n" + "="*70)
    print("  GABRIEL P4 — PONT D'INTÉGRATION HOL")
    print("  Ensemble = 1  ↔  1/x + 1/t + 1/ms  (Pont Savard XIII)")
    print("="*70)

    archiviste.initialiser()

    if len(sys.argv) > 1 and sys.argv[1] == "--api":
        # Lancer l'API FastAPI en mode test
        print("\n  Mode API — Documentation : http://localhost:8010/docs")
        print("  Routes disponibles :")
        print("    POST /hol/enrichir    — Enrichir une question avec le corpus HOL")
        print("    GET  /hol/stats       — Statistiques de la DB")
        print("    GET  /hol/sante       — Vérification santé")
        print("    GET  /hol/spheres     — Liste des sphères")
        print("    GET  /hol/qr          — Liste des Q&R techniques")
        print("    GET  /hol/entites/{sphere_id} — Entités HOL par sphère")
        uvicorn.run("gabriel_p4_bridge:app", host="0.0.0.0", port=8010, reload=False)

    else:
        # Mode test rapide en ligne de commande
        print("\n  Mode test rapide (--api pour lancer l'API FastAPI)\n")
        questions_test = [
            "Comment pont_spectral_direct_final démontre RsP = 1/2 ?",
            "Quel est le rôle de la locale ensemble_savard dans la section XIII ?",
        ]

        async def demo():
            for q in questions_test:
                print(f"\n  Question : {q}")
                res = await archiviste.rechercher(q, top_k=3)
                print(f"  Score    : {res['score_confiance']:.3f}")
                print(f"  Sphères  : {', '.join(res['spheres_activees'])}")
                print(f"  Q&R top  : {[qr['id'] for qr in res['qr_pertinentes']]}")
                print(f"\n{res['contexte_hol'][:800]}\n")
                print("-"*60)

        asyncio.run(demo())
        print("\n  ✅ Pipeline cognitif Gabriel complet (P1→P2→P3→P4)")
        print("="*70 + "\n")

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports

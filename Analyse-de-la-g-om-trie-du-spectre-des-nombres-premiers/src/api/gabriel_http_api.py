#!/usr/bin/env python3
# ============================================================
# gabriel_http_api.py
# v4.0 : HTTP API pour Gabriel - accepte requetes d'Isabelle et sites externes
# 
# Endpoints:
#  POST /query - Envoie une question a Gabriel
#  POST /isabelle/verify - Recoit resultats d'Isabelle CLI
#  GET /health - Verifier que Gabriel est en ligne
#  POST /sync/universestaucarre - Synchro avec www.universestaucarre.com
# ============================================================

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict
from pathlib import Path

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# v4.0 : CORS pour accepter requetes d'autres domaines
CORS(app, resources={
    r"/api/*": {"origins": ["*"]},
    r"/query": {"origins": ["*"]},
    r"/isabelle/*": {"origins": ["*"]},
    r"/sync/*": {"origins": ["*"]},
})

# Reference vers le Pipeline Gabriel
pipeline = None
config = None


def init_gabriel_api(gabriel_pipeline, gabriel_config):
    """Initialiser l'API avec le Pipeline Gabriel"""
    global pipeline, config
    pipeline = gabriel_pipeline
    config = gabriel_config
    logger.info("Gabriel HTTP API initialized (port 8000)")


def _enrichir_multi_rapports(question: str, answer):
    """Couche reponse : append le tableau multi-rapports deterministe (no-throw)."""
    try:
        from src.core.multi_ratio_response import enrichir_reponse_multi_rapports
        cfg_multi = (config or {}).get("multi_ratio_reponse", None) if isinstance(config, dict) else None
        enrichir_reponse_multi_rapports(question, answer, cfg_multi)
    except Exception as exc:  # pragma: no cover - garde-fou reponse
        logger.warning("Enrichissement multi-rapports ignore: %s", exc)
    return answer


def _guard_reject(question: str):
    """Garde-fou de domaine absolu (La fiancée de Cline).

    Retourne une reponse Flask (message + 200) si la requete est hors sujet,
    sinon None. Ne leve jamais : en cas d'indisponibilite, laisse passer.
    """
    try:
        from src.multiloop.fiancee_guard import verifier_requete, MESSAGE_HORS_SUJET
        res = verifier_requete(question)
        if not res.autorise:
            logger.info("Requete rejetee (hors sujet): %s", str(question)[:80])
            return jsonify({
                "answer": res.message or MESSAGE_HORS_SUJET,
                "confidence": 1.0,
                "rejected": True,
                "reason": res.raison,
                "source": "La fiancée de Cline - garde-fou",
            }), 200
    except Exception as exc:
        logger.debug("Garde-fou indisponible: %s", exc)
    return None


# ============================================================
# ENDPOINT 1: Query - Envoyer une question a Gabriel
# ============================================================
@app.route("/query", methods=["POST"])
def query():
    """
    POST /query
    Body: {"question": "...", "source": "isabelle|universestaucarre|web"}
    
    Reponse: {"answer": "...", "confidence": 0.95, "source": "Gabriel"}
    """
    try:
        data = request.get_json() or {}
        question = data.get("question")
        source = data.get("source", "unknown")
        
        if not question:
            return jsonify({"error": "Missing 'question' field"}), 400
        
        _rej = _guard_reject(question)
        if _rej is not None:
            return _rej

        logger.info(f"Query from {source}: {question[:100]}")
        
        # Executer Gabriel Pipeline (synchrone pour Flask)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        final_answer = loop.run_until_complete(pipeline.process(question))
        final_answer = _enrichir_multi_rapports(question, final_answer)

        return jsonify({
            "answer": final_answer.answer_text,
            "confidence": final_answer.confidence,
            "iterations": final_answer.iterations_used,
            "best_score": final_answer.best_score,
            "source": "Gabriel v4.0",
            "timestamp": datetime.now().isoformat(),
            "epistemic_claim": final_answer.epistemic_claim,
        }), 200
    
    except Exception as e:
        # Correction Alerte CodeQL (py/stack-trace-exposure)
        logger.error(f"Query error: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred during query processing."}), 500


# ============================================================
# ENDPOINT 2: Isabelle Verify - Recoit les resultats d'Isabelle CLI
# ============================================================
@app.route("/isabelle/verify", methods=["POST"])
def isabelle_verify():
    """
    POST /isabelle/verify
    Body: {
        "theory_file": "/theories/example.thy",
        "status": "success|error",
        "output": "...",
        "timestamp": "2025-01-15T..."
    }
    
    Reponse: {"stored": true, "file_path": "..."}
    """
    try:
        data = request.get_json() or {}
        theory_file = data.get("theory_file", "unknown")
        status = data.get("status", "unknown")
        output = data.get("output", "")
        timestamp = data.get("timestamp", datetime.now().isoformat())
        
        logger.info(f"Isabelle result: {theory_file} ({status})")
        
        # Sauvegarder dans data/isabelle-results/
        results_dir = Path("/home/agent/app/data/isabelle-results")
        results_dir.mkdir(parents=True, exist_ok=True)
        
        result_file = results_dir / f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        result_file.write_text(json.dumps({
            "theory_file": theory_file,
            "status": status,
            "output": output,
            "received_at": datetime.now().isoformat(),
            "processed_at": timestamp,
        }, indent=2))
        
        return jsonify({
            "stored": True,
            "file_path": str(result_file),
            "status": status,
        }), 200
    
    except Exception as e:
        # Correction Alerte CodeQL (py/stack-trace-exposure)
        logger.error(f"Isabelle verify error: {e}", exc_info=True)
        return jsonify({"error": "An error occurred while processing Isabelle verification."}), 500


# ============================================================
# ENDPOINT 3: Health Check
# ============================================================
@app.route("/health", methods=["GET"])
def health():
    """GET /health - Verifier que Gabriel est en ligne"""
    return jsonify({
        "status": "online",
        "service": "Gabriel v4.0",
        "pipeline": "active" if pipeline else "inactive",
        "timestamp": datetime.now().isoformat(),
    }), 200


# ============================================================
# ENDPOINT 4: Sync avec www.universestaucarre.com
# ============================================================
@app.route("/sync/universestaucarre", methods=["POST"])
def sync_universestaucarre():
    """
    POST /sync/universestaucarre
    
    Permet a www.universestaucarre.com de synchroniser ses resultats
    avec Gabriel local pour comparaisons croisees (4 IAs).
    
    Body: {
        "session_id": "uuid",
        "question": "...",
        "results": {
            "gpt4": "...",
            "claude": "...",
            "gemini": "...",
            "gabriel_web": "..."
        }
    }
    """
    try:
        data = request.get_json() or {}
        
        # Securisation de session_id contre les attaques Path Traversal (CodeQL py/path-injection)
        raw_session_id = data.get("session_id", "unknown")
        session_id = secure_filename(str(raw_session_id)) or "unknown"
        
        question = data.get("question")
        results = data.get("results", {})
        
        logger.info(f"Sync from universestaucarre: session={session_id}")
        
        if not question:
            return jsonify({"error": "Missing 'question' field"}), 400
        
        _rej = _guard_reject(question)
        if _rej is not None:
            return _rej

        # Executer Gabriel LOCAL pour comparaison (synchrone pour Flask)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        local_answer = loop.run_until_complete(pipeline.process(question))
        local_answer = _enrichir_multi_rapports(question, local_answer)
        
        # Sauvegarder la synchro
        sync_dir = Path("/home/agent/app/data/universestaucarre-sync")
        sync_dir.mkdir(parents=True, exist_ok=True)
        
        sync_file = sync_dir / f"sync_{session_id}.json"
        sync_data = {
            "session_id": session_id,
            "question": question,
            "timestamp": datetime.now().isoformat(),
            "gabriel_local": {
                "answer": local_answer.answer_text,
                "confidence": local_answer.confidence,
                "iterations": local_answer.iterations_used,
            },
            "gabriel_web": results.get("gabriel_web"),
            "other_ias": {
                "gpt4": results.get("gpt4"),
                "claude": results.get("claude"),
                "gemini": results.get("gemini"),
            },
            "comparison": {
                "gabriel_local_vs_web": "pending",
                "consensus": "pending",
            },
        }
        sync_file.write_text(json.dumps(sync_data, indent=2))
        
        return jsonify({
            "synced": True,
            "gabriel_local_answer": local_answer.answer_text[:200],
            "gabriel_local_confidence": local_answer.confidence,
            "session_file": str(sync_file),
        }), 200
    
    except Exception as e:
        # Correction Alerte CodeQL (py/stack-trace-exposure)
        logger.error(f"Sync error: {e}", exc_info=True)
        return jsonify({"error": "An error occurred during synchronization."}), 500


# ============================================================
# ENDPOINT 5: WebSocket pour streaming (BONUS)
# ============================================================
@app.route("/stream", methods=["POST"])
def stream_query():
    """
    POST /stream - Streaming des resultats en temps reel
    (Pour sites comme www.universestaucarre.com)
    """
    try:
        data = request.get_json() or {}
        question = data.get("question")
        
        if not question:
            return jsonify({"error": "Missing question"}), 400

        _rej = _guard_reject(question)
        if _rej is not None:
            return _rej
        
        # Executer Gabriel (synchrone pour Flask)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        final_answer = loop.run_until_complete(pipeline.process(question))
        final_answer = _enrichir_multi_rapports(question, final_answer)

        return jsonify({
            "answer": final_answer.answer_text,
            "streamed": True,
        }), 200
    
    except Exception as e:
        # Correction Alerte CodeQL (py/stack-trace-exposure)
        logger.error(f"Stream error: {e}", exc_info=True)
        return jsonify({"error": "An error occurred while processing the stream."}), 500


def run_gabriel_api(host="0.0.0.0", port=8000, debug=False):
    """Lancer le serveur Flask"""
    logger.info(f"Starting Gabriel HTTP API on {host}:{port}")
    app.run(host=host, port=port, debug=debug, threaded=True)


if __name__ == "__main__":
    run_gabriel_api()
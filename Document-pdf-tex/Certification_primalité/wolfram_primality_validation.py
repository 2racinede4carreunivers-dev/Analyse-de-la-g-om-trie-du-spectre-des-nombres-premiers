#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate la primalite des ancres du fichier de reconstruction detail
via l'API Wolfram|Alpha.

La cl� App ID est lue dans le .env du depot (variable WOLFRAM_APP_ID).
Chaque ancre est envoyee sous la forme "is <ANCRE> prime".

Entree :  <repo>/reconstruction_k28M_84M_detail.txt
Sortie :  <output>.jsonl  (une ligne JSON par ancre :
          {ridx, ancre, statut_fiche, resultat, raw})
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import List, Tuple

import httpx

REPO_ROOT = Path(
    r"C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers"
    r"\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers"
)
DEFAULT_INPUT = REPO_ROOT / "reconstruction_k28M_84M_detail.txt"
DEFAULT_OUTPUT = REPO_ROOT / "reconstruction_k28M_84M_detail_wolfram_primalite.jsonl"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("wolfram_val")

sys.path.insert(0, str(REPO_ROOT))
from src.adapters.wolfram import (   # noqa: E402
    WolframClient,
    WolframError,
    WolframInvalidAppIDError,
    WolframNoResultError,
    WolframTimeoutError,
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    p.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    p.add_argument("--concurrency", type=int, default=16,
                   help="nombre de requetes Wolfram simultanees")
    p.add_argument("--batch-size", type=int, default=5000,
                   help="ancres par lot traite")
    p.add_argument("--log-every", type=int, default=2000,
                   help="frequence des logs de progression")
    p.add_argument("--max-attempts", type=int, default=3,
                   help="tentatives par ancre en cas d'erreur reseau")
    return p.parse_args()


def load_app_id(env_path: Path | None = None) -> str:
    """Lire WOLFRAM_APP_ID du .env (ou de la variable d'environnement)."""
    env = env_path or Path(
        os.environ.get("WOLFRAM_ENV", str(REPO_ROOT / ".env"))
    )
    app_id = os.environ.get("WOLFRAM_APP_ID", "")
    if not app_id and env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("WOLFRAM_APP_ID"):
                app_id = line.split("=", 1)[1].strip()
                break
    app_id = (app_id or "").strip()
    if not app_id:
        raise RuntimeError("WOLFRAM_APP_ID non defini (variable ou .env)")
    if app_id.upper().startswith(("VOTRE-", "COLLEZ-", "PLACEHOLDER")):
        raise RuntimeError("WOLFRAM_APP_ID est un placeholder : %r" % app_id)
    log.info("App ID Wolfram lue (len=%d) depuis %s", len(app_id), env)
    return app_id


def parse_wolfram(text: str) -> Tuple[str, str]:
    """Extraire (resultat, raw) a partir du plaintext de Wolfram."""
    t = (text or "").strip()
    low = t.lower()
    if "prime number" in low and "not" not in low and "composite" not in low:
        return "PREMIER", t
    if "not a prime number" in low or "composite number" in low:
        return "COMPOSITE", t
    if "probably prime" in low:
        return "PREMIER_PROBABLE", t
    return "INCONNU", t

async def check_one(
    client: WolframClient,
    ridx: str,
    anc: str,
    statut: str,
    sem: asyncio.Semaphore,
    max_attempts: int,
) -> dict:
    """Un appel Wolfram `is ANCRE prime` avec retries."""
    async with sem:
        last_err: Exception | None = None
        for attempt in range(max_attempts):
            try:
                qr = await client.query_full_results("is %s prime" % anc)
                text = (client.extract_primary_plaintext(qr) or "").strip()
                resultat, raw = parse_wolfram(text)
                return {
                    "ridx": ridx,
                    "ancre": anc,
                    "statut_fiche": statut,
                    "resultat": resultat,
                    "raw": raw,
                }
            except (WolframTimeoutError, WolframError, WolframNoResultError,
                    WolframInvalidAppIDError) as exc:
                last_err = exc
                log.warning(
                    "ancre %s : tentative %d/%d echoue: %s",
                    anc[:12], attempt + 1, max_attempts, exc,
                )
                if attempt < max_attempts - 1:
                    await asyncio.sleep(2 ** attempt)
        return {
            "ridx": ridx,
            "ancre": anc,
            "statut_fiche": statut,
            "resultat": "ERREUR",
            "raw": "erreur apres %d tentatives: %s" % (max_attempts, last_err),
        }


async def run_batch(client, sem, batch, max_attempts) -> List[dict]:
    tasks = [
        check_one(client, ridx, anc, statut, sem, max_attempts)
        for ridx, anc, statut in batch
    ]
    return await asyncio.gather(*tasks)


async def main() -> None:
    args = parse_args()
    log.info("args: %s", args)

    app_id = load_app_id()
    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0, connect=5.0)) as shared:
        client = WolframClient(app_id=app_id, client=shared, timeout=30.0)
        if not client.is_available():
            log.error("Client Wolfram indisponible (App ID invalide ?)")
            sys.exit(1)
        log.info(
            "Client Wolfram prêt (app_id=%s...)", app_id[:8]
        )

        sem = asyncio.Semaphore(args.concurrency)
        output = args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        out_fh = output.open("w", encoding="utf-8")

        total = 0
        t0 = time.time()
        batch: List[Tuple[str, str, str]] = []

        with args.input.open(encoding="utf-8", errors="ignore") as fh:
            for _ in range(3):          # entete + colonnes + separateur
                next(fh, None)
            for line in fh:
                parts = line.split("|")
                if len(parts) < 2:
                    continue
                ridx = parts[0].strip()
                anc = parts[1].strip()
                statut = parts[3].strip() if len(parts) >= 5 else ""
                if not anc or anc == "-":
                    continue            # ancres AMBIGU (tire)
                batch.append((ridx, anc, statut))
                if len(batch) >= args.batch_size:
                    results = await run_batch(client, sem, batch, args.max_attempts)
                    for r in results:
                        out_fh.write(json.dumps(r, ensure_ascii=False) + "\n")
                        total += 1
                    batch = []
                    if total % args.log_every == 0:
                        log.info(
                            "progress: %d ancres (%ds)",
                            total, int(time.time() - t0),
                        )
        if batch:
            results = await run_batch(client, sem, batch, args.max_attempts)
            for r in results:
                out_fh.write(json.dumps(r, ensure_ascii=False) + "\n")
                total += 1
        out_fh.close()
        log.info(
            "FAIT: %d ancres en %.1fs (%.1f ancres/s) -> %s",
            total, time.time() - t0, total / (time.time() - t0), output,
        )


if __name__ == "__main__":
    asyncio.run(main())

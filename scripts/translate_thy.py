"""
Pipeline de traduction du fichier methode_spectral.thy vers 7 langues.

Preserve INTEGRALEMENT le code HOL/Isabelle. Ne traduit QUE :
  - Les commentaires (* ... *)
  - Les blocs Isabelle text \<open>...\<close>
  - L'entete metadata (traduit les libelles, garde les transcriptions API)

Chaque langue produit un fichier methode_spectral_<lang>.thy propre,
compilable par Isabelle et semantiquement equivalent a l'original francais.

Utilisation :
    python scripts/translate_thy.py             # toutes les langues
    python scripts/translate_thy.py en es       # sous-ensemble
"""
from __future__ import annotations

import asyncio
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

from emergentintegrations.llm.chat import LlmChat, UserMessage

EMERGENT_LLM_KEY = os.environ.get("EMERGENT_LLM_KEY", "sk-emergent-c20D27d2bDa5755870")
MODEL_PROVIDER = "anthropic"
MODEL_NAME = "claude-sonnet-4-6"

THY_SOURCE = Path("theories/methode_spectral.thy")
THY_OUT_DIR = Path("theories")

# Configuration par langue : nom local, code ISO, libelles d'entete traduits
LANGUAGES: dict[str, dict[str, str]] = {
    "en": {
        "name": "English",
        "native_name": "English",
        "hdr_file":    "File",
        "hdr_date":    "Date",
        "hdr_date_fr": "July twenty-fourth, two thousand twenty-six",
        "hdr_place":   "Location",
        "hdr_place_fr":"Levis, Chaudiere-Appalaches, Canada",
        "hdr_title":   "Title",
        "hdr_title_fr":"The Universe Squared",
        "hdr_sub":     "Subtitle",
        "hdr_sub_fr":  "Chapter -- The Geometry of the Prime Number Spectrum",
        "hdr_author":  "Author",
    },
    "es": {
        "name": "Spanish",
        "native_name": "Espanol",
        "hdr_file":    "Archivo",
        "hdr_date":    "Fecha",
        "hdr_date_fr": "Veinticuatro de julio de dos mil veintiseis",
        "hdr_place":   "Lugar",
        "hdr_place_fr":"Levis, Chaudiere-Appalaches, Canada",
        "hdr_title":   "Titulo",
        "hdr_title_fr":"El universo al cuadrado",
        "hdr_sub":     "Subtitulo",
        "hdr_sub_fr":  "Capitulo -- La geometria del espectro de los numeros primos",
        "hdr_author":  "Autor",
    },
    "de": {
        "name": "German",
        "native_name": "Deutsch",
        "hdr_file":    "Datei",
        "hdr_date":    "Datum",
        "hdr_date_fr": "Vierundzwanzigster Juli zweitausendsechsundzwanzig",
        "hdr_place":   "Ort",
        "hdr_place_fr":"Levis, Chaudiere-Appalaches, Kanada",
        "hdr_title":   "Titel",
        "hdr_title_fr":"Das Universum im Quadrat",
        "hdr_sub":     "Untertitel",
        "hdr_sub_fr":  "Kapitel -- Die Geometrie des Spektrums der Primzahlen",
        "hdr_author":  "Autor",
    },
    "pt": {
        "name": "Portuguese",
        "native_name": "Portugues",
        "hdr_file":    "Arquivo",
        "hdr_date":    "Data",
        "hdr_date_fr": "Vinte e quatro de julho de dois mil e vinte e seis",
        "hdr_place":   "Local",
        "hdr_place_fr":"Levis, Chaudiere-Appalaches, Canada",
        "hdr_title":   "Titulo",
        "hdr_title_fr":"O universo ao quadrado",
        "hdr_sub":     "Subtitulo",
        "hdr_sub_fr":  "Capitulo -- A geometria do espectro dos numeros primos",
        "hdr_author":  "Autor",
    },
    "ru": {
        "name": "Russian",
        "native_name": "Russkiy",
        "hdr_file":    "Fayl",
        "hdr_date":    "Data",
        "hdr_date_fr": "Dvadtsat chetvertoe iyulya dve tysyachi dvadtsat shestogo goda",
        "hdr_place":   "Mesto",
        "hdr_place_fr":"Levis, Chaudiere-Appalaches, Kanada",
        "hdr_title":   "Nazvanie",
        "hdr_title_fr":"Vselennaya v kvadrate",
        "hdr_sub":     "Podzagolovok",
        "hdr_sub_fr":  "Glava -- Geometriya spektra prostykh chisel",
        "hdr_author":  "Avtor",
    },
    "zh": {
        "name": "Chinese",
        "native_name": "Zhongwen",
        "hdr_file":    "Wenjian",
        "hdr_date":    "Riqi",
        "hdr_date_fr": "Er ling er liu nian qi yue er shi si ri",
        "hdr_place":   "Didian",
        "hdr_place_fr":"Levis, Chaudiere-Appalaches, Jianada",
        "hdr_title":   "Biaoti",
        "hdr_title_fr":"Yuzhou de pingfang",
        "hdr_sub":     "Fu biaoti",
        "hdr_sub_fr":  "Zhangjie -- Suzhi pu de jihe",
        "hdr_author":  "Zuozhe",
    },
    "ja": {
        "name": "Japanese",
        "native_name": "Nihongo",
        "hdr_file":    "Fairu",
        "hdr_date":    "Hizuke",
        "hdr_date_fr": "Nisen nijuuroku nen shichi gatsu nijuuyokka",
        "hdr_place":   "Basho",
        "hdr_place_fr":"Levis, Shodyeru-Aparashu, Kanada",
        "hdr_title":   "Taitoru",
        "hdr_title_fr":"Nijou no uchuu",
        "hdr_sub":     "Sabu taitoru",
        "hdr_sub_fr":  "Shou -- Sosuu no supekutoramu no kikagaku",
        "hdr_author":  "Chosha",
    },
}


HEADER_TEMPLATE = """(*
================================================================================
  {hdr_file} : Methode_spectral.thy
    /fiʃje : metod spɛktʁal ti/
  {hdr_date} : {hdr_date_fr}
    /vɛ̃t katʁ ʒɥijɛ dø mil vɛ̃t sis/
  {hdr_place} : {hdr_place_fr}
    /levi ʃodjɛʁ apalak kanada/
  {hdr_title} : {hdr_title_fr}
    /lynivɛʁ ɛto kaʁe/
  {hdr_sub} : {hdr_sub_fr}
    /ʃapitʁ — la ʒeometʁi dy spɛktʁ dɛ nɔ̃bʁ pʁəmje/
  {hdr_author} : Philippe Thomas Savard
    /filip tɔma savaʁ/
================================================================================
*)
"""


# =============================================================================
# Etape 1 : PARSING - identifie tous les segments traduisibles
# =============================================================================

# Regex : capture (* ... *) et text \<open>...\<close>. On skip le TOUT PREMIER
# bloc de commentaire (l'entete metadata deja gere separement).
_RE_COMMENT = re.compile(r"\(\*.*?\*\)", re.DOTALL)
_RE_TEXT_BLOCK = re.compile(r"text\s*\\<open>.*?\\<close>", re.DOTALL)


def _find_balanced_text_blocks(content: str) -> list[tuple[int, int]]:
    """Trouve les text blocks Isabelle en gerant les \\<open>/\\<close> imbriques.

    Certains blocs `text \\<open>...\\<close>` contiennent des occurrences
    inline \\<open>ident\\<close> pour quoter un identificateur. Une regex
    naive `.*?` capture jusqu'au PREMIER \\<close>, coupant le bloc au
    milieu. On implemente un parser a pile qui matche correctement.

    Retourne une liste de (start, end) valides.
    """
    ranges: list[tuple[int, int]] = []
    OPEN = "\\<open>"
    CLOSE = "\\<close>"
    TEXT_MARK = "text"
    i = 0
    n = len(content)
    while i < n:
        # Cherche "text" suivi (apres whitespace) de \<open>
        idx_text = content.find(TEXT_MARK, i)
        if idx_text == -1:
            break
        # Verifie que c'est un mot isole (bord gauche + espace/newline apres)
        left_ok = (idx_text == 0 or not content[idx_text - 1].isalnum())
        if not left_ok:
            i = idx_text + 1
            continue
        # Skip whitespaces
        j = idx_text + len(TEXT_MARK)
        while j < n and content[j] in " \t\n\r":
            j += 1
        if not content[j:j + len(OPEN)] == OPEN:
            i = idx_text + 1
            continue
        # OK, on a un `text \<open>` -> parcourt jusqu'a la fermeture equilibree
        start = idx_text
        depth = 1
        k = j + len(OPEN)
        while k < n and depth > 0:
            if content[k:k + len(OPEN)] == OPEN:
                depth += 1
                k += len(OPEN)
            elif content[k:k + len(CLOSE)] == CLOSE:
                depth -= 1
                k += len(CLOSE)
            else:
                k += 1
        if depth == 0:
            ranges.append((start, k))
        i = k
    return ranges


def extract_segments(content: str, skip_header: bool = True) -> list[tuple[int, int, str, str]]:
    """Retourne une liste (start, end, kind, text_content) des segments traduisibles.

    kind est "comment" ou "text_block".
    Le TOUT PREMIER bloc de commentaire (metadata en-tete) est ignore si
    skip_header=True (il est traduit separement via HEADER_TEMPLATE).

    Les text blocks sont detectes via un parser a pile qui gere correctement
    les \\<open>/\\<close> imbriques (sinon la regex naive tronque au 1er close).
    """
    segments: list[tuple[int, int, str, str]] = []
    for m in _RE_COMMENT.finditer(content):
        segments.append((m.start(), m.end(), "comment", m.group(0)))
    # Text blocks avec parser balance
    for (s, e) in _find_balanced_text_blocks(content):
        segments.append((s, e, "text_block", content[s:e]))
    segments.sort(key=lambda s: s[0])
    # Retire les text_block qui recouvrent des comments (impossible en pratique
    # mais safety) et deduplique
    filtered: list[tuple[int, int, str, str]] = []
    last_end = -1
    for seg in segments:
        if seg[0] < last_end:
            continue  # chevauchement -> skip
        filtered.append(seg)
        last_end = seg[1]
    segments = filtered
    if skip_header and segments and segments[0][0] < 200:
        segments = segments[1:]
    return segments


# =============================================================================
# Etape 2 : TRADUCTION via Claude Sonnet 4.6
# =============================================================================

SYSTEM_PROMPT = (
    "You are a professional translator specialized in mathematical, "
    "philosophical, and formal-logic texts. You are translating fragments "
    "extracted from an Isabelle/HOL theory file about a spectral method for "
    "reconstructing prime numbers (author: Philippe Thomas Savard). "
    "\n\n"
    "STRICT RULES:\n"
    "1. Preserve EXACT semantic meaning (mathematical, epistemological, "
    "philosophical, ontological). Do NOT paraphrase, simplify, or add ideas.\n"
    "2. Preserve ALL identifiers, function names, and mathematical formulas "
    "verbatim (e.g. RsP, SA, SB, digamma, methode_spectral, sum_list, "
    "asymetrique_ordonnee_nat, etc.).\n"
    "3. Preserve ALL Isabelle syntax markers: '(*', '*)', 'text', "
    "'\\<open>', '\\<close>' — these MUST appear identically in the output.\n"
    "4. Preserve ALL numerical values, section numbers, bibliographic "
    "references (e.g. 'pdf::page_26', 'methode_spectral.thy::lemma_X').\n"
    "5. Preserve the exact LINE BREAKS and INDENTATION structure inside "
    "each segment (keep the same number of lines and leading spaces where "
    "possible).\n"
    "6. Translate ONLY the natural-language French prose. Author names, "
    "proper nouns (Philippe Thomas Savard, Riemann, Chebyshev, Savard, "
    "Isabelle/HOL) stay UNCHANGED.\n"
    "7. If a word/phrase has no direct equivalent (e.g. 'Pont Savard'), "
    "keep the French form and add a brief parenthetical gloss on first "
    "occurrence only.\n"
    "8. Output MUST be a valid JSON object mapping each segment ID to its "
    "translated text. Nothing else. No preamble, no explanation.\n"
)

TRANSLATION_USER_PROMPT = """Translate the following Isabelle theory-file fragments from French to {target_language} ({native_name}).

Return a JSON object with the SAME keys, each value being the translated segment.

Segments (JSON):
{segments_json}

Respond ONLY with the JSON object. Start with {{ and end with }}."""


async def translate_segments_batch(
    segments: dict[str, str],
    lang_code: str,
    lang_info: dict[str, str],
) -> dict[str, str]:
    """Envoie un batch de segments a Claude, recoit la traduction JSON."""
    chat = (
        LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=f"translate-{lang_code}-{id(segments)}",
            system_message=SYSTEM_PROMPT,
        )
        .with_model(MODEL_PROVIDER, MODEL_NAME)
        .with_params(temperature=0.0, max_tokens=16000)
    )

    prompt = TRANSLATION_USER_PROMPT.format(
        target_language=lang_info["name"],
        native_name=lang_info["native_name"],
        segments_json=json.dumps(segments, ensure_ascii=False, indent=2),
    )
    response = await chat.send_message(UserMessage(text=prompt))
    # response can be str or object depending on library version
    text = response if isinstance(response, str) else str(response)
    # Extract JSON from response (defensive : LLM peut envelopper d'un preambule)
    # Robuste : cherche depuis le premier { jusqu'au dernier } equilibre.
    return _robust_json_extract(text)


def _robust_json_extract(text: str) -> dict[str, str]:
    """Parser JSON tolerant : gere les code fences ```json...``` et retente
    avec des reparations progressives si le JSON brut echoue.

    Strategies successives :
      1. json.loads sur le contenu entre premier { et dernier }
      2. Retire les code fences ``` autour
      3. Essai avec json5 si dispo (permet trailing commas, chaines multi-lignes)
      4. Ligne-par-ligne : reconstruit un dict a partir de "seg_XXX": "..."
    """
    import json
    # Strategy 1 : premier { ... dernier }
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        raise ValueError(f"Reponse LLM sans JSON detecte : {text[:200]!r}")
    payload = m.group(0)
    # Retire eventuel wrapping ```json ... ```
    payload = re.sub(r"^```(?:json)?\s*", "", payload)
    payload = re.sub(r"\s*```\s*$", "", payload)
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        pass
    # Strategy 2 : essaie de reparer avec json5 (permissif)
    try:
        import json5  # type: ignore
        return json5.loads(payload)
    except ImportError:
        pass
    except Exception:
        pass
    # Strategy 3 : reconstruction manuelle - matche "seg_XXX": "...contenu..."
    # jusqu'a une double-quote non-echapee suivie de , ou } au niveau top
    result: dict[str, str] = {}
    # Pattern relachee : capture cle et valeur en autorisant multi-lignes
    kv_pattern = re.compile(
        r'"(seg_\d+)"\s*:\s*"((?:[^"\\]|\\.)*)"',
        re.DOTALL,
    )
    for match in kv_pattern.finditer(payload):
        key = match.group(1)
        # Deserialise la string JSON-encoded (traite les \n, \", \\, etc.)
        try:
            val = json.loads('"' + match.group(2) + '"')
        except json.JSONDecodeError:
            val = match.group(2)  # fallback : garde tel quel
        result[key] = val
    if not result:
        raise ValueError(f"JSON irrecuperable : {payload[:300]!r}")
    return result


async def translate_all_segments(
    segments_by_id: dict[str, str],
    lang_code: str,
    lang_info: dict[str, str],
    batch_size: int = 40,
) -> dict[str, str]:
    """Traduit tous les segments par batches, avec retry par batch.

    Post-validation : chaque segment traduit doit preserver EXACTEMENT :
      - Le nombre de \\<open> et \\<close>
      - Les delimiteurs de commentaire (* et *)
      - Le mot-cle 'text' au debut si present
    Sinon on garde le segment FR original (safety).
    """
    OPEN = "\\<open>"
    CLOSE = "\\<close>"
    items = list(segments_by_id.items())
    result: dict[str, str] = {}
    total = len(items)
    n_batches = (total + batch_size - 1) // batch_size
    n_repaired = 0

    for i in range(0, total, batch_size):
        batch = dict(items[i:i + batch_size])
        batch_num = i // batch_size + 1
        print(f"  [{lang_code}] batch {batch_num}/{n_batches} ({len(batch)} segments)...", flush=True)
        for attempt in range(3):
            try:
                translated = await translate_segments_batch(batch, lang_code, lang_info)
                # Validation structurelle par segment
                for k, orig in batch.items():
                    tr = translated.get(k)
                    if tr is None:
                        result[k] = orig  # LLM oublie ce segment
                        n_repaired += 1
                        continue
                    # Verifie balance \<open>/\<close>
                    n_open_orig = orig.count(OPEN)
                    n_close_orig = orig.count(CLOSE)
                    n_open_tr = tr.count(OPEN)
                    n_close_tr = tr.count(CLOSE)
                    # Verifie balance (* / *) pour les comments
                    n_com_open_orig = orig.count("(*")
                    n_com_close_orig = orig.count("*)")
                    n_com_open_tr = tr.count("(*")
                    n_com_close_tr = tr.count("*)")
                    ok_isabelle = (n_open_tr == n_open_orig and n_close_tr == n_close_orig)
                    ok_comment = (n_com_open_tr == n_com_open_orig and n_com_close_tr == n_com_close_orig)
                    if not (ok_isabelle and ok_comment):
                        # Fallback : preserve FR original pour ce segment
                        result[k] = orig
                        n_repaired += 1
                    else:
                        result[k] = tr
                break
            except Exception as exc:
                print(f"    [!] tentative {attempt+1}/3 : {exc}", flush=True)
                if attempt == 2:
                    print(f"    [!] echec batch {batch_num}, fallback FR conserve", flush=True)
                    for k, v in batch.items():
                        result[k] = v
                        n_repaired += 1
                await asyncio.sleep(2)
    if n_repaired:
        print(f"  [{lang_code}] {n_repaired} segments repares (FR conserve pour preserver structure Isabelle)", flush=True)
    return result


# =============================================================================
# Etape 3 : REASSEMBLAGE - substitue les segments traduits dans le fichier
# =============================================================================

def rebuild_thy(
    original_content: str,
    segments: list[tuple[int, int, str, str]],
    translations: dict[str, str],
    header: str,
) -> str:
    """Reconstruit le .thy avec les segments traduits.

    Substitue chaque segment original par sa traduction, EN SENS INVERSE
    (fin -> debut) pour que les indices restent valables.

    IMPORTANT : les seg_id des translations sont construits sur les positions
    de original_content. On garde ces IDs identiques apres retrait du header
    en preservant le mapping (start_original -> seg_id) tout en manipulant
    les positions ajustees pour la substitution.
    """
    # Trouve la position de la fin de l'entete francais existant
    m_header = re.match(r"\(\*.*?\*\)\s*", original_content, re.DOTALL)
    if m_header:
        body = original_content[m_header.end():]
        header_end_offset = m_header.end()
    else:
        body = original_content
        header_end_offset = 0

    # Chaque entree : (start_ajuste, end_ajuste, seg_id_original)
    entries = []
    for (start, end, kind, text) in segments:
        seg_id = f"seg_{start:07d}"  # ID base sur position ORIGINALE (comme au build)
        adj_start = start - header_end_offset
        adj_end = end - header_end_offset
        if adj_start < 0:
            continue  # segment dans le header, deja gere
        entries.append((adj_start, adj_end, seg_id, text))

    working = body
    for (adj_start, adj_end, seg_id, orig_text) in sorted(entries, key=lambda s: s[0], reverse=True):
        translated = translations.get(seg_id, orig_text)  # fallback FR si echec
        working = working[:adj_start] + translated + working[adj_end:]

    return header + working


# =============================================================================
# Etape 4 : PIPELINE ORCHESTRATION
# =============================================================================

async def translate_language(
    lang_code: str,
    original_content: str,
    segments: list[tuple[int, int, str, str]],
) -> Path:
    """Traduit et ecrit un .thy pour une langue donnee."""
    lang_info = LANGUAGES[lang_code]
    print(f"\n=== Traduction vers {lang_info['name']} ({lang_code}) ===", flush=True)

    # Build segments_by_id : cle = id stable base sur position start
    segments_by_id: dict[str, str] = {}
    for (start, end, kind, text) in segments:
        seg_id = f"seg_{start:07d}"
        segments_by_id[seg_id] = text

    # Traduit
    translations = await translate_all_segments(segments_by_id, lang_code, lang_info)

    # Build header
    header = HEADER_TEMPLATE.format(**lang_info) + "\n"

    # Reassemble
    new_content = rebuild_thy(original_content, segments, translations, header)

    # Ecrit
    out_path = THY_OUT_DIR / f"methode_spectral_{lang_code}.thy"
    out_path.write_text(new_content, encoding="utf-8")
    print(f"  [OK] {out_path} ({len(new_content)} chars, "
          f"{len(new_content.splitlines())} lignes)", flush=True)
    return out_path


async def main(target_langs: list[str] | None = None):
    original = THY_SOURCE.read_text(encoding="utf-8")
    segments = extract_segments(original, skip_header=True)
    print(f"[INFO] Fichier source : {THY_SOURCE}")
    print(f"[INFO] Segments a traduire : {len(segments)}")
    print(f"[INFO] Taille totale : {sum(len(s[3]) for s in segments)} chars")

    if target_langs is None:
        target_langs = list(LANGUAGES.keys())
    for code in target_langs:
        if code not in LANGUAGES:
            print(f"[SKIP] Langue inconnue : {code}")
            continue
        await translate_language(code, original, segments)

    print("\n[FIN] Traductions terminees.")


if __name__ == "__main__":
    langs = sys.argv[1:] if len(sys.argv) > 1 else None
    asyncio.run(main(langs))

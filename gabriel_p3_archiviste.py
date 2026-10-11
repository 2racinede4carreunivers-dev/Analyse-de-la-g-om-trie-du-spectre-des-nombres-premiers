#!/usr/bin/env python3
# =============================================================================
#  gabriel_p3_archiviste.py
#  PIPELINE COGNITIF GABRIEL — ÉTAPE 3
#  Archiviste orchestrateur — Recherche dans gabriel_corpus.db
#  Évaluation de pertinence Q&R + réponse LLM via 7 moteurs Gabriel
#
#  Dépôt   : C:\agent-multiloop-Gabriel-local-final
#  Entrée  : gabriel_corpus.db  (sortie étape 2)
#  Usage   : python gabriel_p3_archiviste.py
#            python gabriel_p3_archiviste.py --question "Que démontre RsP_un_demi_general ?"
#            python gabriel_p3_archiviste.py --interactif
# =============================================================================

import sqlite3, json, re, sys, os, argparse
from pathlib import Path
from datetime import datetime
from typing import Optional

RACINE = Path(r"C:\agent-multiloop-Gabriel-local-final")
DB_PATH = RACINE / "gabriel_corpus.db"

# ─────────────────────────────────────────────────────────────────────────────
#  CHEMINS RÉELS DES MOTEURS GABRIEL (issus de gabriel_repo_map.json)
#  Chaque moteur est un module Python du dépôt identifié par le cartographe
# ─────────────────────────────────────────────────────────────────────────────

MOTEURS_GABRIEL = {
    "moteur_1_orchestrateur": {
        "nom":         "Orchestrateur central",
        "description": "Coordonne les 7 moteurs, route les requêtes, agrège les réponses",
        "chemins_candidats": [
            RACINE / "backend" / "orchestrator.py",
            RACINE / "src" / "core" / "orchestrator.py",
            RACINE / "agent-multiloop-Gabriel-local" / "src" / "core" / "orchestrator.py",
        ],
        "specialite":  ["orchestration", "routing", "coordination"],
        "spheres":     ["Ensemble"],
    },
    "moteur_2_spectral": {
        "nom":         "Moteur Spectral HOL",
        "description": "Analyse spectrale, rapports RsP, suites SA/SB, postulats HOL",
        "chemins_candidats": [
            RACINE / "backend" / "spectral_engine.py",
            RACINE / "src" / "engines" / "spectral_engine.py",
            RACINE / "agent-multiloop-Gabriel-local" / "src" / "engines" / "spectral_engine.py",
        ],
        "specialite":  ["SA", "SB", "RsP", "digamma", "spectral_postulate", "HOL", "Isabelle"],
        "spheres":     ["1/ms"],
    },
    "moteur_3_theoremes": {
        "nom":         "Moteur Théorèmes",
        "description": "Lemmes, théorèmes Isabelle/HOL, preuves formelles, pont Savard",
        "chemins_candidats": [
            RACINE / "backend" / "theorem_engine.py",
            RACINE / "src" / "engines" / "theorem_engine.py",
            RACINE / "agent-multiloop-Gabriel-local" / "src" / "engines" / "theorem_engine.py",
        ],
        "specialite":  ["lemma", "theorem", "proof", "Isabelle", "HOL", "pont_savard",
                        "ensemble_savard", "synthese_pont_savard"],
        "spheres":     ["1/t"],
    },
    "moteur_4_geometrie": {
        "nom":         "Moteur Géométrie Spectrale",
        "description": "Extensions géométriques, RSA, zéros de Riemann, opérateur de Hilbert",
        "chemins_candidats": [
            RACINE / "backend" / "geometry_engine.py",
            RACINE / "src" / "engines" / "geometry_engine.py",
            RACINE / "agent-multiloop-Gabriel-local" / "src" / "engines" / "geometrie_spectrale_engine.py",
        ],
        "specialite":  ["RSA_ratio", "riemann_zero", "geometric_area", "quadrature",
                        "Archimede", "validation_hol"],
        "spheres":     ["1/x"],
    },
    "moteur_5_memoire": {
        "nom":         "Moteur Mémoire",
        "description": "Historique des sessions, contexte conversationnel, mémoire persistante",
        "chemins_candidats": [
            RACINE / "memory" / "memory_engine.py",
            RACINE / "backend" / "memory.py",
            RACINE / "agent-multiloop-Gabriel-local" / "memory" / "dictionnaire_spectral.py",
        ],
        "specialite":  ["historique", "contexte", "session", "memoire"],
        "spheres":     ["Ensemble"],
    },
    "moteur_6_llm": {
        "nom":         "Moteur LLM",
        "description": "Interface LLM (Ollama/OpenAI), génération de réponses adaptées",
        "chemins_candidats": [
            RACINE / "backend" / "llm_client.py",
            RACINE / "src" / "adapters" / "llm" / "ollama_client.py",
            RACINE / "agent-multiloop-Gabriel-local" / "src" / "adapters" / "llm" / "ollama_client.py",
        ],
        "specialite":  ["llm", "génération", "réponse", "langage"],
        "spheres":     ["Ensemble"],
    },
    "moteur_7_corpus": {
        "nom":         "Moteur Corpus HOL",
        "description": "Chargeur et indexeur du corpus Isabelle/HOL, interface vers gabriel_corpus.db",
        "chemins_candidats": [
            RACINE / "backend" / "corpus_engine.py",
            RACINE / "src" / "adapters" / "corpus" / "thy_loader.py",
            RACINE / "agent-multiloop-Gabriel-local" / "src" / "adapters" / "corpus" / "thy_loader.py",
        ],
        "specialite":  ["corpus", "thy", "isabelle", "base_de_donnees", "indexation"],
        "spheres":     ["1/ms", "1/t", "1/x"],
    },
}


# ─────────────────────────────────────────────────────────────────────────────
#  NORMALISATION ET SEGMENTATION DES QUESTIONS
# ─────────────────────────────────────────────────────────────────────────────

STOP_MOTS = {
    "le","la","les","un","une","des","de","du","est","que","qui","quoi","comment",
    "dans","avec","pour","sur","par","en","au","aux","et","ou","mais","car",
    "quel","quelle","quels","quelles","cette","ces","ce","il","elle","ils","elles",
    "se","sa","son","ses","leur","leurs","me","te","nous","vous","je","tu",
    "how","what","which","does","the","and","for","with","from","that","this",
}

def normaliser(texte: str) -> str:
    return re.sub(r'\s+', ' ', texte.lower().strip())

def extraire_mots_cles(question: str) -> list[str]:
    """Extrait les mots-clés pertinents d'une question."""
    q_norm = normaliser(question)
    # Suppression ponctuation mais garder _ et /
    tokens = re.findall(r'[a-zàâäéèêëïîôùûü_\d]+(?:/\d)?', q_norm)
    return [t for t in tokens if len(t) > 2 and t not in STOP_MOTS]

def detecter_entites_hol(question: str, mots_cles: list[str]) -> list[str]:
    """Détecte les noms d'entités HOL directement mentionnés dans la question."""
    entites = []
    # Patterns HOL typiques (CamelCase, snake_case, avec chiffres)
    patterns = [
        r'\bRsP[_\w]*\b', r'\bSA[_\w]*\b', r'\bSB[_\w]*\b',
        r'\bA_\d[_\w]*\b', r'\bB_\d[_\w]*\b',
        r'\bspectral[_\w]*\b', r'\bdigamma[_\w]*\b',
        r'\blemma[_\s]\w+\b', r'\btheorem[_\s]\w+\b',
        r'\b[a-z]+_[a-z]+(?:_[a-z\d]+)*\b',
    ]
    for pat in patterns:
        for m in re.finditer(pat, question, re.IGNORECASE):
            entites.append(m.group(0))
    # Termes spécifiques connus
    termes_hol = [
        "pont_savard", "ensemble_savard", "pont_spectral_direct_final",
        "synthese_pont_savard", "alignement_central", "conclusion_ensemble",
        "RsP_un_demi_general", "RsP_un_tiers_constant", "RsP_un_quart_constant",
        "prime_equation_for_primes_pos", "spectral_postulate_pos",
        "reconstruction_premier_pos", "RSA_convergence_implies_distance_decreasing",
        "global_consistency", "riemann_zeros_eigenvalues_correspondence",
    ]
    q_low = question.lower()
    for terme in termes_hol:
        if terme.lower() in q_low:
            entites.append(terme)
    return list(set(entites))


# ─────────────────────────────────────────────────────────────────────────────
#  CLASSE ARCHIVISTE — CŒUR DU MOTEUR DE RECHERCHE
# ─────────────────────────────────────────────────────────────────────────────

class ArchivisteGabriel:

    def __init__(self):
        self.conn: Optional[sqlite3.Connection] = None
        self._moteurs_resolus: dict = {}

    def connecter(self):
        if not DB_PATH.exists():
            print(f"\n  ✗ gabriel_corpus.db introuvable : {DB_PATH}")
            print("  → Exécutez d'abord :")
            print("      python gabriel_p1_keyword_extractor.py")
            print("      python gabriel_p2_sqlite_builder.py")
            sys.exit(1)
        self.conn = sqlite3.connect(str(DB_PATH))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        # Résoudre les chemins réels des moteurs Gabriel
        self._resoudre_moteurs()

    def _resoudre_moteurs(self):
        """Trouve le chemin réel existant pour chaque moteur."""
        for moteur_id, moteur in MOTEURS_GABRIEL.items():
            for chemin in moteur["chemins_candidats"]:
                if chemin.exists():
                    self._moteurs_resolus[moteur_id] = str(chemin)
                    break
            else:
                self._moteurs_resolus[moteur_id] = None  # chemin non trouvé

    def fermer(self):
        if self.conn:
            self.conn.close()

    # ──────────────────────────────────────────────────────────────
    #  RECHERCHE PRINCIPALE
    # ──────────────────────────────────────────────────────────────

    def rechercher(self, question: str, top_k: int = 5) -> dict:
        """
        Orchestrateur central de recherche — Étape 3 du pipeline.
        Input  : question brute de l'utilisateur
        Output : dict complet avec Q&R, entités, sphères, contexte LLM
        """
        mots_cles  = extraire_mots_cles(question)
        entites_hol = detecter_entites_hol(question, mots_cles)

        # 1. Recherche dans l'index des mots-clés
        qr_scores = self._scorer_qr_via_index(mots_cles, entites_hol)

        # 2. Recherche directe par entités HOL dans la DB
        entites_trouvees = self._rechercher_entites(entites_hol + mots_cles)

        # 3. Identifier les sphères activées
        spheres_activees = self._identifier_spheres(qr_scores, entites_trouvees)

        # 4. Récupérer les Q&R top-k
        qr_top = self._recuperer_qr_top(qr_scores, top_k)

        # 5. Récupérer les liens HOL pertinents
        liens_hol = self._recuperer_liens_hol(entites_trouvees[:10])

        # 6. Sélectionner les moteurs Gabriel appropriés
        moteurs_actifs = self._selectionner_moteurs(spheres_activees, mots_cles)

        # 7. Construire le contexte pour le LLM
        contexte_llm = self._construire_contexte_llm(
            question, qr_top, entites_trouvees, spheres_activees, liens_hol
        )

        # 8. Construire la réponse composite
        score_global = max((s for _, s in qr_scores[:5]), default=0.0) if qr_scores else 0.0

        resultat = {
            "question_brute":     question,
            "mots_cles_detectes": mots_cles,
            "entites_hol_detectees": entites_hol,
            "score_confiance":    round(score_global, 3),
            "qr_pertinentes":     qr_top,
            "entites_hol_activees": entites_trouvees[:15],
            "spheres_activees":   spheres_activees,
            "liens_hol_pertinents": liens_hol[:10],
            "moteurs_actifs":     moteurs_actifs,
            "contexte_llm":       contexte_llm,
            "timestamp":          datetime.now().isoformat(),
        }

        # 9. Sauvegarder la session dans la DB
        self._sauvegarder_session(resultat, moteurs_actifs)

        return resultat

    def _scorer_qr_via_index(self, mots_cles: list[str],
                              entites_hol: list[str]) -> list[tuple[str, float]]:
        """Score chaque Q&R en combinant index mots-clés et entités HOL."""
        scores: dict[str, float] = {}

        # Via l'index des mots-clés
        for mc in mots_cles:
            rows = self.conn.execute(
                "SELECT qr_ids, frequence FROM index_mots_cles WHERE mot_cle LIKE ?",
                (f"%{mc}%",)
            ).fetchall()
            for row in rows:
                qr_ids = json.loads(row["qr_ids"] or "[]")
                freq   = row["frequence"] or 1
                for qr_id in qr_ids:
                    scores[qr_id] = scores.get(qr_id, 0.0) + (1.0 / (1 + len(mc))) * freq

        # Bonus pour entités HOL directement mentionnées
        for ent_nom in entites_hol:
            rows = self.conn.execute("""
                SELECT l.qr_id, l.score
                FROM liens_qr_entite l
                JOIN entites_hol e ON l.entite_id = e.id
                WHERE e.nom LIKE ? OR e.nom = ?
            """, (f"%{ent_nom}%", ent_nom)).fetchall()
            for row in rows:
                scores[row["qr_id"]] = scores.get(row["qr_id"], 0.0) + row["score"] * 1.5

        # Tri par score décroissant + normalisation [0,1]
        if not scores:
            return []
        max_s = max(scores.values())
        return sorted([(qid, s/max_s) for qid, s in scores.items()],
                      key=lambda x: -x[1])

    def _recuperer_qr_top(self, qr_scores: list[tuple[str, float]],
                           top_k: int) -> list[dict]:
        """Récupère les données complètes des top Q&R."""
        if not qr_scores:
            # Fallback : retourner toutes les Q&R par ordre alphabétique
            rows = self.conn.execute(
                "SELECT * FROM qr_techniques ORDER BY id LIMIT ?", (top_k,)
            ).fetchall()
        else:
            ids_top = [qid for qid, _ in qr_scores[:top_k]]
            placeholders = ",".join("?" * len(ids_top))
            rows = self.conn.execute(
                f"SELECT * FROM qr_techniques WHERE id IN ({placeholders})",
                ids_top
            ).fetchall()

        resultats = []
        for row in rows:
            qr_id   = row["id"]
            score   = next((s for qid, s in qr_scores if qid == qr_id), 0.0)
            # Entités HOL associées à cette Q&R
            entites = self.conn.execute("""
                SELECT e.nom, e.type_hol, e.sphere_id, e.cercle_niveau, l.score
                FROM liens_qr_entite l
                JOIN entites_hol e ON l.entite_id = e.id
                WHERE l.qr_id = ?
                ORDER BY l.score DESC LIMIT 8
            """, (qr_id,)).fetchall()

            resultats.append({
                "id":           qr_id,
                "niveau":       row["niveau"] or "avance",
                "question":     row["question"] or "",
                "resume":       row["resume"] or "",
                "categorie":    row["categorie"] or "",
                "source":       row["source_fichier"] or "",
                "spheres":      json.loads(row["spheres"] or "[]"),
                "sphere_prim":  row["sphere_primaire"] or "—",
                "mots_cles":    json.loads(row["mots_cles"] or "[]"),
                "score_pertinence": round(score, 3),
                "entites_associees": [
                    {"nom":    e["nom"] or "",
                     "type":   e["type_hol"] or "?",
                     "sphere": e["sphere_id"] or "—",
                     "cercle": e["cercle_niveau"],
                     "score":  e["score"] or 0.0}
                    for e in entites
                ],
            })
        return sorted(resultats, key=lambda x: -x["score_pertinence"])

    def _rechercher_entites(self, termes: list[str]) -> list[dict]:
        """Recherche les entités HOL correspondant aux termes."""
        trouvees = []
        vus = set()
        for terme in termes:
            rows = self.conn.execute("""
                SELECT e.id, e.nom, e.type_hol, e.source_fichier,
                       e.occurrences, e.sphere_id, e.cercle_niveau, e.contexte
                FROM entites_hol e
                WHERE e.nom LIKE ? OR e.nom = ?
                ORDER BY e.occurrences DESC
                LIMIT 5
            """, (f"%{terme}%", terme)).fetchall()
            for row in rows:
                if row["nom"] not in vus:
                    vus.add(row["nom"])
                    trouvees.append({
                        "id":          row["id"],
                        "nom":         row["nom"] or "",
                        "type":        row["type_hol"] or "?",
                        "source":      row["source_fichier"] or "—",
                        "occurrences": row["occurrences"] or 0,
                        "sphere":      row["sphere_id"] or "—",
                        "cercle":      row["cercle_niveau"],   # peut rester None
                        "contexte":    (row["contexte"] or "")[:200],
                    })
        return trouvees

    def _recuperer_liens_hol(self, entites: list[dict]) -> list[dict]:
        """Récupère les liens inter-entités HOL pour les entités trouvées."""
        if not entites:
            return []
        ids = [e["id"] for e in entites if "id" in e]
        if not ids:
            return []
        placeholders = ",".join("?" * len(ids))
        rows = self.conn.execute(f"""
            SELECT
                es.nom AS source_nom, es.sphere_id AS source_sphere,
                ec.nom AS cible_nom,  ec.sphere_id AS cible_sphere,
                h.relation, h.source_fichier
            FROM liens_hol h
            JOIN entites_hol es ON h.source_id = es.id
            JOIN entites_hol ec ON h.cible_id  = ec.id
            WHERE h.source_id IN ({placeholders}) OR h.cible_id IN ({placeholders})
            ORDER BY h.relation
            LIMIT 20
        """, ids + ids).fetchall()
        return [
            {"source": r["source_nom"], "sphere_src": r["source_sphere"],
             "cible":  r["cible_nom"],  "sphere_cib": r["cible_sphere"],
             "relation": r["relation"], "fichier": r["source_fichier"]}
            for r in rows
        ]

    def _identifier_spheres(self, qr_scores: list, entites: list[dict]) -> list[str]:
        """Identifie les sphères (1/ms, 1/t, 1/x) activées par la requête."""
        compteur: dict[str, float] = {"1/ms": 0, "1/t": 0, "1/x": 0, "Ensemble": 0}
        # Depuis les Q&R scorées
        for qr_id, score in qr_scores[:10]:
            row = self.conn.execute(
                "SELECT spheres FROM qr_techniques WHERE id=?", (qr_id,)
            ).fetchone()
            if row:
                for sph in json.loads(row["spheres"] or "[]"):
                    compteur[sph] = compteur.get(sph, 0) + score
        # Depuis les entités trouvées
        for ent in entites:
            sph = ent.get("sphere")
            if sph and sph in compteur:
                compteur[sph] += 0.5
        # Retourner les sphères avec score > 0, triées par score
        return [s for s, v in sorted(compteur.items(), key=lambda x: -x[1]) if v > 0]

    def _selectionner_moteurs(self, spheres: list[str], mots_cles: list[str]) -> list[dict]:
        """Sélectionne les moteurs Gabriel appropriés selon les sphères activées."""
        SPHERE_MOTEUR = {
            "1/ms":    ["moteur_2_spectral",  "moteur_7_corpus"],
            "1/t":     ["moteur_3_theoremes", "moteur_7_corpus"],
            "1/x":     ["moteur_4_geometrie", "moteur_7_corpus"],
            "Ensemble":["moteur_1_orchestrateur", "moteur_5_memoire", "moteur_6_llm"],
        }
        moteurs_ids = set(["moteur_1_orchestrateur", "moteur_6_llm"])
        for sph in spheres:
            for mid in SPHERE_MOTEUR.get(sph, []):
                moteurs_ids.add(mid)
        # Toujours inclure moteur_5_memoire
        moteurs_ids.add("moteur_5_memoire")

        result = []
        for mid in moteurs_ids:
            moteur = MOTEURS_GABRIEL.get(mid, {})
            chemin = self._moteurs_resolus.get(mid)
            result.append({
                "id":          mid,
                "nom":         moteur.get("nom", mid),
                "description": moteur.get("description", ""),
                "specialite":  moteur.get("specialite", []),
                "spheres":     moteur.get("spheres", []),
                "chemin_reel": chemin,
                "actif":       chemin is not None,
            })
        return sorted(result, key=lambda x: x["id"])

    def _construire_contexte_llm(self, question: str, qr_top: list[dict],
                                  entites: list[dict], spheres: list[str],
                                  liens_hol: list[dict]) -> str:
        """Construit le prompt de contexte à injecter dans le LLM de Gabriel."""
        lignes = [
            "=== CONTEXTE COGNITIF — PIPELINE GABRIEL (Étape 3) ===",
            f"Question : {question}",
            f"Sphères activées : {', '.join(spheres) if spheres else 'Ensemble'}",
            f"Équation centrale : Ensemble = 1  ↔  1/x + 1/t + 1/ms",
            "",
            "--- Q&R TECHNIQUES PERTINENTES (corpus Savard) ---",
        ]
        for i, qr in enumerate(qr_top[:5], 1):
            lignes += [
                f"[{i}] {qr['id']} [{qr['niveau']}] — Score : {qr['score_pertinence']:.3f}",
                f"     Q : {qr['question']}",
                f"     R : {qr['resume']}",
                f"     Sphère : {qr['sphere_prim']} | Catégorie : {qr['categorie']}",
            ]
            if qr["entites_associees"]:
                ent_str = ", ".join(
                    f"{e['nom']} ({e['sphere'] or '—'} cercle {e['cercle'] if e['cercle'] is not None else '—'})"
                    for e in qr["entites_associees"][:4]
                )
                lignes.append(f"     Entités HOL : {ent_str}")
            lignes.append("")

        if entites:
            lignes += ["--- ENTITÉS HOL ACTIVÉES ---"]
            for e in entites[:8]:
                lignes.append(
                    f"  • {e.get('nom',''):40s} [{e.get('type','') or '':12s}] — "
                    f"sphère {e.get('sphere') or '—':4s} cercle {str(e.get('cercle')) if e.get('cercle') is not None else '—'} "
                    f"({e.get('source') or '—'}, {e.get('occurrences',0)} occ.)"
                )
            lignes.append("")

        if liens_hol:
            lignes += ["--- GRAPHE DE VALIDATION HOL (liens actifs) ---"]
            for lien in liens_hol[:6]:
                lignes.append(
                    f"  {lien['source']} [{lien['sphere_src']}] "
                    f"──{lien['relation']}──▶ "
                    f"{lien['cible']} [{lien['sphere_cib']}]"
                )
            lignes.append("")

        lignes += [
            "--- INSTRUCTION AU LLM ---",
            "En te basant exclusivement sur le contexte ci-dessus (Q&R du corpus Savard,",
            "entités HOL de methode_spectral.thy et validation_hol_unifiee.thy),",
            "génère une réponse précise, formellement ancrée et conséquente aux",
            "sphères activées (1/ms, 1/t, 1/x) et à l'équation Ensemble = 1/x + 1/t + 1/ms.",
            "Cite les entités HOL pertinentes et leurs cercles concentriques.",
            "======================================================",
        ]
        return "\n".join(lignes)

    def _sauvegarder_session(self, resultat: dict, moteurs: list[dict]):
        """Persiste la session dans la table sessions de la DB."""
        moteur_nom = ", ".join(m["nom"] for m in moteurs[:3] if m.get("actif"))
        self.conn.execute("""
            INSERT INTO sessions
            (question_brute, question_norm, mots_cles_detectes, qr_ids_retournees,
             entites_activees, spheres_activees, moteur_gabriel,
             score_confiance, reponse_generee)
            VALUES (?,?,?,?,?,?,?,?,?)
        """, (
            resultat["question_brute"],
            normaliser(resultat["question_brute"]),
            json.dumps(resultat["mots_cles_detectes"],  ensure_ascii=False),
            json.dumps([q["id"] for q in resultat["qr_pertinentes"]], ensure_ascii=False),
            json.dumps([e["nom"] for e in resultat["entites_hol_activees"][:10]], ensure_ascii=False),
            json.dumps(resultat["spheres_activees"], ensure_ascii=False),
            moteur_nom,
            resultat["score_confiance"],
            resultat["contexte_llm"][:2000],
        ))
        self.conn.commit()

    # ──────────────────────────────────────────────────────────────
    #  AFFICHAGE DES RÉSULTATS
    # ──────────────────────────────────────────────────────────────

    @staticmethod
    def _s(val, default='—') -> str:
        """Convertit None en chaîne sécurisée pour les f-strings."""
        return str(val) if val is not None else default

    def afficher_resultat(self, res: dict, verbeux: bool = True):
        print("\n" + "="*70)
        print("  GABRIEL — RÉSULTAT ARCHIVISTE")
        print("="*70)
        print(f"\n  Question : {res['question_brute']}")
        print(f"  Mots-clés détectés  : {', '.join(res['mots_cles_detectes'][:8])}")
        print(f"  Entités HOL directes: {', '.join(res['entites_hol_detectees'][:5]) or '—'}")
        print(f"  Sphères activées    : {', '.join(res['spheres_activees']) or 'Ensemble'}")
        print(f"  Score de confiance  : {res['score_confiance']:.3f}")

        print(f"\n  ┌── Q&R PERTINENTES ({len(res['qr_pertinentes'])} trouvées)")
        for qr in res["qr_pertinentes"]:
            sph = "/".join(qr["spheres"][:2])
            print(f"  │  [{qr['id']}] [{qr['niveau']:15s}] score={qr['score_pertinence']:.3f} "
                  f"sphère={qr['sphere_prim']}")
            print(f"  │    Q : {qr['question'][:80]}...")
            print(f"  │    R : {qr['resume'][:80]}...")
            if qr["entites_associees"] and verbeux:
                ent_str = ", ".join(e["nom"] for e in qr["entites_associees"][:4])
                print(f"  │    Entités HOL : {ent_str}")
            print("  │")
        print("  └──")

        if verbeux and res["entites_hol_activees"]:
            print(f"\n  ┌── ENTITÉS HOL ACTIVÉES ({len(res['entites_hol_activees'])} trouvées)")
            for e in res["entites_hol_activees"][:8]:
                sph = e['sphere'] or '—'
                cer = str(e['cercle']) if e['cercle'] is not None else '—'
                print(f"  │  {e['nom']:40s} [{e['type'] or '':12s}] "
                      f"sphère {sph:4s} cercle {cer}")
            print("  └──")

        if verbeux and res["liens_hol_pertinents"]:
            print(f"\n  ┌── GRAPHE HOL ACTIF ({len(res['liens_hol_pertinents'])} liens)")
            for lien in res["liens_hol_pertinents"][:6]:
                rel = lien.get('relation') or '—'
                print(f"  │  {lien.get('source',''):30s} ─{rel:15s}▶ {lien.get('cible','')}")
            print("  └──")

        print(f"\n  ┌── MOTEURS GABRIEL ACTIVÉS")
        for m in res["moteurs_actifs"]:
            statut = "✓" if m["actif"] else "✗"
            print(f"  │  {statut} {m['nom']:35s} — {', '.join(m['spheres'])}")
        print("  └──")

        print(f"\n  ┌── CONTEXTE LLM GÉNÉRÉ ({len(res['contexte_llm'])} chars)")
        for ligne in res["contexte_llm"].split('\n')[:15]:
            print(f"  │  {ligne}")
        print("  │  [...]")
        print("  └──")
        print()

    # ──────────────────────────────────────────────────────────────
    #  UTILITAIRES
    # ──────────────────────────────────────────────────────────────

    def stats_db(self):
        """Affiche les statistiques de la base de données."""
        print("\n" + "="*50)
        print("  STATISTIQUES gabriel_corpus.db")
        print("="*50)
        tables = [
            ("spheres",          "Sphères (Ensemble + 1/ms + 1/t + 1/x)"),
            ("cercles",          "Cercles concentriques"),
            ("entites_hol",      "Entités HOL (defs, lemmes, théorèmes)"),
            ("qr_techniques",    "Q&R techniques"),
            ("liens_qr_entite",  "Liens Q&R ↔ entités HOL"),
            ("liens_hol",        "Liens inter-entités HOL"),
            ("fichiers_depot",   "Fichiers du dépôt Gabriel"),
            ("liens_fichiers",   "Liens inter-fichiers"),
            ("index_mots_cles",  "Mots-clés indexés"),
            ("sessions",         "Sessions de requêtes"),
        ]
        for table, label in tables:
            try:
                n = self.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                print(f"  {label:45s} : {n:5d}")
            except Exception:
                pass
        print("="*50 + "\n")

    def historique_sessions(self, n: int = 5):
        """Affiche les dernières sessions de requêtes."""
        rows = self.conn.execute(
            "SELECT question_brute, spheres_activees, score_confiance, timestamp "
            "FROM sessions ORDER BY timestamp DESC LIMIT ?", (n,)
        ).fetchall()
        if not rows:
            print("  (aucune session enregistrée)")
            return
        print(f"\n  Dernières {len(rows)} sessions :")
        for r in rows:
            print(f"  [{r['timestamp'][:16]}] [{r['score_confiance']:.2f}] "
                  f"{r['question_brute'][:60]}...")


# ─────────────────────────────────────────────────────────────────────────────
#  POINT D'ENTRÉE
# ─────────────────────────────────────────────────────────────────────────────

QUESTIONS_DEMO = [
    "Que démontre le théorème pont_spectral_direct_final dans la section XIII ?",
    "Comment RsP_un_demi_general prouve que le rapport spectral est toujours 1/2 ?",
    "Quelle est la relation entre la quadrature d'Archimède et les zéros critiques ?",
    "Explique l'axiome spectral_postulate_pos et son rôle dans prime_equation.",
    "Comment le locale ensemble_savard relie-t-il les sphères 1/ms, 1/t et 1/x ?",
]

def main():
    parser = argparse.ArgumentParser(
        description="Gabriel Archiviste — Orchestrateur de recherche cognitive HOL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples :
  python gabriel_p3_archiviste.py
  python gabriel_p3_archiviste.py --question "Que démontre RsP_un_demi_general ?"
  python gabriel_p3_archiviste.py --interactif
  python gabriel_p3_archiviste.py --stats
  python gabriel_p3_archiviste.py --historique
        """
    )
    parser.add_argument("--question",   "-q", type=str, default=None,
                        help="Question à traiter (mode direct)")
    parser.add_argument("--interactif", "-i", action="store_true",
                        help="Mode interactif (boucle de questions)")
    parser.add_argument("--stats",      "-s", action="store_true",
                        help="Afficher les statistiques de la DB")
    parser.add_argument("--historique", "-H", action="store_true",
                        help="Afficher l'historique des sessions")
    parser.add_argument("--top",        "-k", type=int, default=5,
                        help="Nombre de Q&R à retourner (défaut : 5)")
    parser.add_argument("--silencieux", action="store_true",
                        help="Affichage réduit")
    args = parser.parse_args()

    print("\n" + "="*70)
    print("  GABRIEL P3 — ARCHIVISTE ORCHESTRATEUR")
    print("  Pipeline cognitif — Corpus Spectral HOL")
    print("  Ensemble = 1  ↔  1/x + 1/t + 1/ms  (Pont Savard XIII)")
    print("="*70)

    archiviste = ArchivisteGabriel()
    archiviste.connecter()
    print(f"  ✓ Connexion DB : {DB_PATH}")

    if args.stats:
        archiviste.stats_db()

    if args.historique:
        archiviste.historique_sessions()

    if args.question:
        # Mode direct
        res = archiviste.rechercher(args.question, top_k=args.top)
        archiviste.afficher_resultat(res, verbeux=not args.silencieux)

    elif args.interactif:
        # Mode interactif
        print("\n  Mode interactif — tapez 'quitter' pour sortir\n")
        while True:
            try:
                question = input("  Votre question : ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n  Au revoir !")
                break
            if not question:
                continue
            if question.lower() in ("quitter", "exit", "quit", "q"):
                print("  Au revoir !")
                break
            res = archiviste.rechercher(question, top_k=args.top)
            archiviste.afficher_resultat(res, verbeux=not args.silencieux)

    else:
        # Mode démo : 5 questions prédéfinies
        print("\n  Mode démo — 5 questions du corpus spectral\n")
        for i, q in enumerate(QUESTIONS_DEMO, 1):
            print(f"\n  ── Question {i}/{len(QUESTIONS_DEMO)} ──")
            res = archiviste.rechercher(q, top_k=args.top)
            archiviste.afficher_resultat(res, verbeux=not args.silencieux)
            if i < len(QUESTIONS_DEMO):
                input("  [Entrée pour continuer...]\n")

    if args.stats or args.historique:
        pass
    else:
        archiviste.stats_db()

    archiviste.fermer()
    print("  Pipeline cognitif Gabriel — Archiviste terminé ✓\n")


if __name__ == "__main__":
    main()

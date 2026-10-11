"""Orchestrateur de debat contradictoire Gabriel vs Critique Virtuel.

Lance un echange dialectique en N tours sur un theme spectral, entre :
  - Gabriel (defenseur de la Methode Spectrale Savard, system prompt enrichi)
  - Un Critique Virtuel choisi parmi 5 personas mathematiciens classiques.

Particularites de cette version :
  * 5 PERSONAS de critique (analytique, logicien, sceptique epistemo, geometre
    algebrique, computationnaliste), avec mode 'rotation' qui les fait tourner
    a chaque tour pour maximiser la richesse de la contre-argumentation.
  * ALTERNANCE Claude <-> OpenAI a chaque appel LLM (Ollama est ecarte du debat,
    car retire de la chaine multiloop en prod).
  * Sauvegarde DUALE : JSON signe + Markdown citable pretes pour publication.
  * Nom de fichier CHRONOLOGIQUE + CONTEXTUEL : YYYY-MM-DD_HHhMMmSSs_<slug>_<id>.md
  * Dossier de sortie configurable via la variable d'env DEBAT_OUTPUT_DIR
    (defaut: data/debats/). Sur Docker, peut pointer vers /home/agent/app/data/
    debats-onedrive qui est monte depuis HOST_DEBAT_DIR (OneDrive Windows).

Sortie : objet DebatResult contenant tous les tours + synthese citable.
"""
from __future__ import annotations

import asyncio
import datetime as dt
import json
import logging
import os
import re
import unicodedata
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from ..core.llm_manager import LLMManager
from ..spectral.spectral_knowledge import build_grounded_system_prompt

logger = logging.getLogger(__name__)


# =============================================================================
# Slugification du theme pour nommage de fichier
# =============================================================================
_SLUG_MAX_CHARS = 60


def _slugify_theme(theme: str, max_chars: int = _SLUG_MAX_CHARS) -> str:
    """Convertit un theme en slug ASCII safe pour nom de fichier.

    Etapes :
      1. Decomposition Unicode + suppression des accents (NFD)
      2. Minuscules
      3. Caracteres non alphanumeriques -> tiret
      4. Tirets multiples -> un seul
      5. Tronque a max_chars (par defaut 60) sans couper un mot
      6. Si vide apres nettoyage, retourne 'debat'

    Exemples :
      "Le rapport 1/k est-il une coincidence ?" -> "le-rapport-1-k-est-il-une-coincidence"
      "Préuve Isabelle close ?"                 -> "preuve-isabelle-close"
    """
    if not theme:
        return "debat"
    # Decomposition NFD : 'é' -> 'e' + accent
    decomposed = unicodedata.normalize("NFD", theme)
    ascii_only = decomposed.encode("ascii", "ignore").decode("ascii")
    # Tout en minuscules
    lower = ascii_only.lower()
    # Remplacer non-alphanumerique par tiret
    slugged = re.sub(r"[^a-z0-9]+", "-", lower)
    # Compresser les tirets multiples + supprimer les tirets de bord
    slugged = re.sub(r"-+", "-", slugged).strip("-")
    if not slugged:
        return "debat"
    if len(slugged) <= max_chars:
        return slugged
    # Tronquer sans couper un mot : couper au dernier tiret avant max_chars
    truncated = slugged[:max_chars]
    last_dash = truncated.rfind("-")
    if last_dash > max_chars // 2:
        truncated = truncated[:last_dash]
    return truncated.rstrip("-") or "debat"


def _default_output_dir() -> Path:
    """Determine le dossier de sortie par defaut.

    Priorite :
      1. Variable d'env DEBAT_OUTPUT_DIR (path absolu ou relatif)
      2. data/debats/ (fallback historique pour les tests et le mode local)
    """
    env_path = os.environ.get("DEBAT_OUTPUT_DIR", "").strip()
    if env_path:
        return Path(env_path)
    return Path("data/debats")



# =============================================================================
# Personas de Critiques Virtuels (5 personas etendus)
# =============================================================================
PERSONAS: dict[str, dict[str, str]] = {
    "analytique": {
        "nom": "Theoricien Analytique des Nombres",
        "specialite": "fonction zeta, repartition des premiers, theoreme PNT",
        "system": (
            "Tu es un THEORICIEN ANALYTIQUE DES NOMBRES, dans la lignee de Hadamard, "
            "de la Vallee-Poussin, Selberg, Montgomery, Tao. Tu joues l'avocat du "
            "diable face a Gabriel (defenseure de la Methode Spectrale Savard).\n\n"
            "Tu maitrises :\n"
            "  - La fonction zeta de Riemann et son prolongement meromorphe\n"
            "  - Le theoreme des nombres premiers (PNT) et ses formes effectives\n"
            "  - La formule explicite de von Mangoldt\n"
            "  - Les estimees de zeros par Korobov-Vinogradov\n"
            "  - Les correlations de paires d'Odlyzko et Montgomery\n\n"
            "Tes objections doivent :\n"
            "  - Tester si le 'rapport spectral 1/k' n'est qu'une consequence du PNT\n"
            "  - Demander des estimees ASYMPTOTIQUES (O(...), o(...)) precises\n"
            "  - Confronter avec les zones zerolibres connues\n"
            "  - Citer Hadamard 1896, von Mangoldt 1895, Montgomery 1973, Odlyzko 1989\n\n"
            "Style : courtois, technique, 4 phrases maxi par tour. Toujours UNE "
            "reference classique citee. Jamais 'c'est faux' ; prefere 'comment "
            "reconciliez-vous cela avec...?', 'n'est-ce pas une consequence "
            "asymptotique de...?'."
        ),
    },
    "logicien": {
        "nom": "Logicien Formel",
        "specialite": "Isabelle/HOL, theorie des modeles, fondements",
        "system": (
            "Tu es un LOGICIEN FORMEL, expert en Isabelle/HOL, Coq, Lean, theorie "
            "des modeles (Tarski, Goedel) et fondements des mathematiques. Tu joues "
            "l'avocat du diable face a Gabriel.\n\n"
            "Tes objections doivent :\n"
            "  - Distinguer impitoyablement DEFINITION, AXIOME, LEMME, THEOREME\n"
            "  - Reperer les axiomatisations AD-HOC ou les definitions circulaires\n"
            "  - Verifier si les preuves Isabelle/HOL invoquees sont vraiment "
            "    closes (et pas seulement 'sorry')\n"
            "  - Demander la PROVENANCE exacte de chaque enonce (.thy + section)\n"
            "  - Citer Gentzen, Goedel 1931, Tarski, Curry-Howard, Wiedijk\n\n"
            "Style : tres precis, presque pedant. Pose UNE question logique "
            "ciblee par tour (4 phrases maxi). Toujours cite UN logicien ou UN "
            "theoreme de fondement par objection."
        ),
    },
    "sceptique": {
        "nom": "Sceptique Epistemologue",
        "specialite": "philosophie des sciences, falsifiabilite, methode",
        "system": (
            "Tu es un SCEPTIQUE EPISTEMOLOGUE, dans l'esprit de Popper, Lakatos, "
            "Kuhn, et plus proche en mathematiques de Lakatos (Proofs and Refutations). "
            "Tu joues l'avocat du diable face a Gabriel.\n\n"
            "Tes objections doivent :\n"
            "  - Tester la FALSIFIABILITE : quelle observation refuterait la theorie ?\n"
            "  - Reperer les hypotheses AD-HOC, les redefinitions silencieuses,\n"
            "    les sauvetages par exception\n"
            "  - Distinguer 'PROGRAMME DE RECHERCHE' (Lakatos) vs 'theoreme prouve'\n"
            "  - Questionner le statut epistemique : conjecture ? heuristique ? "
            "    theoreme ? metaphore ?\n"
            "  - Citer Popper (Logique de la decouverte 1934), Lakatos (1976), "
            "    Kuhn (1962), Polya (1954)\n\n"
            "Style : philosophe, courtois, 4 phrases maxi. Demande TOUJOURS un "
            "critere de refutation concret. Cite UN philosophe ou methodologue par "
            "objection."
        ),
    },
    "geometre": {
        "nom": "Geometre Algebrique",
        "specialite": "geometrie arithmetique, schemas, conjectures de Weil",
        "system": (
            "Tu es un GEOMETRE ALGEBRIQUE, dans la lignee de Grothendieck, Deligne, "
            "Serre, Faltings. Tu joues l'avocat du diable face a Gabriel.\n\n"
            "Tes objections doivent :\n"
            "  - Confronter la 'geometrie spectrale Savard' a la geometrie "
            "    arithmetique CLASSIQUE (schemas, motifs, cohomologie etale)\n"
            "  - Questionner la STRUCTURE : qu'est-ce qu'un 'spectre' au sens "
            "    Spec(Z), Spec(F_p), versus 'spectre de Savard' ?\n"
            "  - Examiner si le 'rapport 1/k' peut s'interpreter via une "
            "    cohomologie ou une fonction L (conjectures de Weil, Birch &\n"
            "    Swinnerton-Dyer)\n"
            "  - Citer Grothendieck (EGA, SGA), Deligne (Weil II 1980), Serre, Faltings\n\n"
            "Style : structurel, abstrait, courtois. 4 phrases maxi. Cite UN "
            "geometre algebriste majeur par objection."
        ),
    },
    "computationnaliste": {
        "nom": "Computationnaliste",
        "specialite": "calcul exact, complexite, statistique numerique",
        "system": (
            "Tu es un COMPUTATIONNALISTE, expert en calcul exact (Sage, PARI/GP, "
            "Mathematica), en statistique numerique de la fonction zeta (Odlyzko, "
            "Gourdon) et en analyse de complexite. Tu joues l'avocat du diable.\n\n"
            "Tes objections doivent :\n"
            "  - Demander des VERIFICATIONS NUMERIQUES a grande echelle "
            "    (10^6, 10^9 premiers, pas seulement 1000)\n"
            "  - Tester si le 'rapport 1/k' tient pour des premiers gigantesques "
            "    ou s'effrite asymptotiquement\n"
            "  - Reperer les biais d'echantillonnage et les coincidences "
            "    statistiques (loi de Benford, loi de Cramer)\n"
            "  - Comparer avec les bases de donnees publiques : OEIS, LMFDB, "
            "    Odlyzko zeros, Sloane primes\n"
            "  - Citer Odlyzko, Gourdon-Sebah, Lehmer, OEIS-Sloane, LMFDB\n\n"
            "Style : pragmatique, numerique, courtois. 4 phrases maxi. Cite UNE "
            "base de donnees ou un calcul connu par objection."
        ),
    },
}

ORDRE_ROTATION: tuple[str, ...] = (
    "analytique",
    "logicien",
    "sceptique",
    "geometre",
    "computationnaliste",
)


# =============================================================================
# Modeles de donnees
# =============================================================================
@dataclass
class DebatTour:
    """Un tour de debat (intervention de Gabriel OU du Critique)."""
    numero: int
    role: str             # "gabriel" ou "critique"
    persona: str | None   # nom de la persona si role == "critique"
    provider: str         # "claude" ou "openai"
    texte: str
    timestamp: str = field(default_factory=lambda: dt.datetime.now().isoformat())


@dataclass
class DebatResult:
    """Resultat complet d'un debat contradictoire."""
    debat_id: str
    theme: str
    date: str
    persona_mode: str
    tours: list[DebatTour]
    synthese_citable: str
    duree_secondes: float
    json_path: str | None = None
    markdown_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["tours"] = [asdict(t) for t in self.tours]
        return d


# =============================================================================
# Orchestrateur
# =============================================================================
class DebatOrchestrator:
    """Orchestre un debat dialectique entre Gabriel et un Critique virtuel.

    Architecture :
      * Provider : alternance Claude / OpenAI (Ollama ecarte du debat).
      * Personas : 5 choix + 'rotation' (chaque tour critique = persona suivante).
      * Sortie  : data/debats/<date>_<id>.json + <date>_<id>.md
    """

    NB_TOURS_DEFAUT = 3   # 3 tours = Gabriel(these) + 2x(Critique + Gabriel)
    PERSONAS = PERSONAS    # expose pour les tests / UI

    def __init__(
        self,
        llm: LLMManager,
        audits_dir: Path | str | None = None,
    ):
        self.llm = llm
        # Si audits_dir est explicitement passe (tests), on l'utilise.
        # Sinon, on lit DEBAT_OUTPUT_DIR via _default_output_dir().
        if audits_dir is None:
            self.audits_dir = _default_output_dir()
        else:
            self.audits_dir = Path(audits_dir)
        self.audits_dir.mkdir(parents=True, exist_ok=True)
        self.gabriel_system = build_grounded_system_prompt()
        # Provider counter : 0=Claude, 1=OpenAI, repete
        self._provider_counter = 0

    # ------------------------------------------------------------------
    # API publique
    # ------------------------------------------------------------------
    async def run(
        self,
        theme: str,
        nb_tours: int = NB_TOURS_DEFAUT,
        persona: str = "rotation",
    ) -> DebatResult:
        """Execute un debat complet sur le theme donne.

        Args:
            theme    : Le sujet du debat.
            nb_tours : Nombre de paires (Critique+Gabriel) apres la these initiale.
                       Total messages = 1 + 2*(nb_tours-1) + 1 these = 2*nb_tours - 1.
                       Defaut 3 => 5 messages : G, C, G, C, G.
            persona  : 'rotation' (defaut) | 'analytique' | 'logicien' |
                       'sceptique' | 'geometre' | 'computationnaliste'.

        Returns:
            DebatResult avec tours, synthese, et chemins JSON+Markdown.
        """
        if persona != "rotation" and persona not in PERSONAS:
            raise ValueError(
                f"Persona inconnue : '{persona}'. "
                f"Valeurs valides : 'rotation' ou {list(PERSONAS.keys())}"
            )
        if nb_tours < 1:
            raise ValueError(f"nb_tours doit etre >= 1, recu {nb_tours}")

        debat_id = str(uuid.uuid4())[:8]
        t0 = dt.datetime.now()
        # Reset du compteur d'alternance : chaque debat commence par Claude
        # (la these initiale de Gabriel est toujours sur Claude).
        self._provider_counter = 0
        logger.info(
            "Debat %s sur theme=%r persona=%s nb_tours=%d",
            debat_id, theme[:60], persona, nb_tours,
        )

        tours: list[DebatTour] = []
        historique: list[str] = []

        # ---------- Tour 1 : Gabriel pose sa these ------------------------
        these, prov = await self._invoque_gabriel_these(theme)
        tours.append(DebatTour(
            numero=1, role="gabriel", persona=None,
            provider=prov, texte=these,
        ))
        historique.append(f"GABRIEL (these initiale) :\n{these}")

        # ---------- Tours suivants : Critique -> Gabriel ------------------
        for round_idx in range(1, nb_tours):
            persona_courante = self._select_persona(persona, round_idx)

            # Critique objecte
            objection, prov_c = await self._invoque_critique(
                theme, historique, persona_courante,
            )
            tours.append(DebatTour(
                numero=len(tours) + 1, role="critique",
                persona=persona_courante, provider=prov_c, texte=objection,
            ))
            historique.append(
                f"CRITIQUE ({PERSONAS[persona_courante]['nom']}) :\n{objection}"
            )

            # Gabriel defend
            defense, prov_g = await self._invoque_gabriel_defense(theme, historique)
            tours.append(DebatTour(
                numero=len(tours) + 1, role="gabriel", persona=None,
                provider=prov_g, texte=defense,
            ))
            historique.append(f"GABRIEL (defense {round_idx}) :\n{defense}")

        # ---------- Synthese citable finale -------------------------------
        synthese, _ = await self._invoque_synthese_citable(theme, historique)

        duree = (dt.datetime.now() - t0).total_seconds()
        result = DebatResult(
            debat_id=debat_id,
            theme=theme,
            date=t0.isoformat(),
            persona_mode=persona,
            tours=tours,
            synthese_citable=synthese,
            duree_secondes=duree,
        )
        json_path = self._save_json(result)
        md_path = self._save_markdown(result)
        result.json_path = str(json_path)
        result.markdown_path = str(md_path)
        logger.info(
            "Debat %s termine en %.1fs (%d tours, persona=%s)",
            debat_id, duree, len(tours), persona,
        )
        return result

    # ------------------------------------------------------------------
    # Selection persona + provider
    # ------------------------------------------------------------------
    def _select_persona(self, persona_mode: str, round_idx: int) -> str:
        """Si rotation, cycle sur ORDRE_ROTATION ; sinon retourne le fixe."""
        if persona_mode == "rotation":
            return ORDRE_ROTATION[(round_idx - 1) % len(ORDRE_ROTATION)]
        return persona_mode

    async def _call_llm(
        self,
        prompt: str,
        system: str,
        temperature: float,
    ) -> tuple[str, str]:
        """Alternance Claude / OpenAI (Ollama exclu du debat).

        Retourne (texte, provider_utilise). Si le primaire echoue,
        bascule sur l'autre. Si les deux echouent : message d'erreur.
        """
        order: list[tuple[str, Any]]
        if self._provider_counter % 2 == 0:
            order = [("claude", self.llm.claude), ("openai", self.llm.openai)]
        else:
            order = [("openai", self.llm.openai), ("claude", self.llm.claude)]
        self._provider_counter += 1

        for name, client in order:
            if not client.is_available():
                logger.debug("debat : %s indisponible, skip", name)
                continue
            try:
                txt = await client.generate(
                    prompt, system=system, temperature=temperature,
                )
            except Exception as exc:
                logger.warning("debat : %s a leve %s", name, exc)
                txt = None
            if txt and txt.strip():
                return txt.strip(), name
            logger.warning("debat : %s reponse vide, fallback", name)

        logger.error("debat : aucun LLM disponible (Claude+OpenAI down)")
        return (
            "[ERREUR DEBAT] Aucun LLM disponible (Claude+OpenAI hors-ligne ou cles "
            "API manquantes). Verifie .env (CLAUDE_API_KEY, OPENAI_API_KEY).",
            "none",
        )

    # ------------------------------------------------------------------
    # Invocations LLM specialisees
    # ------------------------------------------------------------------
    async def _invoque_gabriel_these(self, theme: str) -> tuple[str, str]:
        prompt = (
            f"Voici le theme du debat contradictoire : \"{theme}\"\n\n"
            "Pose ta these initiale en 4-6 phrases, en t'appuyant sur la Methode "
            "Spectrale de Philippe Thomas Savard et le lexique technique. Sois "
            "precise, marque ce qui est PROUVE (Isabelle/HOL) versus ce qui est "
            "CONJECTURE. Mentionne au moins UN exemple numerique concret. "
            "Termine par une formulation forte de ta position."
        )
        return await self._call_llm(prompt, self.gabriel_system, temperature=0.4)

    async def _invoque_critique(
        self,
        theme: str,
        historique: list[str],
        persona_key: str,
    ) -> tuple[str, str]:
        persona = PERSONAS[persona_key]
        hist_str = "\n\n".join(historique[-3:])
        prompt = (
            f"Theme du debat : \"{theme}\"\n\n"
            f"Historique recent :\n{hist_str}\n\n"
            f"En tant que {persona['nom']} (specialite : {persona['specialite']}), "
            "formule une OBJECTION rigoureuse et courtoise (4 phrases maxi). "
            "Cite au moins UNE reference classique relevant de TA specialite. "
            "Ne sois pas redondant : creuse un NOUVEAU point faible (zone grise, "
            "hypothese implicite, manque de preuve)."
        )
        return await self._call_llm(prompt, persona["system"], temperature=0.5)

    async def _invoque_gabriel_defense(
        self,
        theme: str,
        historique: list[str],
    ) -> tuple[str, str]:
        hist_str = "\n\n".join(historique[-3:])
        prompt = (
            f"Theme du debat : \"{theme}\"\n\n"
            f"Historique recent :\n{hist_str}\n\n"
            "Reponds a l'objection precedente du Critique Virtuel en 4-6 phrases. "
            "Sois PRECISE : si tu as une preuve formelle (Isabelle/HOL), cite-la. "
            "Si tu n'as qu'une conjecture, dis-le franchement. Reconnais ce qui "
            "est legitime dans l'objection. Termine en proposant une experience "
            "numerique ou un lemme qui pourrait trancher."
        )
        return await self._call_llm(prompt, self.gabriel_system, temperature=0.4)

    async def _invoque_synthese_citable(
        self,
        theme: str,
        historique: list[str],
    ) -> tuple[str, str]:
        hist_str = "\n\n".join(historique)
        prompt = (
            f"Theme du debat : \"{theme}\"\n\n"
            f"DEBAT COMPLET :\n{hist_str}\n\n"
            "Redige une SYNTHESE CITABLE de ce debat en 3 paragraphes pour une "
            "publication academique :\n"
            "  1. Position spectrale (Savard) : these et arguments retenus\n"
            "  2. Critiques classiques adressees : objections + reponses\n"
            "  3. Question ouverte / prochaine etape de recherche\n"
            "Style academique, neutre, citations explicites des positions."
        )
        return await self._call_llm(prompt, self.gabriel_system, temperature=0.3)

    # ------------------------------------------------------------------
    # Sauvegardes (JSON + Markdown) avec nommage chronologique + contextuel
    # ------------------------------------------------------------------
    def _build_filename_stem(self, result: DebatResult) -> str:
        r"""Construit le radical du fichier : <YYYY-MM-DD>_<HHhMMmSSs>_<slug>_<id>.

        Garantit :
          - Tri chronologique naturel (date+heure en prefixe)
          - Contexte lisible (slug du theme)
          - Unicite (id 8 chars uuid en suffixe)
          - Compatible Windows (pas de : ? * < > | / \ " dans le nom)
        """
        # Parse la date ISO du resultat
        try:
            ts = dt.datetime.fromisoformat(result.date)
        except ValueError:
            ts = dt.datetime.now()
        date_part = ts.strftime("%Y-%m-%d")
        time_part = ts.strftime("%Hh%Mm%Ss")
        slug = _slugify_theme(result.theme)
        return f"{date_part}_{time_part}_{slug}_{result.debat_id}"

    def _save_json(self, result: DebatResult) -> Path:
        stem = self._build_filename_stem(result)
        path = self.audits_dir / f"{stem}.json"
        path.write_text(
            json.dumps(result.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return path

    def _save_markdown(self, result: DebatResult) -> Path:
        stem = self._build_filename_stem(result)
        path = self.audits_dir / f"{stem}.md"
        lines: list[str] = []
        lines.append("# Debat contradictoire — Gabriel vs Critique Virtuel")
        lines.append("")
        lines.append(f"**ID** : `{result.debat_id}`  ")
        lines.append(f"**Date** : {result.date}  ")
        lines.append(f"**Theme** : {result.theme}  ")
        lines.append(f"**Mode persona** : `{result.persona_mode}`  ")
        lines.append(f"**Duree** : {result.duree_secondes:.1f} s  ")
        lines.append(f"**Nombre de tours** : {len(result.tours)}")
        lines.append("")
        lines.append("---")
        lines.append("")
        for tour in result.tours:
            if tour.role == "gabriel":
                titre = f"## Tour {tour.numero} — Gabriel  *(via {tour.provider})*"
            else:
                p = PERSONAS.get(tour.persona or "", {})
                nom = p.get("nom", tour.persona or "Critique")
                spec = p.get("specialite", "")
                titre = (
                    f"## Tour {tour.numero} — Critique : *{nom}*  "
                    f"*(via {tour.provider})*"
                )
                if spec:
                    titre += f"\n\n*Specialite : {spec}*"
            lines.append(titre)
            lines.append("")
            lines.append(tour.texte)
            lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Synthese citable")
        lines.append("")
        lines.append(result.synthese_citable)
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append(
            f"*Genere par Gabriel (Multi-Loop Math Agent) — "
            f"alternance Claude/OpenAI, personas {', '.join(ORDRE_ROTATION)}.*"
        )
        path.write_text("\n".join(lines), encoding="utf-8")
        return path

    # ------------------------------------------------------------------
    # Utilitaires expose pour la CLI / tests
    # ------------------------------------------------------------------
    @staticmethod
    def list_personas() -> list[dict[str, str]]:
        """Retourne la liste des personas (pour affichage CLI)."""
        return [
            {"cle": k, "nom": v["nom"], "specialite": v["specialite"]}
            for k, v in PERSONAS.items()
        ]

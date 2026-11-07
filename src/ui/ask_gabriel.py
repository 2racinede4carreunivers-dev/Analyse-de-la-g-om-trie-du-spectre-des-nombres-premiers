"""Module 'Ask Gabriel' : 3 commandes d'aide contextuelle sur l'agent.

Trois commandes accessibles dans la CLI Gabriel :
  - `ask`        -> Principales commandes pour interagir avec Gabriel
  - `ask type`   -> Principales fonctions et caracteristiques + usage
  - `ask rules`  -> Guide sur comment interagir efficacement avec Gabriel

100% deterministe, lu depuis ce module (aucun appel LLM).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional


# --------------------------------------------------------------------------
# Contenu : 'ask' - Principales commandes pour interpeller Gabriel
# --------------------------------------------------------------------------
ASK_MAIN_SECTIONS = [
    {
        "title": "[bold cyan]COMMENT INTERPELLER GABRIEL[/bold cyan]",
        "lines": [
            "Vous pouvez interagir avec Gabriel de [bold]4 facons complementaires[/bold] :",
            "",
            "  [yellow]1. Commandes deterministes (recommandees pour les calculs)[/yellow]",
            "     - 100% reproductibles, citables, zero hallucination",
            "     - Exemples : [cyan]prime 26[/cyan], [cyan]gap -19 -5[/cyan], "
            "[cyan]modele reconstruct 42[/cyan]",
            "",
            "  [yellow]2. Auto-trigger en langage naturel (visualisations)[/yellow]",
            "     - Tapez une question contenant verbe + type math",
            "     - Exemple : [cyan]Trace la convergence du ratio SA/SB sur 1..100[/cyan]",
            "     - Gabriel detecte et genere ASCII + PNG sans LLM",
            "",
            "  [yellow]3. Questions libres (pipeline multi-loop avec LLM)[/yellow]",
            "     - Pour les explications, raisonnements ouverts",
            "     - Exemple : [cyan]Explique pourquoi le modele 1/4 converge plus vite[/cyan]",
            "     - Garde-fous : CertaintyKernel, Slow-Motion Debugger, Silent Audit",
            "",
            "  [yellow]4. Mode debugger pedagogique[/yellow]",
            "     - Decompose la question pas-a-pas, bypass LLM possible",
            "     - Exemple : [cyan]debug \"Reconstruis le 42eme premier\"[/cyan]",
        ],
    },
    {
        "title": "[bold cyan]COMMANDES PRINCIPALES PAR CATEGORIE[/bold cyan]",
        "lines": [
            "  [yellow]Aide & navigation[/yellow]",
            "    [cyan]aide[/cyan] / [cyan]commandes[/cyan]   Liste complete + raccourcis clavier",
            "    [cyan]ask[/cyan] / [cyan]ask type[/cyan] / [cyan]ask rules[/cyan]   Ce systeme d'aide contextuelle",
            "    [cyan]contexte[/cyan]              Contexte mathematique actuel",
            "    [cyan]memoire[/cyan]               Historique des echanges de la session",
            "",
            "  [yellow]Calculs mathematiques[/yellow]",
            "    [cyan]prime <N>[/cyan]             Le N-ieme nombre premier (table 1..1000)",
            "    [cyan]gap <v1> <v2>[/cyan]         Ecart spectral (cas +,+ / -,- / -,+)",
            "    [cyan]rsp <A> <B>[/cyan]           Rapport spectral direct",
            "    [cyan]modele <action>[/cyan]       Interroge les 3 modeles (1/2, 1/3, 1/4)",
            "",
            "  [yellow]Visualisations[/yellow]",
            "    [cyan]courbe <type> n1..n2[/cyan]  ASCII + tableau + PNG citable",
            "    [cyan]rsp-courbe <cfg> [k][/cyan]  Courbe RsP en ASCII",
            "",
            "  [yellow]Verification & preuves[/yellow]",
            "    [cyan]verifier <N>[/cyan]          Validation toolkit (sympy/mpmath/z3)",
            "    [cyan]valider <N>[/cyan]           Boucle Wolfram <-> Gabriel <-> Isabelle",
            "    [cyan]debug \"<q>\"[/cyan]           Mode debugger pedagogique",
            "",
            "  [yellow]Audit & citations[/yellow]",
            "    [cyan]historique[/cyan]            20 derniers audits",
            "    [cyan]audit <id>[/cyan]            Detail d'un audit",
            "    [cyan]citer <id> latex[/cyan]      Citation prete pour article LaTeX",
            "",
            "  [yellow]Tests & CI[/yellow]",
            "    [cyan]ci[/cyan]                    Lance pytest local (332 tests)",
            "",
            "  [yellow]Sortie[/yellow]",
            "    [cyan]quitter[/cyan] / Ctrl+D     Ferme Gabriel proprement",
        ],
    },
    {
        "title": "[bold cyan]POUR EN SAVOIR PLUS[/bold cyan]",
        "lines": [
            "  [cyan]ask type[/cyan]                  Description des fonctions et capacites de Gabriel",
            "  [cyan]ask rules[/cyan]                 Guide pour interagir efficacement",
            "  [cyan]commandes[/cyan]                 Liste exhaustive de TOUTES les commandes",
            "  [cyan]commande-gabriel/COMMANDES.md[/cyan]   Documentation complete (10 sections)",
        ],
    },
]


# --------------------------------------------------------------------------
# Contenu : 'ask type' - Fonctions et caracteristiques
# --------------------------------------------------------------------------
ASK_TYPE_SECTIONS = [
    {
        "title": "[bold cyan]COEUR MATHEMATIQUE - METHODE SPECTRALE[/bold cyan]",
        "lines": [
            "Gabriel implemente la [bold]Methode Spectrale[/bold] de Philippe Thomas Savard,",
            "selon [cyan]theories/methode_spectral.thy[/cyan] (verite officielle Isabelle/HOL).",
            "",
            "  [yellow]3 modeles spectraux disponibles[/yellow]",
            "    [bold]Modele 1/2[/bold]   A(n) = (13/8)·2^n - 2     factor = 64     ratio = 1/2",
            "    [bold]Modele 1/3[/bold]   A(n) = (73/108)·3^n - 3/2  factor = 729    ratio = 1/3",
            "    [bold]Modele 1/4[/bold]   A(n) = (241/192)·4^n - 4/3 factor = 4096   ratio = 1/4",
            "",
            "  [yellow]8 questions canoniques traitees[/yellow]",
            "    Q1.a   Rapport spectral 1x1",
            "    Q1.b   Rapport spectral n×n symetrique",
            "    Q1.c   Rapport spectral asymetrique chaotique",
            "    Q1.d   Rapport spectral asymetrique ordonnee",
            "    Q2     Reconstruction du N-ieme nombre premier",
            "    Q3.a   Calcul de gap (+,+)",
            "    Q3.b   Calcul de gap (-,-)",
            "    Q3.c   Calcul de gap (-,+)",
            "",
            "  [yellow]Comment utiliser[/yellow]",
            "    [cyan]modele list[/cyan]             Liste les 3 modeles",
            "    [cyan]modele questions[/cyan]        Liste les 8 questions",
            "    [cyan]modele all[/cyan]              Repond aux 8 questions sur les 3 modeles",
        ],
    },
    {
        "title": "[bold cyan]ARCHITECTURE COGNITIVE - 7 MOTEURS + MULTI-LOOP[/bold cyan]",
        "lines": [
            "  [yellow]7 moteurs cognitifs[/yellow] qui collaborent dans le pipeline :",
            "    1. [bold]Analyzer[/bold]             Decomposition de la question",
            "    2. [bold]Spectral[/bold]             Calculs exacts (Fraction infinie)",
            "    3. [bold]Geometrie[/bold]            GeometrieSpectraleEngine (3 modeles)",
            "    4. [bold]Gap Solver[/bold]           Resolution directe des ecarts",
            "    5. [bold]HOL/Isabelle[/bold]         Generation/validation de preuves",
            "    6. [bold]Critic[/bold]               Multi-loop self-critique",
            "    7. [bold]Verifier[/bold]             Toolkit sympy/mpmath/z3",
            "",
            "  [yellow]Garde-fous anti-hallucination[/yellow]",
            "    - [bold]CertaintyKernel[/bold]       Formules hardcodees (verite absolue)",
            "    - [bold]Slow-Motion Debugger[/bold]  Decomposition pas-a-pas si incoherence",
            "    - [bold]Silent Audit[/bold]          Re-prompt silencieux du LLM",
            "    - [bold]Verification croisee[/bold]  Wolfram ↔ Gabriel ↔ Isabelle",
        ],
    },
    {
        "title": "[bold cyan]VISUALISATIONS - ASCII + TABLE + PNG[/bold cyan]",
        "lines": [
            "  [yellow]8 types de courbes calculables[/yellow] :",
            "    SA, SB, SA_SB, digamma, invariant, ratio, gap, prime",
            "",
            "  [yellow]3 formats de sortie combinables[/yellow] :",
            "    [bold]ASCII[/bold]   (toujours) - directement dans le terminal",
            "    [bold]Table[/bold]   ([cyan]--table[/cyan]) - valeurs exactes en Fraction",
            "    [bold]PNG[/bold]     ([cyan]--png[/cyan]) - 150 dpi, dossier data/graphs/, citable",
            "",
            "  [yellow]Auto-trigger en langage naturel[/yellow]",
            "    Gabriel detecte automatiquement les demandes de graphique :",
            "      \"Trace la convergence du ratio SA/SB sur 1..100\"",
            "      \"Comment evolue digamma entre 1 et 50 ?\"",
            "      \"Visualise SA et SB pour les 30 premiers en PNG\"",
            "",
            "  [yellow]Commande explicite[/yellow]",
            "    [cyan]courbe <type> <n1>..<n2> [--table] [--png] [--scale=auto|log10|linear][/cyan]",
        ],
    },
    {
        "title": "[bold cyan]AUDIT JSON SIGNE - CITATION SCIENTIFIQUE[/bold cyan]",
        "lines": [
            "Chaque calcul important produit un [bold]audit JSON signe SHA-256[/bold] dans",
            "[cyan]data/audits/[/cyan] qui peut etre cite dans vos articles.",
            "",
            "  [yellow]Acceder a vos audits[/yellow]",
            "    [cyan]historique[/cyan]              20 derniers audits",
            "    [cyan]audit <id>[/cyan]              JSON complet d'un audit",
            "    [cyan]citer <id> markdown[/cyan]     Citation Markdown",
            "    [cyan]citer <id> latex[/cyan]        Citation LaTeX (\\bibitem)",
            "    [cyan]citer <id> text[/cyan]         Citation texte brut",
            "",
            "  [yellow]Contenu d'un audit[/yellow]",
            "    - intervention_type (gap, modele_spectral, courbe, ...)",
            "    - question originale + reponse certifiee",
            "    - citations Isabelle/HOL (.thy references)",
            "    - rapports toolkit (sympy, mpmath, z3)",
            "    - hash SHA-256 verifiable",
        ],
    },
    {
        "title": "[bold cyan]INTEGRATIONS HOL/LEAN[/bold cyan]",
        "lines": [
            "  [yellow]Theories chargees au demarrage[/yellow]",
            "    - methode_spectral.thy",
            "    - geometrie_spectre_premier.thy",
            "    - riemann_spectral.thy",
            "    - RiemannSpectral.lean",
            "",
            "  [yellow]Capacites[/yellow]",
            "    - Lecture du corpus  ([cyan]corpus[/cyan], [cyan]corpus detail[/cyan])",
            "    - Generation de scripts de verification Isabelle/HOL",
            "    - Validation formelle ([cyan]valider <N>[/cyan])",
            "    - Bridge HOL4/Lean4 (en cours)",
        ],
    },
]


# --------------------------------------------------------------------------
# Contenu : 'ask rules' - Guide d'interaction
# --------------------------------------------------------------------------
ASK_RULES_SECTIONS = [
    {
        "title": "[bold cyan]LES 10 REGLES D'OR POUR INTERAGIR AVEC GABRIEL[/bold cyan]",
        "lines": [
            "",
            "  [yellow]1. PRIVILEGIEZ LES COMMANDES DETERMINISTES POUR LES CALCULS[/yellow]",
            "     - [cyan]prime 26[/cyan]  > 'Quel est le 26eme nombre premier ?'",
            "     - [cyan]gap 26 56[/cyan] > 'Calcule l ecart entre les positions 26 et 56'",
            "     - Pourquoi ? Zero appel LLM, zero hallucination, reproductible.",
            "",
            "  [yellow]2. SOYEZ PRECIS SUR LES BORNES[/yellow]",
            "     - BON  : 'Trace SA sur n=1..50'",
            "     - MAL  : 'Trace SA pour quelques valeurs'",
            "     - L'auto-trigger reconnait : 'n=1..50', 'de 1 a 100', 'entre 5 et 25',",
            "       '[1,200]', 'les 100 premiers'.",
            "",
            "  [yellow]3. INDIQUEZ LE MODELE SOUHAITE QUAND PERTINENT[/yellow]",
            "     - Par defaut, Gabriel utilise le modele 1/2",
            "     - Pour comparer : [cyan]modele all[/cyan] ou [cyan]modele reconstruct 26[/cyan]",
            "     - Les 3 modeles (1/2, 1/3, 1/4) reconstruisent le MEME premier",
            "",
            "  [yellow]4. DEMANDEZ UN PNG POUR LES ARTICLES SCIENTIFIQUES[/yellow]",
            "     - Mots-cles : 'article scientifique', 'exporte', 'PDF', 'citable'",
            "     - Ou explicitement : ajoutez [cyan]--png[/cyan] a [cyan]courbe[/cyan]",
            "",
            "  [yellow]5. CITEZ AVEC L'ID D'AUDIT[/yellow]",
            "     - Apres chaque calcul, Gabriel affiche : [cyan]Audit cree : id=XXXXX[/cyan]",
            "     - Notez l'ID -> [cyan]citer XXXXX latex[/cyan] pour l'article",
            "",
            "  [yellow]6. EN CAS DE DOUTE, DECOMPOSEZ[/yellow]",
            "     - Mode debugger : [cyan]debug \"votre question\"[/cyan]",
            "     - Gabriel decompose etape par etape, propose le bypass LLM",
            "",
            "  [yellow]7. UTILISEZ LE LANGAGE NATUREL POUR LES EXPLICATIONS[/yellow]",
            "     - Bon pour : 'Explique pourquoi le ratio converge vers 1/2'",
            "     - Pas pour : 'Calcule 2+2' (utilisez plutot une commande directe)",
            "",
            "  [yellow]8. VERIFIEZ AVEC PYTEST AVANT DE PUBLIER[/yellow]",
            "     - [cyan]ci[/cyan] dans Gabriel -> 332 tests verifient l'integrite",
            "     - Si echec : examiner le rapport, corriger, relancer",
            "",
            "  [yellow]9. NE TOUCHEZ PAS AU CODE GABRIEL POUR CORRIGER UN TEST[/yellow]",
            "     - Si un test echoue : [bold]le code suit methode_spectral.thy[/bold]",
            "     - Si la valeur attendue diverge de .thy, c'est LE TEST qui est faux",
            "     - .thy = verite officielle absolue",
            "",
            "  [yellow]10. EXPLOITEZ LES RACCOURCIS CLAVIER[/yellow]",
            "     - [bold]Fleche Haut/Bas[/bold]  Navigue dans l'historique",
            "     - [bold]Tab[/bold]              Auto-completion des commandes",
            "     - [bold]Ctrl+R[/bold]           Recherche dans l'historique",
            "     - [bold]Ctrl+L[/bold]           Efface l'ecran",
            "     - Historique persistant : [cyan]data/.gabriel_history[/cyan]",
        ],
    },
    {
        "title": "[bold cyan]CE QUE GABRIEL FAIT BIEN[/bold cyan]",
        "lines": [
            "  [green]✓[/green] Reconstruction exacte du N-ieme premier (N=1..1000)",
            "  [green]✓[/green] Calcul de rapports spectraux (3 modeles, 4 sous-cas chacun)",
            "  [green]✓[/green] Calcul d'ecarts (3 cas : +,+ / -,- / -,+)",
            "  [green]✓[/green] Visualisations citables (ASCII + Table + PNG 150 dpi)",
            "  [green]✓[/green] Audit JSON signe SHA-256 reproductible",
            "  [green]✓[/green] Detection automatique de demandes de graphique",
            "  [green]✓[/green] Slow-Motion Debugger pour decortiquer une question",
            "  [green]✓[/green] Verification toolkit (sympy/mpmath/z3) sans reseau",
            "  [green]✓[/green] Generation Isabelle/HOL pour vos preuves",
        ],
    },
    {
        "title": "[bold cyan]LIMITES ACTUELLES DE GABRIEL[/bold cyan]",
        "lines": [
            "  [red]×[/red] Table de primes limitee a 1000 (extension possible si besoin)",
            "  [red]×[/red] Plan trifocal FZg/HyRi/MsP non encore implemente",
            "  [red]×[/red] Compilation Isabelle requiert le profil Docker -WithIsabelle",
            "  [red]×[/red] Bridge Lean4 ↔ Riemann en cours, pas encore complet",
            "  [red]×[/red] Le LLM peut halluciner sur des questions hors-domaine,",
            "      mais les garde-fous (CertaintyKernel) bloquent les erreurs critiques",
        ],
    },
    {
        "title": "[bold cyan]EN CAS DE PROBLEME[/bold cyan]",
        "lines": [
            "  1. [yellow]Reponse incoherente ou incertaine[/yellow]",
            "     -> Relancez avec [cyan]debug \"votre question\"[/cyan]",
            "        Le Slow-Motion Debugger force le bypass LLM si necessaire.",
            "",
            "  2. [yellow]Un test pytest echoue[/yellow]",
            "     -> Tapez [cyan]ci[/cyan] pour le rapport",
            "     -> Verifiez que les valeurs attendues correspondent a .thy",
            "     -> Ne modifiez PAS le code Gabriel ; corrigez le test",
            "",
            "  3. [yellow]Crash UnicodeEncodeError sur PowerShell[/yellow]",
            "     -> Caracteres surrogates Windows. Connu, fix en cours.",
            "",
            "  4. [yellow]Pas d acces aux 1000 primes ?[/yellow]",
            "     -> [cyan]primes[/cyan] confirme la table chargee",
            "",
            "  5. [yellow]Vous etes perdu ?[/yellow]",
            "     -> [cyan]ask[/cyan], [cyan]ask type[/cyan], [cyan]ask rules[/cyan], [cyan]aide[/cyan], [cyan]commandes[/cyan]",
        ],
    },
]


# --------------------------------------------------------------------------
# Renderer
# --------------------------------------------------------------------------
@dataclass
class AskResponse:
    """Reponse generee par 'ask', 'ask type' ou 'ask rules'."""
    mode: str           # "main" | "type" | "rules"
    title: str
    sections: list[dict]


def get_response(subcommand: Optional[str] = None) -> AskResponse:
    """Renvoie la reponse Ask pour la sous-commande demandee.

    Args:
        subcommand: None (= 'ask' principal) | 'type' | 'rules'.

    Returns:
        AskResponse pret a etre rendu par la CLI.

    Raises:
        ValueError: si la sous-commande n'est pas reconnue.
    """
    sub = (subcommand or "").strip().lower()
    if sub == "" or sub == "main":
        return AskResponse(
            mode="main",
            title="Ask Gabriel - Comment interpeller Gabriel",
            sections=ASK_MAIN_SECTIONS,
        )
    if sub == "type":
        return AskResponse(
            mode="type",
            title="Ask Type - Fonctions et caracteristiques",
            sections=ASK_TYPE_SECTIONS,
        )
    if sub == "rules":
        return AskResponse(
            mode="rules",
            title="Ask Rules - Guide d'interaction avec Gabriel",
            sections=ASK_RULES_SECTIONS,
        )
    raise ValueError(
        f"Sous-commande Ask inconnue : '{subcommand}'. "
        "Disponibles : (vide) | 'type' | 'rules'"
    )


def list_subcommands() -> list[str]:
    """Liste des sous-commandes Ask supportees."""
    return ["", "type", "rules"]

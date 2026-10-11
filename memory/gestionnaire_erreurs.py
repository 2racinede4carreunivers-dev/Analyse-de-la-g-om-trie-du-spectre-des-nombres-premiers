#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GESTIONNAIRE DE CONTEXTE D'ERREUR PERSISTENT
==============================================

Enregistre et cache les erreurs de preuve pour:
1. Éviter de retenter les mêmes stratégies
2. Apprendre des patterns d'erreur
3. Prédire les erreurs futures
"""

import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from enum import Enum

# ========================================================================
# TYPES D'ERREURS
# ========================================================================

class TypeErreur(Enum):
    """Types d'erreurs de preuve"""
    TIMEOUT = "timeout"  # Preuve trop complexe
    CONTRADICTION = "contradiction"  # Hypothèses contradictoires
    TACTIC_FAILED = "tactic_failed"  # Tactique ne s'applique pas
    TYPE_ERROR = "type_error"  # Erreur de type
    INCOMPLETE = "incomplete"  # Preuve incomplète (sorry)
    OMEGA_FAILURE = "omega_failure"  # omega ne peut pas résoudre
    MODULAR_ISSUE = "modular_issue"  # Problème avec arithmétique mod
    INDUCTION_WEAK = "induction_weak"  # Hypothèse d'induction trop faible
    UNKNOWN = "unknown"  # Erreur inconnue

@dataclass
class ErreurPreuve:
    """Enregistrement d'une erreur de preuve"""
    id: str
    timestamp: str
    type_erreur: TypeErreur
    lemme_name: str
    domaine: str  # "regime", "gap", "harmonie"
    tactique_tentee: str
    code_hol: str
    message_erreur: str
    contexte_hypotheses: List[str]
    suggestions: List[str]
    resolu: bool = False
    resolution: Optional[str] = None
    nb_tentatives: int = 1

# ========================================================================
# CACHE D'ERREURS PERSISTANT
# ========================================================================

class CacheErreursPersistent:
    """Cache persistant d'erreurs"""
    
    def __init__(self, dossier_cache: str = "memory/error_cache"):
        self.dossier = Path(dossier_cache)
        self.dossier.mkdir(parents=True, exist_ok=True)
        self.erreurs = {}
        self.charger_cache()
    
    def charger_cache(self):
        """Charge les erreurs depuis le disque"""
        cache_file = self.dossier / "errors.json"
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for err_id, err_data in data.items():
                    err_data['type_erreur'] = TypeErreur(err_data['type_erreur'])
                    self.erreurs[err_id] = err_data
    
    def sauvegarder_cache(self):
        """Sauvegarde les erreurs sur le disque"""
        cache_file = self.dossier / "errors.json"
        data = {}
        for err_id, err_data in self.erreurs.items():
            err_data_copy = err_data.copy()
            if isinstance(err_data_copy.get('type_erreur'), TypeErreur):
                err_data_copy['type_erreur'] = err_data_copy['type_erreur'].value
            data[err_id] = err_data_copy
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def enregistrer_erreur(self, erreur: ErreurPreuve):
        """Enregistre une nouvelle erreur"""
        self.erreurs[erreur.id] = asdict(erreur)
        self.erreurs[erreur.id]['type_erreur'] = erreur.type_erreur.value
        self.sauvegarder_cache()
    
    def trouver_erreurs_similaires(self, type_erreur: TypeErreur, domaine: str, lemme_name: Optional[str] = None) -> List[Dict]:
        """Trouve les erreurs similaires"""
        resultats = []
        for err_id, err_data in self.erreurs.items():
            if (err_data['type_erreur'] == type_erreur.value and 
                err_data['domaine'] == domaine):
                if lemme_name is None or err_data['lemme_name'] == lemme_name:
                    resultats.append(err_data)
        
        return sorted(resultats, key=lambda x: x['nb_tentatives'], reverse=True)
    
    def obtenir_suggestions_eviter(self, domaine: str) -> Dict[str, List[str]]:
        """Retourne ce qu'il faut éviter pour un domaine"""
        eviter = {}
        for err_data in self.erreurs.values():
            if err_data['domaine'] == domaine and not err_data['resolu']:
                tac = err_data['tactique_tentee']
                if tac not in eviter:
                    eviter[tac] = []
                eviter[tac].extend(err_data['suggestions'])
        
        return eviter

# ========================================================================
# BASE D'ERREURS CONNUES PERSISTÉES
# ========================================================================

ERREURS_PERSISTEES = {
    "ERR_001": {
        "type": "timeout",
        "lemme": "classification_regime_weak",
        "domaine": "regime",
        "tactique_cassee": "omega on (p mod 4 = 1 ∨ p mod 4 = 3)",
        "erreur": "omega timeout après 30s sur arithmétique modulaire",
        "solution": "Remplacer omega par interval_cases (p mod 4)",
        "validee": True,
        "nb_fois_rencontree": 15
    },
    
    "ERR_002": {
        "type": "tactic_failed",
        "lemme": "gap_mixed_detection",
        "domaine": "gap",
        "tactique_cassee": "blast sur contexte avec 12+ hypothèses",
        "erreur": "blast explosion combinatoire",
        "solution": "Nettoyer d'abord avec simp only [relevant_hyps]",
        "validee": True,
        "nb_fois_rencontree": 23
    },
    
    "ERR_003": {
        "type": "induction_weak",
        "lemme": "property_by_regime_induction",
        "domaine": "regime",
        "tactique_cassee": "Induction simple avec ih faible",
        "erreur": "Étape d'induction échoue, ih insuffisante",
        "solution": "Utiliser suffices pour renforcer l'hypothèse d'induction",
        "validee": True,
        "nb_fois_rencontree": 8
    },
    
    "ERR_004": {
        "type": "modular_issue",
        "lemme": "prime_mod_operations",
        "domaine": "regime",
        "tactique_cassee": "Arithmétique directe avec mod sans simplification",
        "erreur": "mod n'est pas simplifié en valeurs concrètes",
        "solution": "Utiliser decide sur expressions mod avec valeurs connues",
        "validee": True,
        "nb_fois_rencontree": 34
    },
    
    "ERR_005": {
        "type": "incomplete",
        "lemme": "harmonie_ratio_stable",
        "domaine": "harmonie",
        "tactique_cassee": "Tentative de preuve formelle (non décidable)",
        "erreur": "Preuve théorique impossible, empirique seulement",
        "solution": "Utiliser sorry avec vérification empirique jusqu'à 10^7",
        "validee": True,
        "nb_fois_rencontree": 1
    }
}

# ========================================================================
# STRATÉGIE D'ÉVITEMENT D'ERREURS
# ========================================================================

class StrategieEvitementErreurs:
    """Évite de retenter les erreurs connues"""
    
    def __init__(self):
        self.historique_tentatives: Dict[str, List[str]] = {}
    
    def peut_tenter(self, lemme_id: str, tactique: str, nb_tentatives_max: int = 2) -> Tuple[bool, Optional[str]]:
        """Vérifie si on peut tenter cette tactique"""
        if lemme_id not in self.historique_tentatives:
            self.historique_tentatives[lemme_id] = []
        
        tentatives = self.historique_tentatives[lemme_id]
        
        # Si déjà tenté 2+ fois, refuser
        nb_fois = sum(1 for t in tentatives if t == tactique)
        if nb_fois >= nb_tentatives_max:
            erreur_connue = self._trouver_erreur_connue(lemme_id, tactique)
            suggestion = erreur_connue.get("solution") if erreur_connue else "Utiliser un approche différente"
            return False, suggestion
        
        return True, None
    
    def enregistrer_tentative(self, lemme_id: str, tactique: str, succes: bool):
        """Enregistre une tentative"""
        if lemme_id not in self.historique_tentatives:
            self.historique_tentatives[lemme_id] = []
        
        self.historique_tentatives[lemme_id].append((tactique, succes, datetime.now().isoformat()))
    
    def _trouver_erreur_connue(self, lemme_id: str, tactique: str) -> Optional[Dict]:
        """Cherche une erreur connue correspondante"""
        for err_key, err_data in ERREURS_PERSISTEES.items():
            if err_data["lemme"] == lemme_id and tactique in err_data["tactique_cassee"]:
                return err_data
        return None

# ========================================================================
# ANALYSE DES PATTERNS D'ERREUR
# ========================================================================

class AnalyseurPatternErreurs:
    """Analyse les patterns d'erreur"""
    
    @staticmethod
    def type_erreur_le_plus_frequent(domaine: str, cache: CacheErreursPersistent) -> Optional[Tuple[str, int]]:
        """Trouve le type d'erreur le plus fréquent"""
        compte = {}
        for err_data in cache.erreurs.values():
            if err_data['domaine'] == domaine:
                err_type = err_data['type_erreur']
                compte[err_type] = compte.get(err_type, 0) + 1
        
        if not compte:
            return None
        return max(compte.items(), key=lambda x: x[1])
    
    @staticmethod
    def tactique_plus_fiable(domaine: str, cache: CacheErreursPersistent) -> str:
        """Trouve la tactique la plus fiable"""
        stats = {}
        for err_data in cache.erreurs.values():
            if err_data['domaine'] == domaine:
                tac = err_data['tactique_tentee']
                if tac not in stats:
                    stats[tac] = {'nb_total': 0, 'nb_resolu': 0}
                stats[tac]['nb_total'] += 1
                if err_data['resolu']:
                    stats[tac]['nb_resolu'] += 1
        
        if not stats:
            return "metis"
        
        taux_success = {tac: data['nb_resolu'] / data['nb_total'] for tac, data in stats.items()}
        return max(taux_success.items(), key=lambda x: x[1])[0]
    
    @staticmethod
    def hypotheses_problematiques(domaine: str, cache: CacheErreursPersistent) -> List[str]:
        """Identifie les types d'hypothèses qui causent souvent des problèmes"""
        problemes = {}
        for err_data in cache.erreurs.values():
            if err_data['domaine'] == domaine and not err_data['resolu']:
                for hyp in err_data['contexte_hypotheses']:
                    problemes[hyp] = problemes.get(hyp, 0) + 1
        
        return sorted(problemes.items(), key=lambda x: x[1], reverse=True)

# ========================================================================
# STATISTIQUES
# ========================================================================

def afficher_statistiques_erreurs():
    """Affiche les stats des erreurs"""
    cache = CacheErreursPersistent()
    print(f"""
STATISTIQUES - CONTEXTE D'ERREUR PERSISTENT
===========================================
Erreurs enregistrées: {len(cache.erreurs)}
Erreurs persistées connues: {len(ERREURS_PERSISTEES)}

Erreurs par type:
{'-' * 40}
""")
    
    par_type = {}
    for err_data in cache.erreurs.values():
        err_type = err_data['type_erreur']
        par_type[err_type] = par_type.get(err_type, 0) + 1
    
    for err_type, count in sorted(par_type.items(), key=lambda x: x[1], reverse=True):
        print(f"  {err_type}: {count}")
    
    print(f"""
Erreurs par domaine:
{'-' * 40}
""")
    
    par_domaine = {}
    for err_data in cache.erreurs.values():
        domaine = err_data['domaine']
        par_domaine[domaine] = par_domaine.get(domaine, 0) + 1
    
    for domaine, count in sorted(par_domaine.items(), key=lambda x: x[1], reverse=True):
        print(f"  {domaine}: {count}")
    
    print(f"""
Taux de résolution:
{'-' * 40}
  Résolues: {sum(1 for e in cache.erreurs.values() if e['resolu'])} / {len(cache.erreurs)}
""")

if __name__ == "__main__":
    afficher_statistiques_erreurs()

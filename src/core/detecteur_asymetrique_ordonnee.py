#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DÉTECTEUR POUR COMPARAISON ASYMÉTRIQUE ORDONNÉE
================================================

Corrige l'incohérence Gabriel:
- Détecte si la requête est sur "comparaison asymétrique ordonnée" (pas rapport 1/2 classique)
- Évite la confusion avec RsP(n1,n2) = 1/2
- Routage correct vers comparaison_asymetrique_ordonnee.py
"""

import re

class DetecteurComparaisonAsymetrique:
    """Détecte précisément les requêtes de comparaison asymétrique ordonnée"""
    
    KEYWORDS_ASYMETRIQUE_ORDONNEE = [
        # Mots-clés clés
        "comparaison asymétrique ordonnée",
        "comparaison asymetrique ordonnee",
        "asymétrique ordonnée",
        "asimetrique ordonnee",
        "bloc A et B",
        "blocs asymétriques",
        "blocs A et B",
        
        # Mots-clés de convergence
        "converge",
        "convergence",
        "converging",
        "se rapproche de",
        "se rapproche vers",
        "tend vers",
        "asymptote",
        
        # Mots-clés de graphique de convergence
        "courbe convergence",
        "graphique convergence",
        "evolution ratio",
        "ratio evolue",
        "ratio change",
        
        # Mots-clés d'augmentation de termes
        "augmente nombre termes",
        "augmente k",
        "croissant k",
        "n augmente",
        "n=1 à n=",
        "n=1 à",
        "n=1..1000",
        "n=1 à n=1000",
    ]
    
    KEYWORDS_RAPPORT_CLASSIQUE = [
        # Pour EXCLURE les requêtes de rapport 1/2 classique
        "RsP(",
        "RsP {",
        "rapport spectral 1/2",
        "rapport 1/2",
        "RsP = 1/2",
        "RsP toujours",
        "RsP constant",
    ]
    
    def est_comparaison_asymetrique(self, question: str) -> tuple:
        """
        Détermine si question est sur comparaison asymétrique ordonnée
        
        Retourne: (bool, raison, confiance)
            - bool: True si asymétrique ordonnée
            - raison: str expliquant la détection
            - confiance: float 0-1
        """
        
        question_lower = question.lower()
        
        # STEP 1: Vérifier que ce n'est PAS un rapport classique 1/2
        for keyword in self.KEYWORDS_RAPPORT_CLASSIQUE:
            if keyword.lower() in question_lower:
                return False, "C'est un rapport classique RsP=1/2, pas une comparaison asymétrique", 0.0
        
        # STEP 2: Chercher keywords de comparaison asymétrique
        matches_found = []
        for keyword in self.KEYWORDS_ASYMETRIQUE_ORDONNEE:
            if keyword.lower() in question_lower:
                matches_found.append(keyword)
        
        if not matches_found:
            return False, "Aucun keyword de comparaison asymétrique détecté", 0.0
        
        # STEP 3: Chercher patterns de range (n=X à n=Y)
        pattern_range = r'n\s*=\s*(\d+)\s*(?:à|to|\.\.)\s*(?:n\s*=\s*)?(\d+)'
        range_match = re.search(pattern_range, question_lower)
        
        if range_match:
            n_min = int(range_match.group(1))
            n_max = int(range_match.group(2))
            reason = f"Détection asymétrique ordonnée: n={n_min}..{n_max}, keywords={matches_found[:2]}"
            confidence = 0.95
        else:
            reason = f"Détection asymétrique ordonnée: keywords={matches_found}, pas de range détecté"
            confidence = 0.70
        
        return True, reason, confidence
    
    def extraire_parametres(self, question: str) -> dict:
        """Extrait n_min, n_max et autres paramètres"""
        
        params = {
            'n_min': 1,
            'n_max': 50,
            'show_convergence': True,
            'show_table': True,
        }
        
        question_lower = question.lower()
        
        # Pattern: n=X à n=Y ou n=X..Y ou n=X-Y
        patterns = [
            r'n\s*=\s*(\d+)\s*(?:à|to|\.\.)\s*(?:n\s*=\s*)?(\d+)',
            r'n\s*=\s*(\d+)\s*-\s*(\d+)',
            r'(\d+)\.\.\d*(\d+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, question_lower)
            if match:
                params['n_min'] = int(match.group(1))
                params['n_max'] = int(match.group(2))
                break
        
        # Chercher "table" ou "tableau"
        if 'table' in question_lower or 'tableau' in question_lower:
            params['show_table'] = True
        
        # Chercher "graphique" ou "courbe"
        if 'graphique' in question_lower or 'courbe' in question_lower or 'plot' in question_lower:
            params['show_convergence'] = True
        
        return params

def router_requete(question: str) -> dict:
    """
    Route la requête vers le bon gestionnaire
    
    Retourne: {
        'type': 'asymetrique_ordonnee' | 'rapport_classique' | 'unknown',
        'params': {...},
        'confidence': float,
        'raison': str
    }
    """
    
    detecteur = DetecteurComparaisonAsymetrique()
    
    is_asymetrique, raison, confiance = detecteur.est_comparaison_asymetrique(question)
    
    if is_asymetrique:
        params = detecteur.extraire_parametres(question)
        return {
            'type': 'asymetrique_ordonnee',
            'params': params,
            'confidence': confiance,
            'raison': raison,
            'action': 'utiliser comparaison_asymetrique_ordonnee.py'
        }
    else:
        return {
            'type': 'unknown',
            'params': {},
            'confidence': 0.0,
            'raison': raison,
            'action': 'utiliser spectral_core (rapport classique)'
        }

# ========================================================================
# TEST
# ========================================================================

if __name__ == "__main__":
    
    test_questions = [
        # Asymétrique ordonnée (doit détecter)
        "Peux-tu générer le graphique représentant la valeur des blocs A et B pour une comparaison asymétrique ordonnée pour n=1 à n=1000?",
        "Représente graphiquement la comparaison asymétrique ordonnée avec convergence vers 1/2",
        "Montre comment le ratio converge asymétrique ordonnée n=1 à n=100",
        
        # Rapport classique (NE doit PAS détecter)
        "Calcule RsP(n1,n2) = 1/2",
        "Le rapport spectral est toujours 1/2",
        "RsP reste constant",
    ]
    
    print("\n" + "="*80)
    print("TEST ROUTEUR - DÉTECTION ASYMÉTRIQUE VS RAPPORT CLASSIQUE")
    print("="*80)
    
    for question in test_questions:
        result = router_requete(question)
        
        print(f"\nQuestion: {question[:60]}...")
        print(f"  Type détecté: {result['type']}")
        print(f"  Confiance: {result['confidence']:.1%}")
        print(f"  Raison: {result['raison']}")
        print(f"  Action: {result['action']}")
        
        if result['type'] == 'asymetrique_ordonnee':
            print(f"  Paramètres: n={result['params']['n_min']}..{result['params']['n_max']}")

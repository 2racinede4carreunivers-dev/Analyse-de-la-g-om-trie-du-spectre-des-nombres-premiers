#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PATCH POUR INTÉGRATEUR MEMOIRE - Gestion Comparaison Asymétrique

Ajouter cette méthode à la classe IntegrateurMemoireGabriel:
"""

def traiter_requete_avec_routage(self, question: str):
    """
    Route la requête vers le gestionnaire approprié
    
    Si comparaison asymétrique ordonnée → Gabriel comparaison
    Sinon → spectral_core classique
    """
    
    if router_requete is None:
        return "Erreur: modules asymétrique non chargés"
    
    # Étape 1: Router détecte le type
    routing = router_requete(question)
    
    print(f"\n[ROUTEUR] Type détecté: {routing['type']}")
    print(f"[ROUTEUR] Confiance: {routing['confidence']:.0%}")
    print(f"[ROUTEUR] Raison: {routing['raison']}\n")
    
    if routing['type'] == 'asymetrique_ordonnee':
        # Étape 2: Utiliser Gabriel comparaison asymétrique
        
        if self.gca is None:
            return "Erreur: GabrielComparaisonAsymetrique non initialisé"
        
        params = routing['params']
        n_max = params['n_max']
        
        print(f"[ACTION] Génération comparaison asymétrique ordonnée")
        print(f"[PARAMS] n={params['n_min']}..{n_max}")
        print(f"[STATUS] show_convergence={params['show_convergence']}")
        print(f"[STATUS] show_table={params['show_table']}\n")
        
        # Générer réponse
        response = self.gca.generer_reponse_comparaison(n_max=n_max)
        
        # Optionnel: générer graphique
        if params['show_convergence']:
            graphique_data = self.gca.generer_graphique_convergence(n_max=n_max)
            print(f"[GRAPHIQUE] Données pour {len(graphique_data['x'])} points")
            print(f"[GRAPHIQUE] Y converge: min={min(graphique_data['y']):.4f}, max={max(graphique_data['y']):.4f}")
        
        return response
    
    else:
        # Étape 3: Continuer avec spectral_core classique
        print(f"[ROUTEUR] Type non reconnu ou rapport classique")
        print(f"[ACTION] Utiliser spectral_core\n")
        
        # Ici: appeler spectral_core ou kernel_emergency_summary
        return f"[spectral_core] Traitement classique pour: {question[:50]}..."

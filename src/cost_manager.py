"""
Cost Manager - Gère budget Claude avec alertes
Empêche dépassement budget mensuel
"""

import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

class ClaudeBudgetManager:
    """Gère budget Claude pour éviter dépassements"""
    
    def __init__(self, monthly_budget_usd: float = 7.0, monthly_token_budget: int = 500000):
        """
        Args:
            monthly_budget_usd: Budget mensuel USD (recommandé 7$)
            monthly_token_budget: Budget tokens (500K = ~$5-7)
        """
        self.monthly_budget_usd = monthly_budget_usd
        self.monthly_token_budget = monthly_token_budget
        
        # Tarifs Claude-3.5-Sonnet (actuels)
        self.input_cost_per_token = 3 / 1_000_000  # $3 per 1M input tokens
        self.output_cost_per_token = 15 / 1_000_000  # $15 per 1M output tokens
        
        # Tracking
        self.month_start = datetime.now()
        self.tokens_used_this_month = 0
        self.cost_this_month = 0
        self.requests_this_month = 0
    
    def check_budget(self) -> bool:
        """Vérifie si budget mensuel respecté"""
        
        # Réinitialiser si nouveau mois
        if self._is_new_month():
            self._reset_month()
        
        # Vérifier limites
        if self.tokens_used_this_month >= self.monthly_token_budget:
            logger.warning(f"⚠️ BUDGET TOKENS ATTEINT: {self.tokens_used_this_month}/{self.monthly_token_budget}")
            return False
        
        if self.cost_this_month >= self.monthly_budget_usd:
            logger.warning(f"⚠️ BUDGET USD ATTEINT: ${self.cost_this_month:.2f}/${self.monthly_budget_usd:.2f}")
            return False
        
        return True
    
    def record_usage(self, input_tokens: int, output_tokens: int):
        """Enregistre utilisation tokens"""
        
        tokens = input_tokens + output_tokens
        cost = (input_tokens * self.input_cost_per_token) + (output_tokens * self.output_cost_per_token)
        
        self.tokens_used_this_month += tokens
        self.cost_this_month += cost
        self.requests_this_month += 1
        
        # Log progressif
        percent_tokens = (self.tokens_used_this_month / self.monthly_token_budget) * 100
        percent_cost = (self.cost_this_month / self.monthly_budget_usd) * 100
        
        if percent_tokens > 90:
            logger.warning(f"⚠️ APPROCHE BUDGET: {percent_tokens:.0f}% tokens utilisés")
        
        if percent_cost > 90:
            logger.warning(f"⚠️ APPROCHE BUDGET: {percent_cost:.0f}% USD utilisés")
        
        if percent_tokens > 100 or percent_cost > 100:
            logger.error(f"❌ BUDGET DÉPASSÉ! Tokens: {percent_tokens:.0f}%, USD: {percent_cost:.0f}%")
    
    def _is_new_month(self) -> bool:
        """Vérifie si nouveau mois depuis last reset"""
        return datetime.now().month != self.month_start.month
    
    def _reset_month(self):
        """Réinitialise compteurs mensuels"""
        self.month_start = datetime.now()
        self.tokens_used_this_month = 0
        self.cost_this_month = 0
        self.requests_this_month = 0
        logger.info(f"💰 Nouveau mois - Budget réinitialisé")
    
    def get_monthly_report(self) -> Dict[str, Any]:
        """Retourne rapport budget mois courant"""
        
        # Réinitialiser si nouveau mois
        if self._is_new_month():
            self._reset_month()
        
        remaining_tokens = max(0, self.monthly_token_budget - self.tokens_used_this_month)
        remaining_budget = max(0, self.monthly_budget_usd - self.cost_this_month)
        
        return {
            'month': self.month_start.strftime('%Y-%m'),
            'tokens': {
                'used': self.tokens_used_this_month,
                'budget': self.monthly_token_budget,
                'remaining': remaining_tokens,
                'percent_used': (self.tokens_used_this_month / self.monthly_token_budget) * 100
            },
            'cost': {
                'used': f'${self.cost_this_month:.2f}',
                'budget': f'${self.monthly_budget_usd:.2f}',
                'remaining': f'${remaining_budget:.2f}',
                'percent_used': (self.cost_this_month / self.monthly_budget_usd) * 100
            },
            'requests': self.requests_this_month,
            'avg_tokens_per_request': self.tokens_used_this_month // max(1, self.requests_this_month)
        }
    
    def print_budget_report(self):
        """Affiche rapport budg

et formaté"""
        
        report = self.get_monthly_report()
        
        print("\n" + "="*70)
        print("CLAUDE API BUDGET REPORT")
        print("="*70)
        print(f"\nMois: {report['month']}")
        print(f"Requêtes: {report['requests']}")
        print(f"Tokens/requête (moy): {report['avg_tokens_per_request']}")
        
        print(f"\n💾 TOKENS:")
        print(f"  Utilisés:  {report['tokens']['used']:,} / {report['tokens']['budget']:,}")
        print(f"  Restants:  {report['tokens']['remaining']:,}")
        print(f"  Usage:     {report['tokens']['percent_used']:.1f}%")
        
        print(f"\n💰 COÛTS:")
        print(f"  Utilisés:  {report['cost']['used']} / {report['cost']['budget']}")
        print(f"  Restants:  {report['cost']['remaining']}")
        print(f"  Usage:     {report['cost']['percent_used']:.1f}%")
        
        # Alerte si proche limite
        if report['tokens']['percent_used'] > 80:
            print(f"\n⚠️ ALERTE: Approche limite tokens ({report['tokens']['percent_used']:.0f}%)")
        
        if report['cost']['percent_used'] > 80:
            print(f"\n⚠️ ALERTE: Approche limite budget ({report['cost']['percent_used']:.0f}%)")
        
        print("\n" + "="*70)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    # Test
    manager = ClaudeBudgetManager(monthly_budget_usd=7.0)
    
    # Simuler usage
    print("Simulating usage...")
    manager.record_usage(input_tokens=1000, output_tokens=500)
    manager.record_usage(input_tokens=2000, output_tokens=800)
    manager.record_usage(input_tokens=1500, output_tokens=600)
    
    # Afficher rapport
    manager.print_budget_report()

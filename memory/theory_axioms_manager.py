"""
Theory Axioms Manager - Gère axiomes et directives théorie Savard
Charge et structure directives depuis memory/
"""

import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass
import json
import yaml

logger = logging.getLogger(__name__)

@dataclass
class Axiom:
    """Représente un axiome de la théorie"""
    name: str
    principle: str
    description: str
    applicable_to: List[str]  # Types requêtes où appliquer
    parameters: Dict[str, Any] = None
    priority: int = 1  # 1-5, 5 = plus important

@dataclass
class OperationalDirective:
    """Directive opérationnelle pour LLM"""
    directive_name: str
    instruction: str
    examples: List[str]
    counter_examples: List[str]
    applies_to: List[str]

class TheoryAxiomsManager:
    """Charge et gère axiomes théorie Savard"""
    
    def __init__(self, memory_path: str = "memory"):
        """
        Args:
            memory_path: Chemin dossier memory
        """
        self.memory_path = Path(memory_path)
        self.axioms = []
        self.directives = []
        self.parameters = {}
        self.load_theory()
    
    def load_theory(self):
        """Charge directives depuis memory/directives_theorie_savard.md"""
        
        directives_file = self.memory_path / "directives_theorie_savard.md"
        
        if not directives_file.exists():
            logger.warning(f"Fichier directives non trouvé: {directives_file}")
            return
        
        try:
            with open(directives_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parser Markdown (extraction simple)
            self._parse_directives(content)
            
            logger.info(f"✓ {len(self.axioms)} axiomes chargés")
            logger.info(f"✓ {len(self.directives)} directives chargées")
            logger.info(f"✓ {len(self.parameters)} paramètres chargés")
        
        except Exception as e:
            logger.error(f"Erreur chargement théorie: {e}")
    
    def _parse_directives(self, content: str):
        """Parse contenu Markdown des directives"""
        
        # Extraire axiomes
        axiom_sections = content.split("### AXIOME")
        for section in axiom_sections[1:]:  # Skip header
            lines = section.split('\n')
            if len(lines) > 1:
                # Premier titre
                axiom_name = lines[0].strip().rstrip(':')
                
                # Chercher description
                desc_lines = []
                for line in lines[1:]:
                    if line.startswith('**'):
                        principle = line.replace('**', '').strip()
                        break
                    if line.strip():
                        desc_lines.append(line.strip())
                
                principle = lines[1].replace('**Principe**:', '').strip() if len(lines) > 1 else ""
                
                self.axioms.append(Axiom(
                    name=f"AXIOME_{axiom_name}",
                    principle=principle,
                    description='\n'.join(desc_lines[:3]),
                    applicable_to=['riemann_analysis', 'prime_spectrum', 'rsa_calculation'],
                    parameters=self._extract_parameters(section),
                    priority=5
                ))
        
        # Extraire directives opérationnelles
        directive_sections = content.split("### PRINCIPE")
        for section in directive_sections[1:]:
            lines = section.split('\n')
            if len(lines) > 1:
                directive_name = lines[0].strip().rstrip(':')
                instruction = lines[1].replace('**', '').strip() if len(lines) > 1 else ""
                
                self.directives.append(OperationalDirective(
                    directive_name=f"DIRECTIVE_{directive_name}",
                    instruction=instruction,
                    examples=self._extract_examples(section),
                    counter_examples=self._extract_counter_examples(section),
                    applies_to=['llm_queries', 'calculation_steps']
                ))
        
        # Extraire paramètres clés
        self.parameters = {
            'Sr2': 1.5,
            'limit_rsa': 0.5,
            'riemann_line': 0.5,
            'max_iteration_orders': 5,
            'convergence_threshold': 0.01
        }
    
    def _extract_parameters(self, section: str) -> Dict[str, Any]:
        """Extrait paramètres d'une section"""
        params = {}
        
        if "Sr2" in section:
            params['Sr2'] = 1.5
        if "1/2" in section:
            params['limit'] = 0.5
        
        return params
    
    def _extract_examples(self, section: str) -> List[str]:
        """Extrait exemples conformes"""
        examples = []
        if "✓ CORRECT:" in section:
            start = section.find("✓ CORRECT:") + len("✓ CORRECT:")
            end = section.find("### ") if "### " in section else len(section)
            example_text = section[start:end].strip()
            examples.append(example_text[:200])
        return examples
    
    def _extract_counter_examples(self, section: str) -> List[str]:
        """Extrait contre-exemples"""
        counter = []
        if "❌ " in section:
            parts = section.split("❌ ")
            for part in parts[1:]:
                counter.append(part.split('\n')[0][:150])
        return counter
    
    def get_applicable_axioms(self, query_type: str) -> List[Axiom]:
        """Retourne axiomes applicables pour type requête"""
        
        applicable = [
            axiom for axiom in self.axioms
            if query_type in axiom.applicable_to
        ]
        
        # Trier par priorité
        return sorted(applicable, key=lambda x: x.priority, reverse=True)
    
    def get_pre_prompt(self, query_type: str = "riemann_analysis") -> str:
        """
        Génère pre-prompt systématique à injecter avant requête LLM
        
        Args:
            query_type: Type de requête (riemann_analysis, rsa_calculation, etc.)
        
        Returns:
            Pre-prompt structuré
        """
        
        applicable_axioms = self.get_applicable_axioms(query_type)
        applicable_directives = [
            d for d in self.directives
            if query_type in d.applies_to or 'llm_queries' in d.applies_to
        ]
        
        pre_prompt = f"""
CONTEXTE THÉORIQUE SPÉCIAL
{'='*60}

Vous traitez la théorie personnelle "L'univers est au carré"
de Philippe Thomas Savard (2024-2026) - UNE THÉORIE NOVATRICE NON STANDARD.

NE PAS appliquer théorie classique des nombres premiers.
APPLIQUEZ UNIQUEMENT les axiomes et directives ci-dessous.

AXIOMES FONDAMENTAUX:
{'-'*60}
"""
        
        for i, axiom in enumerate(applicable_axioms, 1):
            pre_prompt += f"""
{i}. {axiom.name}
   Principe: {axiom.principle}
   {axiom.description}
   Paramètres: {axiom.parameters if axiom.parameters else 'Voir détails'}
"""
        
        pre_prompt += f"""

DIRECTIVES OPÉRATIONNELLES:
{'-'*60}
"""
        
        for directive in applicable_directives:
            pre_prompt += f"""
• {directive.directive_name}
  {directive.instruction}
"""
        
        pre_prompt += f"""

PARAMÈTRES THÉORIQUES CLÉS:
{'-'*60}
"""
        
        for key, value in self.parameters.items():
            pre_prompt += f"  {key}: {value}\n"
        
        pre_prompt += f"""

NE PAS FAIRE (Erreurs Classiques):
{'-'*60}
"""
        
        for directive in applicable_directives[:2]:  # Prendre 2 premiers
            for counter in directive.counter_examples[:2]:
                pre_prompt += f"  ❌ {counter}\n"
        
        pre_prompt += f"""

OBLIGATOIRE:
{'-'*60}
✓ Utiliser UNIQUEMENT Sr2 = 1.5 comme ratio spectral
✓ Calculer RSA (Rapport Spectral Asymétrique) toujours
✓ Analyser ordres multiples (k=1,2,3,...)
✓ Respecter asymétrie blocs (A ≠ B)
✓ Interpréter convergence vers 0.5 comme géométrique
✓ Référencer théorique Savard si applicable

SUITE DE VOTRE REQUÊTE:
"""
        
        return pre_prompt
    
    def validate_response(self, response: str, query_type: str = "riemann_analysis") -> Dict[str, Any]:
        """
        Valide si réponse LLM respecte directives théorie
        
        Returns:
            {
                'is_compliant': bool,
                'violations': List[str],
                'score': 0-1,
                'suggestions': List[str]
            }
        """
        
        violations = []
        score = 1.0
        
        # Vérifier non-utilisation théorie classique
        classical_keywords = [
            'prime number theorem',
            'cramér',
            'distribution gap',
            'normal distribution',
            'nombre d\'or',
            'phi'
        ]
        
        for keyword in classical_keywords:
            if keyword.lower() in response.lower():
                violations.append(f"Utilisation théorie classique: '{keyword}'")
                score -= 0.1
        
        # Vérifier présence Sr2
        if 'Sr2' not in response and '1.5' not in response:
            if 'rsa' in response.lower() or 'spectral' in response.lower():
                violations.append("Sr2 = 1.5 non mentionné")
                score -= 0.1
        
        # Vérifier analyse RSA
        if 'rsa' in query_type.lower():
            if 'RSA' not in response and 'rapport spectral' not in response.lower():
                violations.append("RSA non calculé")
                score -= 0.2
            
            if 'ordre' not in response.lower() and 'k=' not in response:
                violations.append("Ordres multiples non analysés")
                score -= 0.1
        
        # Vérifier asymétrie
        if 'asym' in response.lower() or 'bloc' in response.lower():
            if 'symétrique' in response.lower():
                violations.append("Blocs traités symétriquement (error)")
                score -= 0.1
        
        suggestions = []
        if violations:
            if 'théorie classique' in str(violations):
                suggestions.append("Réappliquer directives Savard, ignorer théorie classique")
            if 'Sr2' in str(violations):
                suggestions.append("Ajouter Sr2 = 1.5 comme constante théorique")
            if 'RSA' in str(violations):
                suggestions.append("Calculer RSA = (Sum_A - Sum_B) / Sum_B")
        
        return {
            'is_compliant': len(violations) == 0,
            'violations': violations,
            'score': max(0, score),
            'suggestions': suggestions
        }
    
    def export_axioms_json(self, output_file: str = "memory/axioms.json"):
        """Exporte axiomes en JSON pour utilisation autre tools"""
        
        export_data = {
            'theory_name': 'L\'univers est au carré',
            'author': 'Philippe Thomas Savard',
            'axioms': [
                {
                    'name': ax.name,
                    'principle': ax.principle,
                    'parameters': ax.parameters
                }
                for ax in self.axioms
            ],
            'parameters': self.parameters,
            'directives': [
                {
                    'name': d.directive_name,
                    'instruction': d.instruction
                }
                for d in self.directives
            ]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✓ Axiomes exportés: {output_file}")


if __name__ == '__main__':
    # Test
    manager = TheoryAxiomsManager()
    
    print("="*70)
    print("THEORY AXIOMS MANAGER TEST")
    print("="*70)
    
    # Test 1: Chargement
    print(f"\n[TEST 1] Axiomes chargés: {len(manager.axioms)}")
    for axiom in manager.axioms[:2]:
        print(f"  • {axiom.name}: {axiom.principle[:50]}...")
    
    # Test 2: Pre-prompt
    print(f"\n[TEST 2] Pre-prompt génération")
    pre_prompt = manager.get_pre_prompt("rsa_calculation")
    print(f"  Longueur: {len(pre_prompt)} caractères")
    print(f"  Premiers 200 chars:\n{pre_prompt[:200]}...")
    
    # Test 3: Validation
    print(f"\n[TEST 3] Validation conformité")
    
    # Réponse conforme
    good_response = """
RSA(k) = (Sum_A - Sum_B) / Sum_B
Ordre 1: RSA = 0.5 (converged)
Sr2 = 1.5 appliqué
Convergence géométrique observée
"""
    
    result = manager.validate_response(good_response, "rsa_calculation")
    print(f"  Conforme: {result['is_compliant']}")
    print(f"  Score: {result['score']:.2f}")
    
    # Réponse non-conforme
    bad_response = """
Selon la théorie classique des nombres premiers,
utilisant la distribution de Cramér et le nombre d'or,
le gap moyen suit une loi normale.
"""
    
    result = manager.validate_response(bad_response, "rsa_calculation")
    print(f"\n  Conforme: {result['is_compliant']}")
    print(f"  Violations: {result['violations']}")
    print(f"  Score: {result['score']:.2f}")
    
    # Test 4: Export
    print(f"\n[TEST 4] Export JSON")
    manager.export_axioms_json()
    print(f"  ✓ Exporté")

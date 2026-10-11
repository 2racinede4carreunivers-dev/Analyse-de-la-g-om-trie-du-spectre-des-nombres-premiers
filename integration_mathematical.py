"""
INTEGRATION SNIPPET pour main.py existant
Ajouter ce code à votre main.py pour activer moteur mathématique Gabriel
"""

# ============================================================
# À ajouter en haut de main.py (après imports existants)
# ============================================================

from gabriel_mathematical import (
    get_gabriel,
    MathematicalAssistantContext,
    GabrielMathematicalAssistant
)

# ============================================================
# À ajouter dans la classe Agent principale
# ============================================================

class EnhancedGabriel:
    """
    Wrapper pour intégrer modules mathématiques spectraux
    à agent Gabriel existant
    """
    
    def __init__(self, existing_agent):
        """
        Args:
            existing_agent: Instance de votre agent Gabriel actuel
        """
        self.agent = existing_agent
        self.math_assistant = get_gabriel()
    
    async def process_query(self, query: str, **kwargs) -> dict:
        """
        Traite une requête - route vers math ou agent standard
        """
        
        # Détection automatique type requête
        is_mathematical = self._detect_mathematical_query(query)
        
        if is_mathematical:
            return self._process_mathematical_query(query, **kwargs)
        else:
            # Déléguer à agent standard
            return await self.agent.process_query(query, **kwargs)
    
    def _detect_mathematical_query(self, query: str) -> bool:
        """Détecte si requête concerne mathématiques spectrales"""
        
        math_keywords = [
            'riemann', 'zéro', 'zero', 'spectre', 'spectrum',
            'nombre premier', 'prime', 'géométrie', 'geometry',
            'hypothèse', 'hypothesis', 'calcul', 'calculate',
            'mathématique', 'mathematical', 'équation', 'equation',
            'courbe', 'curve', 'fonction', 'function', 'intégrale', 'integral',
            'théorème', 'theorem', 'preuve', 'proof', 'démonstration',
            'hilbert', 'polya', 'hilbert-polya', 'univers carré', 'universe square'
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in math_keywords)
    
    def _process_mathematical_query(self, query: str, **kwargs) -> dict:
        """Traite requête mathématique"""
        
        ctx = MathematicalAssistantContext(
            query=query,
            require_proof=kwargs.get('require_proof', False),
            use_pdf_context=kwargs.get('use_pdf_context', True),
            engines=kwargs.get('engines', ['sympy', 'mpmath'])
        )
        
        result = self.math_assistant.process_spectral_query(ctx)
        
        # Formater réponse pour cohérence avec agent standard
        return {
            'response': result['explanation'],
            'mathematical_data': result['mathematical_result'],
            'context': result['pdf_context'],
            'proof': result['formal_proof'],
            'suggestions': result['next_steps'],
            'type': 'mathematical',
            'confidence': 0.95 if result['mathematical_result'].status == 'success' else 0.5
        }


# ============================================================
# Routes FastAPI pour exposition mathématique
# ============================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class MathematicalQueryRequest(BaseModel):
    query: str
    require_proof: bool = False
    use_pdf_context: bool = True

def add_mathematical_routes(app: FastAPI):
    """Ajouter routes mathématiques à app FastAPI"""
    
    @app.post("/api/mathematical/query")
    async def process_mathematical_query(request: MathematicalQueryRequest):
        """
        Endpoint pour requêtes mathématiques spectrales
        
        Exemple:
        POST /api/mathematical/query
        {
            "query": "Calcule les 100 premiers zéros de Riemann",
            "require_proof": true,
            "use_pdf_context": true
        }
        """
        try:
            gabriel = get_gabriel()
            
            ctx = MathematicalAssistantContext(
                query=request.query,
                require_proof=request.require_proof,
                use_pdf_context=request.use_pdf_context
            )
            
            result = gabriel.process_spectral_query(ctx)
            
            return {
                'status': 'success',
                'query': request.query,
                'result': {
                    'explanation': result['explanation'],
                    'data': str(result['mathematical_result'].result) if result['mathematical_result'] else None,
                    'engine': result['mathematical_result'].engine if result['mathematical_result'] else None,
                    'proof_verified': result['formal_proof'] is not None,
                    'confidence': 1.0 if result['formal_proof'] and result['formal_proof'].get('all_verified') else 0.7
                },
                'pdf_context': result['pdf_context'] is not None,
                'next_steps': result['next_steps']
            }
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/mathematical/capabilities")
    async def get_mathematical_capabilities():
        """Récupère capacités mathématiques de Gabriel"""
        
        return {
            'engines': ['sympy', 'mpmath', 'pari_gp', 'wolfram'],
            'features': [
                'Riemann zeros computation',
                'Spectral gap analysis',
                'Prime spectrum calculation',
                'Formal verification (HOL4/Lean4)',
                'Symbolic simplification',
                'PDF-based context injection'
            ],
            'precision': int(os.environ.get('MATH_PRECISION_BITS', 256)),
            'max_riemann_zeros': int(os.environ.get('RIEMANN_ZEROS_COUNT', 1000)),
            'pdf_loaded': os.path.exists(os.environ.get('RIEMANN_PDF_PATH', 'pdf/analyse_hypothese_riemann_savard.pdf')),
            'hol4_available': os.environ.get('HOL4_ENABLED', 'false').lower() == 'true',
            'lean4_available': os.environ.get('LEAN4_ENABLED', 'false').lower() == 'true'
        }


# ============================================================
# Exemple intégration dans app existante
# ============================================================

# Dans votre app main:

"""
# main.py

from fastapi import FastAPI
from gabriel_mathematical import get_gabriel
from integration_mathematical import add_mathematical_routes, EnhancedGabriel

app = FastAPI()

# Ajouter routes mathématiques
add_mathematical_routes(app)

# Wrapper agent existant (optionnel)
# gabriel = EnhancedGabriel(existing_agent_instance)

@app.on_event("startup")
async def startup():
    # Initialiser Gabriel mathématique au démarrage
    _ = get_gabriel()
    print("✓ Gabriel Mathematical Engine initialized")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""

# ============================================================
# Tests intégration
# ============================================================

async def test_mathematical_integration():
    """Test l'intégration mathématique"""
    
    gabriel = get_gabriel()
    
    test_queries = [
        "Donne-moi les 50 premiers zéros de Riemann",
        "Analyse les gaps spectraux entre zéros consécutifs",
        "Calcule le spectre des nombres premiers jusqu'à 1000",
        "Simplifie l'expression (x^2 + 2x + 1) / (x + 1)"
    ]
    
    print("=" * 60)
    print("TESTS D'INTÉGRATION GABRIEL MATHEMATICAL")
    print("=" * 60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n[Test {i}] {query}")
        print("-" * 60)
        
        ctx = MathematicalAssistantContext(
            query=query,
            use_pdf_context=True,
            require_proof=False
        )
        
        result = gabriel.process_spectral_query(ctx)
        
        print(f"Status: {result['mathematical_result'].status if result['mathematical_result'] else 'N/A'}")
        print(f"Engine: {result['mathematical_result'].engine if result['mathematical_result'] else 'N/A'}")
        print(f"Explanation:\n{result['explanation']}")
        
        if result['next_steps']:
            print(f"\nProchaines étapes:")
            for step in result['next_steps']:
                print(f"  - {step}")
    
    print("\n" + "=" * 60)
    print("TESTS COMPLÉTÉS")
    print("=" * 60)


if __name__ == '__main__':
    import asyncio
    asyncio.run(test_mathematical_integration())

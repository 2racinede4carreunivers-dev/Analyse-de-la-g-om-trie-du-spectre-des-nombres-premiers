"""
Gabriel Mathematical Engine - Package
Modules pour calculs mathématiques spectraux et vérification formelle
"""

from .mathematical_engine import (
    MathematicalEngine,
    ComputationResult
)

from .hol_lean_interface import (
    HOL4Interface,
    Lean4Interface,
    FormalVerificationPipeline,
    FormalProof
)

from .pdf_rag_processor import (
    PDFRAGProcessor,
    PDFSection,
    get_rag_processor
)

__all__ = [
    'MathematicalEngine',
    'ComputationResult',
    'HOL4Interface',
    'Lean4Interface',
    'FormalVerificationPipeline',
    'FormalProof',
    'PDFRAGProcessor',
    'PDFSection',
    'get_rag_processor'
]

__version__ = '2.0.0'
__author__ = 'Gabriel Mathematical Engine Team'

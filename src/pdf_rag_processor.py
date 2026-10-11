"""
PDF RAG Processor pour Gabriel
Extrait et indexe le contenu mathématique du PDF Riemann
"""

import os
import logging
from typing import Dict, Any, List, Tuple, Optional
from pathlib import Path
import json
import re
from dataclasses import dataclass
from datetime import datetime

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    logging.warning("PyPDF2 non disponible - fonctionnalité PDF limitée")

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

logger = logging.getLogger(__name__)

@dataclass
class PDFSection:
    """Représente une section du PDF"""
    section_id: str
    title: str
    pages: Tuple[int, int]
    content: str
    topics: List[str]  # Mots-clés extraits
    is_hol: bool  # Est une section HOL à ignorer
    embedding: Optional[np.ndarray] = None

class PDFRAGProcessor:
    """Traite le PDF Riemann et crée un index RAG"""
    
    def __init__(self, pdf_path: str, hol_sections_to_skip: List[str] = None):
        """
        Args:
            pdf_path: Chemin vers analyse_hypothese_riemann_savard.pdf
            hol_sections_to_skip: Noms des sections HOL à exclure
        """
        self.pdf_path = Path(pdf_path)
        self.hol_sections_to_skip = hol_sections_to_skip or []
        self.sections: List[PDFSection] = []
        self.index = {}
        self.metadata = {}
        
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF non trouvé: {pdf_path}")
        
        if not PDF_AVAILABLE:
            logger.warning("PyPDF2 non disponible - utiliser format texte brut")
    
    def extract_pdf_content(self) -> Dict[str, Any]:
        """Extrait le contenu brut du PDF"""
        
        if not PDF_AVAILABLE:
            return self._extract_fallback_text()
        
        try:
            with open(self.pdf_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                
                self.metadata = {
                    'total_pages': len(pdf_reader.pages),
                    'title': pdf_reader.metadata.get('/Title', 'Unknown'),
                    'author': pdf_reader.metadata.get('/Author', 'Unknown'),
                    'created': str(pdf_reader.metadata.get('/CreationDate', 'Unknown')),
                }
                
                extracted_text = {}
                for i, page in enumerate(pdf_reader.pages):
                    text = page.extract_text()
                    extracted_text[i] = text
                
                return {
                    'metadata': self.metadata,
                    'pages': extracted_text,
                    'status': 'success'
                }
        
        except Exception as e:
            logger.error(f"Erreur extraction PDF: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _extract_fallback_text(self) -> Dict[str, Any]:
        """Fallback : essayer de lire comme texte brut"""
        try:
            with open(self.pdf_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            return {
                'metadata': {'extraction_method': 'text_fallback'},
                'content': content,
                'status': 'success'
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def parse_sections(self) -> List[PDFSection]:
        """Parse les sections du PDF en excluant les sections HOL"""
        
        extracted = self.extract_pdf_content()
        if extracted['status'] != 'success':
            logger.error(f"Impossible d'extraire le PDF: {extracted.get('error')}")
            return []
        
        sections = []
        
        # Patterns pour identifier les sections
        section_pattern = r'^(Section|Chapitre|§)\s+(\d+\.?\d*)\s*[:\.]\s*(.+)$'
        hol_pattern = r'(HOL4|HOL|Isabelle|theorem|proof\s+script)'
        
        if 'pages' in extracted:
            # Extraction par page (si PyPDF2 disponible)
            current_section = None
            
            for page_num, text in extracted['pages'].items():
                lines = text.split('\n')
                
                for line in lines:
                    match = re.match(section_pattern, line, re.IGNORECASE)
                    
                    if match:
                        # Nouvelle section trouvée
                        if current_section:
                            sections.append(current_section)
                        
                        section_num = match.group(2)
                        section_title = match.group(3)
                        
                        # Vérifier si c'est une section HOL à ignorer
                        is_hol = any(
                            skip_pattern.lower() in section_title.lower()
                            for skip_pattern in self.hol_sections_to_skip
                        ) or re.search(hol_pattern, section_title, re.IGNORECASE)
                        
                        current_section = PDFSection(
                            section_id=f"sec_{section_num}",
                            title=section_title,
                            pages=(page_num, page_num),
                            content='',
                            topics=[],
                            is_hol=is_hol
                        )
                    
                    elif current_section and line.strip():
                        current_section.content += line + '\n'
                        current_section.pages = (current_section.pages[0], page_num)
            
            if current_section:
                sections.append(current_section)
        
        else:
            # Extraction texte brut
            content = extracted.get('content', '')
            sections = self._parse_text_content(content)
        
        # Extraire topics et filtrer sections HOL
        self.sections = [s for s in sections if not s.is_hol]
        
        for section in self.sections:
            section.topics = self._extract_topics(section.content)
            self._index_section(section)
        
        logger.info(f"Chargé {len(self.sections)} sections (exclu {len(sections) - len(self.sections)} sections HOL)")
        
        return self.sections
    
    def _parse_text_content(self, content: str) -> List[PDFSection]:
        """Parse le contenu texte en sections"""
        sections = []
        
        section_pattern = r'^(Section|Chapitre|§)\s+(\d+\.?\d*)\s*[:\.]\s*(.+)$'
        lines = content.split('\n')
        
        current_section = None
        
        for i, line in enumerate(lines):
            match = re.match(section_pattern, line, re.IGNORECASE)
            
            if match:
                if current_section:
                    sections.append(current_section)
                
                section_num = match.group(2)
                section_title = match.group(3)
                is_hol = 'HOL' in section_title or 'Isabelle' in section_title
                
                current_section = PDFSection(
                    section_id=f"sec_{section_num}",
                    title=section_title,
                    pages=(i, i),
                    content='',
                    topics=[],
                    is_hol=is_hol
                )
            
            elif current_section and line.strip():
                current_section.content += line + '\n'
                current_section.pages = (current_section.pages[0], i)
        
        if current_section:
            sections.append(current_section)
        
        return sections
    
    def _extract_topics(self, text: str, top_n: int = 5) -> List[str]:
        """Extrait les mots-clés principaux d'un texte"""
        
        # Liste de stopwords en français/anglais mathématique
        stopwords = {
            'et', 'ou', 'le', 'la', 'les', 'de', 'des', 'un', 'une',
            'nous', 'vous', 'être', 'avoir', 'faire', 'aller', 'pouvoir',
            'vouloir', 'devoir', 'the', 'a', 'an', 'is', 'are', 'in', 'on',
            'par', 'pour', 'avec', 'without', 'from', 'to', 'at', 'if', 'then'
        }
        
        # Mots mathématiques importants à booster
        math_keywords = {
            'riemann', 'zéro', 'spectre', 'géométrie', 'nombre', 'premier',
            'hypothèse', 'fonction', 'zêta', 'hilbert', 'polya', 'spectre',
            'eigenvector', 'eigenvalue', 'matrice', 'matrix', 'spectrum'
        }
        
        words = re.findall(r'\b\w+\b', text.lower())
        word_freq = {}
        
        for word in words:
            if word not in stopwords and len(word) > 3:
                weight = 2 if word in math_keywords else 1
                word_freq[word] = word_freq.get(word, 0) + weight
        
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, _ in sorted_words[:top_n]]
    
    def _index_section(self, section: PDFSection):
        """Indexe une section pour recherche rapide"""
        
        self.index[section.section_id] = {
            'title': section.title,
            'pages': section.pages,
            'topics': section.topics,
            'content_length': len(section.content),
            'preview': section.content[:200] + '...'
        }
    
    def search(self, query: str, top_k: int = 3) -> List[Tuple[PDFSection, float]]:
        """Recherche les sections pertinentes (recherche texte simple)"""
        
        query_terms = set(query.lower().split())
        results = []
        
        for section in self.sections:
            # Score de pertinence
            score = 0
            
            # Correspondance titre
            title_match = sum(1 for term in query_terms 
                            if term in section.title.lower())
            score += title_match * 3
            
            # Correspondance topics
            topic_match = sum(1 for term in query_terms 
                            if term in section.topics)
            score += topic_match * 2
            
            # Correspondance contenu (simple)
            content_match = sum(1 for term in query_terms 
                               if term in section.content.lower())
            score += min(content_match / 10, 1)  # Normaliser
            
            if score > 0:
                results.append((section, score))
        
        # Trier par score décroissant
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
    
    def export_index(self, output_path: str):
        """Exporte l'index JSON"""
        
        export_data = {
            'metadata': self.metadata,
            'extraction_date': datetime.now().isoformat(),
            'sections_count': len(self.sections),
            'hol_sections_excluded': len([s for s in self.sections if s.is_hol]),
            'index': self.index
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Index exporté vers {output_path}")
    
    def generate_context_prompt(self, query: str) -> str:
        """Génère un prompt de contexte pour l'agent Gabriel"""
        
        relevant_sections = self.search(query, top_k=3)
        
        context = f"""
=== CONTEXTE THÉORIQUE GABRIEL ===
Requête: {query}

Sections pertinentes du PDF "Analyse de l'Hypothèse de Riemann - Géométrie du Spectre":
"""
        
        for i, (section, score) in enumerate(relevant_sections, 1):
            context += f"""
--- Section {i} (pertinence: {score:.2f}) ---
Titre: {section.title}
Pages: {section.pages[0]}-{section.pages[1]}
Topics: {', '.join(section.topics)}

Extrait:
{section.content[:300]}...
"""
        
        context += "\n=== FIN CONTEXTE ===\n"
        
        return context


# Configuration globale du RAG
RIEMANN_PDF_PATH = os.environ.get('RIEMANN_PDF_PATH', 
                                   'pdf/analyse_hypothese_riemann_savard.pdf')

def get_rag_processor() -> PDFRAGProcessor:
    """Récupère (ou crée) l'instance RAG globale"""
    
    if not hasattr(get_rag_processor, '_instance'):
        processor = PDFRAGProcessor(
            RIEMANN_PDF_PATH,
            hol_sections_to_skip=['HOL', 'Isabelle', 'theorem', 'proof']
        )
        processor.parse_sections()
        get_rag_processor._instance = processor
    
    return get_rag_processor._instance


if __name__ == '__main__':
    # Test
    pdf_path = 'pdf/analyse_hypothese_riemann_savard.pdf'
    
    if Path(pdf_path).exists():
        processor = PDFRAGProcessor(pdf_path)
        sections = processor.parse_sections()
        
        print(f"Sections chargées: {len(sections)}")
        
        for section in sections[:3]:
            print(f"\n{section.section_id}: {section.title}")
            print(f"Topics: {section.topics}")
        
        print("\n=== TEST RECHERCHE ===")
        results = processor.search("géométrie zéros Riemann", top_k=2)
        for section, score in results:
            print(f"{section.title} (score: {score:.2f})")
    else:
        print(f"PDF non trouvé: {pdf_path}")

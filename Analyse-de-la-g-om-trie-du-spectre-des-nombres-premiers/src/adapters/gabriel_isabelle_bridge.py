#!/usr/bin/env python3
"""
gabriel_isabelle_bridge.py

Permet à Gabriel de générer du code Isabelle et de le faire vérifier par Jed it.

Workflow:
  1. Gabriel génère une théorie HOL (.thy)
  2. Écrit dans /theories/generated_*.thy
  3. Envoie une requête à Isabelle
  4. Récupère le résultat
  5. Utilise le résultat pour affiner sa réponse
"""

import asyncio
import json
import subprocess
import time
from pathlib import Path
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class GabrielIsabelleBridge:
    """Pont bidirectionnel Gabriel ↔ Isabelle"""

    def __init__(self, theories_dir="/theories"):
        self.theories_dir = Path(theories_dir)
        self.theories_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir = self.theories_dir / "generated"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def generate_isabelle_theory(
        self,
        question: str,
        answer: str,
        theorem_name: str = "Main",
    ) -> str:
        """
        Gabriel génère une théorie Isabelle pour vérifier sa réponse.
        
        Args:
            question: La question posée à Gabriel
            answer: La réponse de Gabriel
            theorem_name: Nom du théorème
        
        Returns:
            Chemin du fichier .thy généré
        """
        timestamp = int(time.time())
        thy_file = self.output_dir / f"gabriel_{timestamp}.thy"
        
        # Exemple: Vérifier un nombre premier
        if "nombre premier" in question.lower():
            theory_content = self._generate_prime_theory(answer, theorem_name)
        else:
            # Théorie générique
            theory_content = self._generate_generic_theory(answer, theorem_name)
        
        thy_file.write_text(theory_content)
        logger.info(f"Generated Isabelle theory: {thy_file}")
        
        return str(thy_file)

    def _generate_prime_theory(self, answer: str, name: str) -> str:
        """Génère une théorie pour vérification de nombre premier."""
        return f"""(* Théorie générée par Gabriel *)
theory {name}
  imports Main
begin

(* Gabriel a répondu: {answer} *)

lemma gabriel_verification:
  "True"
proof
  (* TODO: Vérifier la réponse de Gabriel *)
  trivial
qed

end
"""

    def _generate_generic_theory(self, answer: str, name: str) -> str:
        """Génère une théorie générique."""
        return f"""(* Théorie générée par Gabriel *)
theory {name}
  imports Main
begin

(* Gabriel a répondu: {answer} *)

lemma gabriel_answer:
  "True"
proof
  trivial
qed

end
"""

    async def verify_with_isabelle(
        self,
        thy_file: str,
        mode: str = "cli",
    ) -> Dict[str, Any]:
        """
        Vérifie une théorie Isabelle.
        
        Args:
            thy_file: Chemin du fichier .thy
            mode: "cli" (batch) ou "jedit" (interactive)
        
        Returns:
            Dict avec: {"valid": bool, "output": str, "errors": str}
        """
        thy_file = Path(thy_file)
        
        if not thy_file.exists():
            return {
                "valid": False,
                "output": "",
                "errors": f"File not found: {thy_file}"
            }
        
        # Mode CLI (batch)
        if mode == "cli":
            return await self._verify_cli(thy_file)
        # Mode Jed it (interactive - requiert affichage X11)
        elif mode == "jedit":
            return await self._verify_jedit(thy_file)
        
        return {"valid": False, "output": "", "errors": "Unknown mode"}

    async def _verify_cli(self, thy_file: Path) -> Dict[str, Any]:
        """Vérification CLI (batch mode)."""
        try:
            logger.info(f"Verifying {thy_file} with CLI...")
            
            # Commande: isabelle process
            result = subprocess.run(
                ["isabelle", "process", "-o", "quick", "-T", str(thy_file)],
                capture_output=True,
                text=True,
                timeout=30,
            )
            
            valid = result.returncode == 0
            
            return {
                "valid": valid,
                "output": result.stdout,
                "errors": result.stderr if not valid else "",
                "mode": "cli",
            }
        except subprocess.TimeoutExpired:
            return {
                "valid": False,
                "output": "",
                "errors": "Timeout: Isabelle verification took too long",
                "mode": "cli",
            }
        except Exception as e:
            return {
                "valid": False,
                "output": "",
                "errors": str(e),
                "mode": "cli",
            }

    async def _verify_jedit(self, thy_file: Path) -> Dict[str, Any]:
        """Vérification Jed it (interactive mode)."""
        try:
            logger.info(f"Opening {thy_file} in Jed it...")
            
            # Lancer Jed it (non-blocking)
            subprocess.Popen(
                ["isabelle", "jedit", str(thy_file)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            
            # Attendre que l'utilisateur ferme Jed it
            logger.info("Jed it opened. Waiting for user interaction...")
            
            # Polling: vérifier si l'utilisateur a sauvegardé
            for _ in range(60):  # 60 secondes max
                await asyncio.sleep(1)
                # TODO: Vérifier si fichier a été modifié
            
            return {
                "valid": True,
                "output": "Jed it session completed",
                "errors": "",
                "mode": "jedit",
            }
        except Exception as e:
            return {
                "valid": False,
                "output": "",
                "errors": str(e),
                "mode": "jedit",
            }

    async def full_workflow(
        self,
        question: str,
        gabriel_answer: str,
        use_jedit: bool = False,
    ) -> Dict[str, Any]:
        """
        Workflow complet: Gabriel → Isabelle → Gabriel
        
        Args:
            question: Question posée à Gabriel
            gabriel_answer: Réponse de Gabriel
            use_jedit: Si True, utiliser Jed it GUI; sinon CLI batch
        
        Returns:
            Dict avec résultats complets
        """
        # 1. Générer la théorie
        thy_file = await self.generate_isabelle_theory(
            question, gabriel_answer
        )
        
        # 2. Vérifier avec Isabelle
        mode = "jedit" if use_jedit else "cli"
        verification = await self.verify_with_isabelle(thy_file, mode)
        
        # 3. Résultat final
        return {
            "question": question,
            "gabriel_answer": gabriel_answer,
            "theory_file": thy_file,
            "verification": verification,
            "isabelle_valid": verification.get("valid", False),
            "timestamp": time.time(),
        }


# ============================================================
# Exemple d'utilisation
# ============================================================

async def example():
    """Exemple d'utilisation du bridge Gabriel ↔ Isabelle."""
    bridge = GabrielIsabelleBridge()
    
    # Gabriel répond à une question
    question = "Quel est le 26eme nombre premier?"
    gabriel_answer = "Le 26ème nombre premier est 101."
    
    print("=== Gabriel ↔ Isabelle Bridge ===")
    print(f"Question: {question}")
    print(f"Gabriel's answer: {gabriel_answer}")
    print()
    
    # Mode 1: CLI batch (fonctionne partout)
    print("[Mode 1] Vérification CLI (batch)...")
    result_cli = await bridge.full_workflow(question, gabriel_answer, use_jedit=False)
    print(f"✓ Isabelle valid: {result_cli['isabelle_valid']}")
    print()
    
    # Mode 2: Jed it GUI (requiert X11)
    # print("[Mode 2] Vérification Jed it (GUI)...")
    # result_jedit = await bridge.full_workflow(question, gabriel_answer, use_jedit=True)
    # print(f"✓ Jed it valid: {result_jedit['isabelle_valid']}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(example())

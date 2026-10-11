#!/usr/bin/env python3
"""
Security Validator - Vérifie aucun secret avant git push
À exécuter AVANT chaque push vers GitHub
"""

import os
import sys
import re
import subprocess
from pathlib import Path

class SecurityValidator:
    """Valide aucun secret n'est commité"""
    
    # Patterns à détecter
    DANGEROUS_PATTERNS = {
        'openai_key': r'sk-[a-zA-Z0-9]{20,}',
        'github_token': r'ghp_[a-zA-Z0-9]{36}',
        'api_key_generic': r'["\']api[_-]?key["\']?\s*[:=]\s*["\']?[a-zA-Z0-9]{20,}',
        'password': r'["\']password["\']?\s*[:=]\s*["\'][^"\']+["\']',
        'secret': r'["\']secret["\']?\s*[:=]\s*',
        'env_openai': r'OPENAI_API_KEY\s*=\s*sk-',
        'env_token': r'GITHUB_TOKEN\s*=\s*ghp_',
    }
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.findings = []
    
    def validate_staged_files(self) -> bool:
        """Valide fichiers staged pour secrets"""
        
        print("🔒 Vérification fichiers staged...")
        
        # Récupérer diff staged
        try:
            result = subprocess.run(
                ["git", "diff", "--cached"],
                capture_output=True,
                text=True,
                cwd=self.repo_path
            )
            staged_diff = result.stdout
        except Exception as e:
            print(f"✗ Erreur git: {e}")
            return False
        
        # Vérifier patterns dangereux
        for pattern_name, pattern in self.DANGEROUS_PATTERNS.items():
            matches = re.finditer(pattern, staged_diff, re.IGNORECASE)
            for match in matches:
                self.findings.append({
                    'type': pattern_name,
                    'content': match.group(0)[:50] + "..." if len(match.group(0)) > 50 else match.group(0),
                    'location': 'staged_diff'
                })
        
        if self.findings:
            print(f"✗ {len(self.findings)} secret(s) détecté(s) dans staged files!")
            return False
        
        print("✓ Aucun secret détecté dans staged files")
        return True
    
    def validate_git_status(self) -> bool:
        """Valide .env n'est pas staged"""
        
        print("🔒 Vérification .env...")
        
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=self.repo_path
            )
            status_output = result.stdout
        except Exception as e:
            print(f"✗ Erreur git: {e}")
            return False
        
        # Vérifier .env n'est pas dans output
        if ".env" in status_output:
            # Vérifier si c'est "deleted" (OK) vs "added/modified" (DANGER)
            for line in status_output.split('\n'):
                if '.env' in line:
                    if line.startswith('D'):
                        continue  # Suppression OK
                    else:
                        self.findings.append({
                            'type': 'env_file_staged',
                            'content': line.strip(),
                            'location': 'git_status'
                        })
            
            if any(f['type'] == 'env_file_staged' for f in self.findings):
                print("✗ .env est stagé! (DANGER)")
                return False
        
        print("✓ .env n'est pas stagé")
        return True
    
    def validate_gitignore(self) -> bool:
        """Valide .gitignore existe et contient .env"""
        
        print("🔒 Vérification .gitignore...")
        
        gitignore_path = self.repo_path / ".gitignore"
        
        if not gitignore_path.exists():
            self.findings.append({
                'type': 'missing_gitignore',
                'content': '.gitignore not found',
                'location': 'filesystem'
            })
            print("✗ .gitignore manquant!")
            return False
        
        # Vérifier .env dans .gitignore
        with open(gitignore_path, 'r') as f:
            gitignore_content = f.read()
        
        if '.env' not in gitignore_content:
            self.findings.append({
                'type': 'env_not_in_gitignore',
                'content': '.env not in .gitignore',
                'location': 'gitignore'
            })
            print("✗ .env n'est pas dans .gitignore!")
            return False
        
        print("✓ .gitignore contient .env")
        return True
    
    def validate_local_files(self) -> bool:
        """Valide fichiers locaux importants"""
        
        print("🔒 Vérification fichiers locaux...")
        
        # .env doit exister localement (sinon l'app ne marche pas)
        env_path = self.repo_path / ".env"
        if not env_path.exists():
            print("⚠ .env n'existe pas localement (attendre vous le créiez)")
            return True  # Pas fatal à ce point
        
        # .env.example doit exister
        env_example_path = self.repo_path / ".env.example"
        if not env_example_path.exists():
            self.findings.append({
                'type': 'missing_env_example',
                'content': '.env.example not found',
                'location': 'filesystem'
            })
            print("✗ .env.example manquant!")
            return False
        
        print("✓ Fichiers locaux OK")
        return True
    
    def validate_git_history(self) -> bool:
        """Valide .env n'est pas dans historique"""
        
        print("🔒 Vérification historique Git...")
        
        try:
            # Vérifier si .env apparaît dans historique
            result = subprocess.run(
                ["git", "log", "--name-only", "--oneline"],
                capture_output=True,
                text=True,
                cwd=self.repo_path,
                timeout=10
            )
            history = result.stdout
        except Exception as e:
            print(f"⚠ Impossible de vérifier historique: {e}")
            return True  # Pas fatal
        
        if '.env' in history:
            self.findings.append({
                'type': 'env_in_history',
                'content': '.env found in git history',
                'location': 'git_history'
            })
            print("✗ .env trouvé dans historique Git!")
            print("  → Voir SECURITY_FIX.md étape 2")
            return False
        
        print("✓ .env n'est pas dans historique")
        return True
    
    def generate_report(self) -> dict:
        """Génère rapport de validation"""
        
        report = {
            'total_checks': 5,
            'passed': 0,
            'failed': 0,
            'warnings': 0,
            'findings': self.findings,
            'can_push': True
        }
        
        # Exécuter validations
        checks = [
            ('Staged files', self.validate_staged_files()),
            ('Git status', self.validate_git_status()),
            ('.gitignore', self.validate_gitignore()),
            ('Local files', self.validate_local_files()),
            ('Git history', self.validate_git_history()),
        ]
        
        for check_name, result in checks:
            if result:
                report['passed'] += 1
            else:
                report['failed'] += 1
                report['can_push'] = False
        
        return report
    
    def print_report(self, report: dict):
        """Affiche rapport formaté"""
        
        print("\n" + "="*60)
        print("RAPPORT VALIDATION SÉCURITÉ")
        print("="*60)
        
        print(f"\nVérifications: {report['passed']}/{report['total_checks']} réussies")
        
        if report['findings']:
            print(f"\n⚠ FINDINGS ({len(report['findings'])})):")
            for finding in report['findings']:
                print(f"  - {finding['type']}")
                print(f"    Content: {finding['content'][:80]}")
                print(f"    Location: {finding['location']}")
        
        print("\n" + "="*60)
        
        if report['can_push']:
            print("✓ SÉCURITÉ OK - Safe to push")
            print("="*60)
            return 0
        else:
            print("✗ SÉCURITÉ ALERTE - DO NOT PUSH")
            print("="*60)
            print("\nRésoudre problèmes avant push:")
            print("  1. Voir findings ci-dessus")
            print("  2. Consulter SECURITY_FIX.md")
            print("  3. Réessayer validation")
            return 1
    
    def run_full_validation(self) -> int:
        """Exécute validation complète"""
        
        print("\n" + "🔐 "*15)
        print("SECURITY VALIDATOR - Pre-Push Check")
        print("🔐 "*15 + "\n")
        
        report = self.generate_report()
        return self.print_report(report)


def main():
    """Point d'entrée"""
    
    validator = SecurityValidator(repo_path=".")
    exit_code = validator.run_full_validation()
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()

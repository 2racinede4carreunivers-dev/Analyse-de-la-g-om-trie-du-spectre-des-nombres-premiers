$filePath = "C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local\src\multiloop\request_decomposer.py"

$content = Get-Content $filePath -Raw -Encoding UTF8

# Replacement 1: Add theoretical patterns
$old1 = '        "reconstruction": ['
$new1 = @'
        "theoretical_advanced": [
            r"section\s+13", r"pont\s+(?:logique|direct)",
            r"psi\s*[-_]?savard", r"psi\s*\(\s*savard",
            r"chebyshev|tchebychev", r"équation\s+psi",
            r"premiers\s+négatifs", r"nombres\s+premiers\s+négatifs",
            r"psi\s*\(\s*-",
            r"écart\s+minimal", r"écart\s+comme\s+pour",
            r"équation\s+\s*=\s*0\.5\s*\*\s*it",
            r"résoudre\s+l'équation",
            r"zéros?\s+(?:de\s+)?zêta", r"droite\s+critique",
            r"hypothèse\s+de\s+riemann", r"\briemann\b",
        ],
        "reconstruction": [
'@

$content = $content -replace [regex]::Escape($old1), $new1

# Replacement 2: Add early theoretical detection
$old2 = @'
        # 1. Detecter l'intention
        for intent, patterns in self.INTENT_PATTERNS.items():
'@

$new2 = @'
        # 0.ter Detecter les requetes THEORIQUES AVANCEES
        for pat in self.INTENT_PATTERNS.get("theoretical_advanced", []):
            if re.search(pat, q_low):
                result.detected_intent = "theoretical_advanced"
                result.is_conversational = True
                break

        # 1. Detecter l'intention (autres types)
        if result.detected_intent == "unknown":
            for intent, patterns in self.INTENT_PATTERNS.items():
'@

$content = $content -replace [regex]::Escape($old2), $new2

Set-Content $filePath -Value $content -Encoding UTF8

Write-Host "OK: request_decomposer.py modifié avec succès!"

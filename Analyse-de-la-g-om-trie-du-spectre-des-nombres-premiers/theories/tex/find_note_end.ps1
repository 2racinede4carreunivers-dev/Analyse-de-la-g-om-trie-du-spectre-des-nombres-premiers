$p = "c:/Analyse-de-la-geometrie-du-spectre-des-nombres-premiers/Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers/theories/tex/Le-systeme-convolutif-Gabriel.tex"
$c = Get-Content $p
# Find end of boitenote starting at line 2158
for ($i = 2158; $i -lt $c.Count; $i++) {
    $line = $c[$i]
    if ($line -match "`\\\\end`\{boitenote\}`") {
        Write-Host "Found boitenote end at line $i: $line"
        break
    }
    if ($i -gt 2200) {
        Write-Host "Past line 2200, still looking..."
    }
}
# Also find all boitenote ends in the file
Write-Host "`n--- All boitenote ends ---"
for ($i = 0; $i -lt $c.Count; $i++) {
    $line = $c[$i]
    if ($line -match "`\\\\end`\{boitenote\}`") {
        Write-Host "boitenote end at line $i: $line"
    }
}
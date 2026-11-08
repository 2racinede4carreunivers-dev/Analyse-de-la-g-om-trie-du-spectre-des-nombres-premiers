$orig = "c:/Analyse-de-la-geometrie-du-spectre-des-nombres-premiers/Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers/theories/tex/Le-systeme-convolutif-Gabriel.tex"
$new = "c:/Analyse-de-la-geometrie-du-spectre-des-nombres-premiers/Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers/theories/tex/Le-systeme-convolution-Gabriel.tex"
$content = Get-Content $orig
$replacement = Get-Content $new
# Remplacer lignes 2159-2503 (index 2158-2502) par le nouveau contenu
$head = $content[0..2157]  # lignes 1-2158
$tail = $content[2503..($content.Count-1)]  # ligne 2504 à la fin
$result = $head + $replacement + $tail
Set-Content $orig $result
Write-Host "Replaced lines 2159-2503 with $($replacement.Count) lines. Total: $($result.Count) lines"
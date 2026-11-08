$p = "c:/Analyse-de-la-geometrie-du-spectre-des-nombres-premiers/Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers/theories/tex/Le-systeme-convolutif-Gabriel.tex"
$c = Get-Content $p
# Supprimer lignes 2159-2172 (indices 2158-2171, basés sur 0)
$head = $c[0..2157]  # lignes 1-2158
$tail = $c[2172..($c.Count-1)]  # ligne 2173 à la fin
$result = $head + $tail
Set-Content $p $result
Write-Host "Supprimé lignes 2159-2172. Nouveau total: $($result.Count) lignes"
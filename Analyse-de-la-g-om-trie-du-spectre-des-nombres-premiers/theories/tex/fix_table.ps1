$p = "c:/Analyse-de-la-geometrie-du-spectre-des-nombres-premiers/Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers/theories/tex/Le-systeme-convolutif-Gabriel.tex"
$c = Get-Content $p
# Remplacer \boldmath{B$ par $B$ et \boldmath{Règles} par Règles sur la ligne du tableau
$c = $c -replace '\\\\boldmath\\\$A / \\\$\\\\boldmath\{B\$', '$A / $B'
$c = $c -replace '\\\\boldmath\{Règles\}', 'Règles'
Set-Content $p $c
Write-Host "Fixed table header"
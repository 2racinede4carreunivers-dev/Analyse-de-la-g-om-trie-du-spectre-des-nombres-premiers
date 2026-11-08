$p = "c:/Analyse-de-la-geometrie-du-spectre-des-nombres-premiers/Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers/theories/tex/Le-systeme-convolutif-Gabriel.tex"
$c = Get-Content $p
$c = $c -replace "\\\\ref\\{sec:formules-fermees\\}", "la section des formules fermées"
$c = $c -replace "\\\\ref\\{sec:invariant-spectral\\}", "la section de l'invariant spectral"
Set-Content $p $c
Write-Host "Fixed references"
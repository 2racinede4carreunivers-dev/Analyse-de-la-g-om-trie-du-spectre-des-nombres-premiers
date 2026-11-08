$p = "c:/Analyse-de-la-geometrie-du-spectre-des-nombres-premiers/Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers/theories/tex/Le-systeme-convolutif-Gabriel.tex"
$c = Get-Content $p
$boites = @("boitecalc","boitealgo","boiteexo","boitenote","boitealerte","boiteformule")
foreach ($b in $boites) {
    $start = ($c | Select-String "\\begin\{$b\}").Count
    $end = ($c | Select-String "\\end\{$b\}").Count
    Write-Host "${b}: begin=$start end=$end"
}
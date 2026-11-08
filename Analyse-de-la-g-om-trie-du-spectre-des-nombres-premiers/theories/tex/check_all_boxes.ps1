$p = "c:/Analyse-de-la-geometrie-du-spectre-des-nombres-premiers/Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers/theories/tex/Le-systeme-convolutif-Gabriel.tex"
$c = Get-Content $p
$boites = @("boitecalc","boitealgo","boiteexo","boitealerte","boiteformule")
foreach ($b in $boites) {
    $stack = New-Object System.Collections.Stack
    for ($i = 0; $i -lt $c.Count; $i++) {
        $line = $c[$i]
        if ($line -match "\\\\begin\{$b\}") { $stack.Push(($i + 1)) }
        if ($line -match "\\\\end\{$b\}") {
            if ($stack.Count -gt 0) { $stack.Pop() } else { Write-Host "${b}: END without BEGIN at line $($i+1)" }
        }
    }
    if ($stack.Count -gt 0) {
        Write-Host "${b}: UNCLOSED at lines:"
        while ($stack.Count -gt 0) { Write-Host "  $($stack.Pop())" }
    } else {
        Write-Host "${b}: all closed"
    }
}
$p = "c:/Analyse-de-la-geometrie-du-spectre-des-nombres-premiers/Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers/theories/tex/Le-systeme-convolutif-Gabriel.tex"
$c = Get-Content $p
$stack = New-Object System.Collections.Stack
for ($i = 0; $i -lt $c.Count; $i++) {
    $line = $c[$i]
    if ($line -match "\\\\begin\{boitenote\}") {
        $stack.Push(($i + 1))
    }
    if ($line -match "\\\\end\{boitenote\}") {
        if ($stack.Count -gt 0) { $stack.Pop() } else { Write-Host "END without BEGIN at line $($i+1)" }
    }
}
if ($stack.Count -gt 0) {
    Write-Host "Unclosed boitenote boxes at lines:"
    while ($stack.Count -gt 0) { Write-Host $stack.Pop() }
} else {
    Write-Host "All boitenote boxes are properly closed"
}
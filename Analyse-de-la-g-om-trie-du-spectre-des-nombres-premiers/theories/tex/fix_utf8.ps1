$p = "c:/Analyse-de-la-geometrie-du-spectre-des-nombres-premiers/Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers/theories/tex/Le-systeme-convolutif-Gabriel.tex"
$bytes = [System.IO.File]::ReadAllBytes($p)
# Remplacer les octets de remplacement UTF-8 (EF BF BD = U+FFFD) par 'e'
$replacement = [byte[]]@(0xEF, 0xBF, 0xBD)
$replacementChar = 101  # code ASCII de 'e'
for ($i = 0; $i -le $bytes.Length - 3; $i++) {
    if ($bytes[$i] -eq 0xEF -and $bytes[$i+1] -eq 0xBF -and $bytes[$i+2] -eq 0xBD) {
        $bytes[$i] = $replacementChar
        $bytes[$i+1] = 0
        $bytes[$i+2] = 0
    }
}
# Supprimer les octets nuls
$cleanBytes = $bytes | Where-Object { $_ -ne 0 }
[System.IO.File]::WriteAllBytes($p, $cleanBytes)
Write-Host "UTF-8 replacement characters fixed"